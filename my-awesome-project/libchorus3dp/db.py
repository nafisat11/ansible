#NOTE: THIS IS ONLY A PROTOTYPE

import collections
import io
import logging
import os
import shutil
import sqlite3
import tarfile

from . import config

_logger = logging.getLogger('db')

def _te_resolved(path):
    return os.path.realpath(os.path.abspath(x))
def _te_badpath(path, base):
    return not _te_resolved(joinpath(base, path)).startswith(base)
def _te_badlink(info, base):
    tip = _te_resolved(os.path.join(base, os.path.dirname(info.name)))
    return _te_badpath(info.linkname, base=tip)
def _te_safemembers(members):
    base = _te_resolved(".")
    for finfo in members:
        if _te_badpath(finfo.name, base):
            _logger.warn("{name} is blocked: illegal path".format(
                name=finfo.name,
            ))
        elif finfo.issym() and _te_badlink(finfo, base):
            _logger.warn("{name} is blocked: invalid hardlink to {link}".format(
                name=finfo.name,
                link=finfo.linkname,
            ))
        elif finfo.islnk() and _te_badlink(finfo, base):
            _logger.warn("{name} is blocked: invalid symlink to {link}".format(
                name=finfo.name,
                link=finfo.linkname,
            ))
        else:
            yield finfo
            
