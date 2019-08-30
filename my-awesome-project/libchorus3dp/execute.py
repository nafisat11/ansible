#Carries out the process of executing instructions and recording pass/fail
#state for each host.

import collections
import logging
import os
import tempfile
import threading
import time
import traceback

import ansible.parsing.dataloader
import ansible.vars
import ansible.inventory
import ansible.executor.playbook_executor

from . import config
from . import db

_logger = logging.getLogger('execute')

_SINGLE_HOST_THREAD_COUNT = 5

_AnsibleExecutorOptions = collections.namedtuple('Options', [
    'listtags',
    'listtasks',
    'listhosts',
    'syntax',
    'connection',
    'module_path',
    'forks',
    'remote_user',
    'verbosity',
    'check',
    'become',
    'become_method',
    'become_user',
])
class _AnsibleExecutor(object):
    _playbook = None
    _executor = None
    
    def __init__(self, playbook, hosts, local_blob_path):
        self._playbook = tempfile.NamedTemporaryFile()
        self._playbook.write(playbook.encode('utf-8'))
        self._playbook.flush()
        
        variable_manager = ansible.vars.VariableManager()
        variable_manager.extra_vars = {
            'ce__local_blob_path': local_blob_path,
        }
        loader = ansible.parsing.dataloader.DataLoader()
        
        inventory = ansible.inventory.Inventory(
            loader=loader,
            variable_manager=variable_manager,
            host_list=hosts,
        )
        
        options = _AnsibleExecutorOptions(
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            connection='ssh',
            module_path=None,
            forks=5,
            remote_user='root',
            verbosity=None,
            check=False,
            become=False,
            become_method=None,
            become_user=None,
        )
        
        self._executor = ansible.executor.playbook_executor.PlaybookExecutor(
            playbooks=[self._playbook.name],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=None,
        )
        
    def execute(self):
        results = self._executor.run()
        
        retry_file_path = self._playbook.name + '.retry'
        failed_hosts = []
        try:
            for host in open(retry_file_path):
                host = host.strip()
                if host:
                    failed_hosts.append(host)
        except IOError: #No retry-file written
            pass
        else:
            try:
                os.unlink(retry_file_path)
            except Exception as e:
                _logger.warn("Unable to unlink {path}".format(
                    path=retry_file_path,
                ))
        return failed_hosts
        
class _SingleHostThread(threading.Thread):
    _NAME = 'single-host'
    _executor = None
    
    def __init__(self, executor):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = self._NAME
        
        self._executor = executor
        
    def run(self):
        while True:
            time.sleep(1)
            instructions_id = self._executor.get_single_host_instructions_id(self)
            if instructions_id is None:
                continue
                
            success = False
            try:
                instructions_details = self._database.retrieve_instructions_details(instructions_id)
                if instructions_details is None:
                    #The result can be None if the database was modified
                    continue
                (retry, date, name, host) = instructions_details
                
                executor = _AnsibleExecutor(
                    playbook=instructions,
                    hosts=[host],
                    local_blob_path=os.path.join(config.TASK_FILEPATH, 'single', str(instructions_id), 'data'),
                )
                failed_hosts = executor.execute()
                
                _logger.info("{failed}/{total} hosts failed".format(
                    failed=len(failed_hosts),
                    total=len(hosts),
                ))
                
                success = host not in failed_hosts
                if success:
                    self._database.delete_instructions_single(instructions_id)
            except Exception:
                #Any unhandled failures during execution may break instructions-ordering
                #Wipe the slate and start over for consistency
                _logger.error("Unable to execute:\n{error}".format(
                    error=traceback.format_exc(),
                ))
            else:
                if not retry:
                    self._database.cull_instructions_single(instructions_id)
            finally:
                self._executor.release_single_host_instructions_id(self, instructions_id, success)
                
