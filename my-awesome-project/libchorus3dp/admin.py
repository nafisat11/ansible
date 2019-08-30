from . import db
from . import execute
from . import web_common

class PauseExecutionHandler(web_common.JSONHandler):
    def post(self):
        execute.EXECUTOR.pause()
        
class RestartExecutionHandler(web_common.JSONHandler):
    def post(self):
        execute.EXECUTOR.restart()
        
class ListInstructionsHandler(web_common.JSONHandler):
    def post(self):
        (multi_tasks, single_tasks) = db.Database().list_instructions()
        self.write({
            'single': single_tasks,
            'multi': multi_tasks,
        })
        
class RemoveInstructionsHandler(web_common.JSONHandler):
    def post(self):
        db.Database().cull_instructions(self._body['instructions_id'])
        
class RemoveSingleInstructionsHandler(web_common.JSONHandler):
    def post(self):
        db.Database().cull_instructions_single(self._body['instructions_id'])
        
class RemoveHostHandler(web_common.JSONHandler):
    def post(self):
        db.Database().remove_host(self._body['host'])
        
