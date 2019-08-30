from . import db
from . import execute
from . import web_common

class LoadInstructionsHandler(web_common.JSONHandler):
    def post(self):
        instructions_id = db.Database().install_instructions(
            instructions=self._body['instructions'],
            hosts=self._body['hosts'],
            retry=self._body.get('retry', True),
            name=self._body.get('name'),
            files=((file_data['filename'], file_data['body']) for file_data in self.request.files.get('files', ())),
            roles=((role_data['filename'], role_data['body']) for role_data in self.request.files.get('roles', ())),
        )
        self.write({
            'id': instructions_id,
            'position': execute.EXECUTOR.load_instructions(),
        })
        
class LoadInstructionsSingleHandler(web_common.JSONHandler):
    def post(self):
        instructions_id = db.Database().install_instructions_single(
            instructions=self._body['instructions'],
            host=self._body['host'],
            retry=self._body.get('retry', True),
            name=self._body.get('name'),
            files=((file_data['filename'], file_data['body']) for file_data in self.request.files.get('files', ())),
            roles=((role_data['filename'], role_data['body']) for role_data in self.request.files.get('roles', ())),
        )
        execute.EXECUTOR.load_instructions()
        self.write({
            'id': instructions_id,
        })
        
