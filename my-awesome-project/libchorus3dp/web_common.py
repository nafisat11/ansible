import json

import tornado.web

class JSONHandler(tornado.web.RequestHandler):
    __body = None
    
    @property
    def _body(self):
        if not self.__body:
            self.__body = json.loads(self.get_argument('data'))
        return self.__body
        