class Database(object):
    def __init__(self):
        #CAUTION: This assumes the system will be initialised in a serial fashion
        db_exists = False
        if not os.path.exists(config.TASK_DATABASE):
            self._setup_db()
            
    def _setup_db(self):
        _logger.warn("Initialising database...")
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""CREATE TABLE instructions(
                id INTEGER PRIMARY KEY,
                deletion_flag BOOLEAN DEFAULT FALSE,
                retry BOOLEAN DEFAULT TRUE,
                date INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
                name TEXT
            )""")
            
            cursor.execute("""CREATE TABLE pending(
                instructions_id INTEGER NOT NULL,
                host TEXT NOT NULL,
                PRIMARY KEY(instructions_id, host),
                FOREIGN KEY(instructions_id) REFERENCES instructions(id) ON DELETE CASCADE
            ) WITHOUT ROWID""")
            
            cursor.execute("""CREATE TABLE instructions_single(
                id INTEGER PRIMARY KEY,
                deletion_flag BOOLEAN DEFAULT FALSE,
                retry BOOLEAN DEFAULT TRUE,
                date INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
                name TEXT,
                host TEXT NOT NULL
            ) WITHOUT ROWID""")
            
    def _remove_files(self, instructions_type, task_id):
        file_path = os.path.join(config.TASK_FILEPATH, instructions_type, str(task_id))
        if os.path.exists(file_path):
            _logger.debug("Removing {path}...".format(
                path=file_path,
            ))
            try:
                shutil.rmtree(file_path)
            except Exception as e:
                _logger.error("Unable to remove {path}: {error}".format(
                    path=file_path,
                    error=e,
                ))
                raise
                
    def _install_files(self, instructions_type, task_id, instructions, files=None, roles=None):
        base_path = os.path.join(config.TASK_FILEPATH, instructions_type, str(task_id))
        _logger.debug("Installing instructions in {path}...".format(
            path=file_path,
        ))
        try:
            os.makedirs(base_path)
        except Exception as e:
            _logger.error("Unable to create {path}: {error}".format(
                path=base_path,
                error=e,
            ))
            raise
            
        try:
            with open(os.path.join(base_path, 'playbook.yml'), 'wb') as playbook:
                playbook.write(instructions)
                
            if files:
                file_path = os.path.join(base_path, 'data')
                _logger.debug("Installing data in {path}...".format(
                    path=file_path,
                ))
                os.makedirs(file_path)
                for (filename, data) in files:
                    with open(os.path.join(file_path, filename), 'wb') as output:
                        output.write(data)
                        
            if roles:
                roles_path = os.path.join(base_path, 'roles')
                _logger.debug("Installing roles in {path}...".format(
                    path=roles_path,
                ))
                os.makedirs(roles_path)
                for (filename, data) in roles:
                    roles_archive = tarfile.open(mode='r:gz', fileobj=io.StringIO(data))
                    try:
                        roles_archive.extractall(path=roles_path, members=_te_safemembers(roles_archive))
                    finally:
                        roles_archive.close()
        except Exception as e:
            _logger.error("Unable to prepare files under {path}: {error}".format(
                path=base_path,
                error=e,
            ))
            try:
                self._remove_files(instructions_type, task_id)
            except Exception as ex: #Can't do anything about this one
                _logger.warn("Unable to clean up temporary files under {path}: {error}".format(
                    path=base_path,
                    error=ex,
                ))
            raise
            
    def install_instructions(self, instructions, hosts, retry=True, name=None, files=None, roles=None):
        _logger.info("Installing instructions for {count} hosts...".format(
            count=len(hosts),
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON""")
            
            cursor.execute("""INSERT INTO instructions(
                retry,
                name
            ) VALUES (
                :retry,
                :name
            )""", {
                'retry': retry,
                'name': name,
            })
            row_id = cursor.lastrowid
            
            cursor.executemany("""INSERT INTO pending(
                instructions_id,
                host
            ) VALUES (
                :instructions_id,
                :host
            )""", ({
                'instructions_id': row_id,
                'host': host,
            } for host in hosts))
            
            self._install_files('multi', row_id, instructions, files=files, roles=roles)
        return row_id
        
    def install_instructions_single(self, instructions, host, retry=True, name=None, files=None, roles=None):
        _logger.info("Installing instructions for {host}...".format(
            host=host,
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""INSERT INTO instructions_single(
                retry,
                name,
                host
            ) VALUES (
                :retry,
                :name,
                :host
            )""", {
                'retry': retry,
                'name': name,
                'host': host,
            })
            
            self._install_files('multi', cursor.lastrowid, instructions, files=files, roles=roles)
            return cursor.lastrowid
            
    def retrieve_instructions_details(self, instructions_id):
        _logger.info("Retrieving instructions for {id}...".format(
            id=instructions_id,
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT deletion_flag, retry, date, name FROM
                instructions
            WHERE
                id = :instructions_id
            LIMIT 1""", {
                'instructions_id': instructions_id,
            })
            result = cursor.fetchone()
            if result is None:
                return None
                
            (deletion_flag, retry, date, name) = result
            if deletion_flag:
                self.delete_instructions(instructions_id)
                return None
                
            cursor.execute("""SELECT host FROM
                pending
            WHERE
                instructions_id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            hosts = [i[0] for i in cursor.fetchall()]
        return (retry, date, name, hosts)
        
    def retrieve_instructions_details_single(self, instructions_id):
        _logger.info("Retrieving instructions for {id}...".format(
            id=instructions_id,
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT deletion_flag, retry, date, name, host FROM
                instructions_single
            WHERE
                id = :instructions_id
            LIMIT 1""", {
                'instructions_id': instructions_id,
            })
            record = cursor.fetchone()
            if not record:
                return None
                
            (deletion_flag, retry, date, name) = record
            if deletion_flag:
                self.delete_instructions_single(instructions_id)
                return None
            return (retry, date, name)
            
    def enumerate_instructions(self):
        _logger.info("Enumerating instruction IDs...")
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT id FROM
                instructions
            ORDER BY
                date ASC
            """)
            return collections.deque(i[0] for i in cursor.fetchall())
            
    def enumerate_instructions_single(self):
        _logger.info("Enumerating single instruction IDs...")
        tasks = collections.defaultdict(list)
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT id, host FROM
                instructions_single
            ORDER BY
                date ASC
            """)
            for (instructions_id, host) in cursor.fetchall():
                tasks[host].append(instructions_id)
        return tasks
        
    def clear_succeeded(self, instructions_id, hosts):
        _logger.info("Clearing {count} hosts for instructions {id}...".format(
            count=len(hosts),
            id=instructions_id,
        ))
        if not hosts:
            return
        args = [instructions_id]
        args.extend(hosts)
        
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""DELETE FROM
                pending
            WHERE
                instructions_id = ?
            AND
                host IN ({hosts_list})
            """.format(hosts_list=','.join('?' for i in range(len(hosts)))), args)
            
            #See if any hosts are outstanding
            cursor.execute("""SELECT COUNT(host) FROM
                pending
            WHERE
                instructions_id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            count = cursor.fetchone()[0]
            
        if count == 0:
            self.delete_instructions(instructions_id)
            
    def delete_instructions(self, instructions_id):
        _logger.info("Clearing instructions {id}...".format(
            id=instructions_id,
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""PRAGMA foreign_keys = ON""")
            
            cursor.execute("""DELETE FROM
                instructions
            WHERE
                id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            
            self._remove_files('multi', instructions_id)
            
    def delete_instructions_single(self, instructions_id):
        _logger.info("Clearing instructions {id}...".format(
            id=instructions_id,
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""DELETE FROM
                instructions_single
            WHERE
                id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            
            self._remove_files('single', instructions_id)
            
    def cull_instructions(self, instructions_id):
        _logger.info("Marking instructions {id} for removal...".format(
            id=instructions_id
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE
                instructions
            SET
                deletion_flag = TRUE
            WHERE
                id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            
    def cull_instructions_single(self, instructions_id):
        _logger.info("Marking instructions {id} for removal...".format(
            id=instructions_id
        ))
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE
                instructions_single
            SET
                deletion_flag = TRUE
            WHERE
                id = :instructions_id
            """, {
                'instructions_id': instructions_id,
            })
            
    def remove_host(self, host):
        _logger.info("Clearing instructions for {host}...".format(
            host=host,
        ))
        
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            #Remove multi-target references
            
            #While counting the number of other hosts waiting on an instruction
            #seems like an obvious way to tackle this problem, it's open to
            #test-before-set race conditions since each transaction will see all
            #items. It's necessary to record every affected ID and free them
            #afterwards, if necessary.
            cursor.execute("""SELECT instructions_id FROM
                pending
            WHERE
                host = :host
            """, {
                'host': host,
            })
            affected_instructions = [i[0] for i in cursor.fetchall()]
            
            if affected_instructions:
                cursor.execute("""DELETE FROM
                    pending
                WHERE
                    host = :host
                """, {
                    'host': host,
                })
        #End the transaction so that cleanup can occur after the last
        #transaction has terminated, in case of parallel decommissioning
        
        if affected_instructions:
            #Clean up any finished instructions
            for instructions_id in affected_instructions:
                with sqlite3.connect(config.TASK_DATABASE) as connection:
                    cursor = connection.cursor()
                    
                    cursor.execute("""SELECT COUNT(host) FROM
                        pending
                    WHERE
                        instructions_id = :instructions_id
                    """, {
                        'instructions_id': instructions_id,
                    })
                    count = cursor.fetchone()[0]
                    
                if count == 0:
                    self.delete_instructions(instructions_id)
                    
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT id FROM
                instructions_single
            WHERE
                host = :host
            """, {
                'host': host,
            })
            affected_instructions = [i[0] for i in cursor.fetchall()]
            
        for instructions_id in affected_instructions:
            self.delete_instructions_single(instructions_id)
            
    def list_instructions(self):
        _logger.info("Summarising all instructions...")
        
        multi_tasks = []
        single_tasks = []
        with sqlite3.connect(config.TASK_DATABASE) as connection:
            cursor = connection.cursor()
            
            cursor.execute("""SELECT i.date, i.name, i.id, i.retry, i.deletion_flag, p.host FROM
                instructions i,
                pending p
            WHERE i.id = p.instructions_id
            ORDER BY i.date ASC, i.id ASC, p.host ASC""")
            task = None
            task_id = None
            for (date, name, instructions_id, retry, deletion_flag, host) in cursor.fetchall():
                if task_id != instructions_id:
                    if task:
                        multi_tasks.append(task)
                    task = {
                        'date': date,
                        'name': name,
                        'instructions_id': instructions_id,
                        'hosts': [],
                        'retry': retry,
                        'cull': deletion_flag,
                    }
                task['hosts'].append(host)
            if task:
                multi_tasks.append(task)
                
            cursor.execute("""SELECT date, name, id, retry, deletion_flag, host FROM
                instructions_single
            ORDER BY date ASC, id ASC
            """)
            for (date, name, instructions_id, retry, deletion_flag, host) in cursor.fetchall():
                single_tasks.append({
                    'date': date,
                    'name': name,
                    'instructions_id': instructions_id,
                    'host': host,
                    'retry': retry,
                    'cull': deletion_flag,
                })
                
        return (multi_tasks, single_tasks)
        
