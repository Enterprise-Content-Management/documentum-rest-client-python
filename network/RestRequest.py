from model import Resource
import requests
import base64

__author__ = 'wangc31'


HTTP_VERBS = ['delete', 'get', 'head', 'options', 'patch', 'post', 'put',
              'trace']

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204

HTTP_HEADER_ACCEPT = 'accept'
HTTP_HEADER_CONTENT_TYPE = 'content-type'


class RestRequest:
    def __init__(self, href):
        self.href = href
        self.verb = None
        self.user = None
        self.pwd = None

        self.params = None
        self.data = None
        self.files = None

        self.accept_type = None
        self.content_type = None

    def __call__(self, data=None, files=None, params=None):
        self.data = data
        self.files = files
        self.params = params
        return self.request()

    def auth(self, user, pwd):
        self.user = user
        self.pwd = pwd
        return self

    def accept(self, media_type):
        self.accept_type = media_type
        return self

    def as_(self, media_type):
        self.content_type = media_type
        return self

    def __getattr__(self, name):
        if self._is_verb(name):
            self.verb = name
            return self
        else:
            raise AttributeError(name)

    def prepare_headers(self):
        headers = self.get_basic_authen_header()

        if hasattr(self, 'content_type'):
            headers.update(self.get_content_header())

        if hasattr(self, 'accept_type'):
            headers.update(self.get_accept_header())
        return headers

    def request(self):
        print('Run method %s for URI %s' % (self.verb, self.href))
        headers = self.prepare_headers()

        if self.__is_multipart_request():
            rsp = requests.request(self.verb, self.href, headers=headers, params=self.params, files=self.files)
        else:
            rsp = requests.request(self.verb, self.href, headers=headers, params=self.params, data=self.data)

        self.check_return_code(rsp)
        return RestResponse(rsp)

    def get_basic_authen_header(self):
        if not self.user or not self.pwd:
            raise ValueError('login name or password is invalid.')

        encoded_credential = base64.b64encode((self.user + ":" + self.pwd).encode("utf-8"))
        return {"Authorization": "Basic " + encoded_credential.decode("utf-8")}

    def get_content_header(self):
        if self.__empty_content_type_if_multipart():
            return {}

        if hasattr(self, 'content_type'):
            return {HTTP_HEADER_CONTENT_TYPE: self.content_type}

        return {}

    def __empty_content_type_if_multipart(self):
        return self.__is_multipart_request()

    def __is_multipart_request(self):
        if self.files:
            return True
        else:
            return False

    def get_accept_header(self):
        return {HTTP_HEADER_ACCEPT: self.accept_type}

    @staticmethod
    def _is_verb(name):
        return name in HTTP_VERBS

    def check_return_code(self, response):
        code = response.status_code
        print('Status code: ' + str(code))

        if self.verb == 'get' and not code == HTTP_STATUS_OK:
            self._dump_error_info()
            raise Exception(response.content)

        if self.verb == 'post' and not code == HTTP_STATUS_OK and not code == HTTP_STATUS_CREATED:
            self._dump_error_info()
            raise Exception(response.content)

        if self.verb == 'delete' and not code == HTTP_STATUS_NO_CONTENT:
            self._dump_error_info()
            raise Exception(response.content)

        print('Succeed\n')

    def _dump_error_info(self):
        print('Exception caught during %s for link %s' % (self.verb, self.href))


class RestResponse:
    def __init__(self, response):
        self.response = response

    def resource(self):
        if len(self.response.content) is not 0:
            resource = Resource.Resource(self.response.json())
            return resource
        else:
            return None

    def status(self):
        return self.response.status_code