class _Executor(threading.Thread):
    #WARNING: this thread, and its single-host worker-threads, do not join
    #Graceful shutdowns are not currently possible
    
    _host_status = None #:A dictionary of hostnames and pass/fail status to this point
    
    _instructions = None #:A deque of instruction-IDs yet-unprocessed
    _instructions_lock = None #:A lock used to ensure that new tasks are queued in deterministic order
    
    _idle = True #:True if between cycles
    
    _database = None #:A database connection
    
    _next_cycle = 0.0 #:The timestamp at which to next fill the instructions-queue and run again
    
    _single_host_threads = None #:A collection of single-host threads, {thread: host}
    _single_host_tasks = None #:A dictionary of single-host tasks to be executed, {host: instruction_id}
    _single_host_task_lock = None #:A lock used to prevent races related to single-host tasks
    
    #WARNING: this is a debug feature. In practice, there should be no reason to pause execution
    #versus initiating a controlled shutdown.
    _paused = False #True while execution is suspended
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.name = 'executor'
        
        self._host_status = collections.defaultdict(lambda:True)
        self._instructions = collections.deque()
        self._instructions_lock = threading.Lock()
        
        self._database = db.Database()
        
        self._single_host_task_lock = threading.Lock()
        self._single_host_tasks = {}
        self._single_host_threads = dict((_SingleHostThread(self), None) for i in range(_SINGLE_HOST_THREAD_COUNT))
        for i in self._single_host_threads:
            i.start()
            
    def _load_instructions(self):
        """
        Must only be called while _instructions_lock is held.
        """
        self._host_status.clear()
        if not self._paused:
            self._instructions = self._database.enumerate_instructions()
            self._idle = False
            
            #Update outstanding single-host tasks
            #It's okay if this collides with an in-progress task, since the IDs won't change
            with self._single_host_task_lock:
                self._single_host_tasks = self._database.enumerate_instructions_single()
                for host in self._single_host_tasks:
                    self._host_status[host] = False #Don't attempt to run instructions on not-yet-synced hosts
            _logger.info("Prepared {count} tasks".format(count=len(self._instructions)))
        else:
            _logger.info("Task-execution is paused")
            
        #Schedule the next cycle a minute into the future,
        #just to prevent excessive retries on offline hosts
        self._next_cycle = time.time() + 60
        
    def load_instructions(self):
        """
        Allows newly added instructions to execute as soon as possible, rather
        than waiting for a full sleep-cycle if between-tasks.
        
        This will indirectly reset the sleep-cycle.
        """
        with self._instructions_lock:
            if self._idle:
                self._load_instructions()
                
    def _sort_key_get_single_host_instructions_id(self, element):
        return element[1]
    def get_single_host_instructions_id(self, single_host_thread):
        with self._single_host_task_lock:
            if single_host_thread not in self._single_host_threads:
                raise ValueError("Unrecognised thread: {}".format(single_host_thread))
                
            #Exclude any hosts already being processed
            candidate_hosts = self._single_host_tasks.copy()
            for host in self._single_host_threads.values():
                if host is not None and host in candidate_hosts:
                    del candidate_hosts[host]
                    
            if not candidate_hosts:
                return None
                
            #Determine which host has the most work outstanding
            (host, instructions_ids) = sorted(
                candidate_hosts.items(),
                key=self._sort_key_get_single_host_instructions_id,
                reverse=True,
            )[0]
            
            #Update the assignment
            self._single_host_threads[single_host_thread] = host
            return instructions_ids[0]
            
    def release_single_host_instructions_id(self, single_host_thread, instructions_id, success):
        with self._single_host_task_lock:
            host = self._single_host_threads[single_host_thread]
            tasks = self._single_host_tasks.get(host)
            if tasks is None:
                _logger.info("{host} has no outstanding tasks".format(host=host))
                return
                
            if not success:
                del self._single_host_tasks[host]
                _logger.info("Marked {host} as failed".format(host=host))
                return
                
            if instructions_id in tasks:
                tasks.remove(instructions_id)
                _logger.info("Marked {instructions_id} as complete".format(instructions_id=instructions_id))
                if not tasks:
                    del self._single_host_tasks[host]
            else:
                _logger.info("Ignored unknown task {instructions_id}".format(instructions_id=instructions_id))
                
    def run(self):
        while True:
            instructions_id = None
            with self._instructions_lock:
                if self._instructions:
                    instructions_id = self._instructions.popleft()
            if instructions_id:
                try:
                    instructions_details = self._database.retrieve_instructions_details(instructions_id)
                    if instructions_details is None:
                        continue
                    (retry, date, name, candidate_hosts) = instructions_details
                    
                    #Filter the list such that only hosts that have passed until this point are eligible
                    hosts = [host for host in candidate_hosts if self._host_status[host]]
                    _logger.info("Preparing to execute {date}/{name} over {count} hosts...".format(
                        date=date,
                        name=name,
                        count=len(hosts),
                    ))
                    if not hosts: #Nothing is eligible for this instruction-set
                        continue
                        
                    #Execute over the set of hosts
                    executor = _AnsibleExecutor(
                        playbook=instructions,
                        hosts=hosts,
                        local_blob_path=os.path.join(config.TASK_FILEPATH, 'multi', str(instructions_id), 'data'),
                    )
                    failed_hosts = executor.execute()
                    
                    _logger.info("{failed}/{total} hosts failed".format(
                        failed=len(failed_hosts),
                        total=len(hosts),
                    ))
                    
                    #Mark every failed host
                    for host in failed_hosts:
                        if host:
                            self._host_status[host] = False
                            
                    #Filter the list of attempted hosts to leave only those that succeeded
                    hosts = [host for host in hosts if self._host_status[host]]
                    
                    #Clear hosts that succeeded
                    self._database.clear_succeeded(instructions_id, hosts)
                except Exception:
                    #Any unhandled failures during execution may break instructions-ordering
                    _logger.error("Unable to execute:\n{error}".format(
                        error=traceback.format_exc(),
                    ))
                    #Wipe the slate and start over for consistency
                    with self._instructions_lock:
                        self._load_instructions()
                else:
                    if not retry:
                        self._database.cull_instructions(instructions_id)
            else:
                if time.time() > self._next_cycle:
                    with self._instructions_lock:
                        self._load_instructions()
                else:
                    _logger.debug("Nothing to do")
                    with self._instructions_lock:
                        self._idle = True
                    time.sleep(1)
                    
    def pause(self):
        with self._instructions_lock:
            self._paused = True
            self._load_instructions()
            _logger.info("Paused execution")
            
    def restart(self):
        with self._instructions_lock:
            self._paused = False
            self._load_instructions()
            _logger.info("Restarted execution")
            
EXECUTOR = _Executor()
EXECUTOR.start()
