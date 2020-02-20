
# -*- coding: utf-8 -*-
import sys
import time
import warnings

import requests

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import urljoin

    def b(s):
        if isinstance(s, str):
            return s.encode('utf-8')
        return s
    str = str

else:
    from urlparse import urljoin

    def b(s):
        return s
    str = unicode


class A6Client(object):
    def __init__(self, host):
        if not host:
            raise Exception('no host arg specified')
        # if not username:
        #     raise Exception('no username arg specified')
        # if not password:
        #     raise Exception('no password arg specified')

        self.base_uri = urljoin(host, '/apisix/admin/')
        # self.username = username
        # self.password = password
        self.timeout = 30

        # self.__token = ''
        # self.__login_time = 0

    def do_api(self, method, path, body = None):
        # login_time = self.__login_time or 0
        # if not self.__token or time.time() - login_time >= 3600 - 60:
        #     self.login()

        # r = requests.request(method, urljoin(self.base_uri, path),
                            #  headers = {'Auth': self.__token},
                            #  json = body, timeout = self.timeout)
        r = requests.request(method, urljoin(self.base_uri, path),
                             json = body, timeout = self.timeout)

        # print(method)
        # print(body)
        # print(r.url)
        # print(r.text)
        # print(r.status_code)

        response = r.json()
        # print(response)
        if r.status_code >= 300:
            error_msg = response.get('error_msg', '') or response.get('message', '')
            warnings.warn('{} {} failed : status : {} : {}'.format(method, path, r.status_code, error_msg))
            return None

        return response['node']

    def set_login_time(self, login_time):
        self.__login_time = login_time

    def set_token(self, token):
        self.__token = token

    def get_token(self):
        return self.__token

    def login(self):
        r = requests.post(urljoin(self.base_uri, 'user/login'),
                          data = json.dumps({'username': self.username, 'password': self.password}),
                          timeout = self.timeout)
        response = r.json()
        status = response.get('status')
        if status != 0:
            err = response.get('msg', '')
            raise Exception("failed to login: " + err)

        data = response.get('data')
        if not data:
            raise Exception('failed to get data of response')

        token = data.get('token')
        if not token:
            return False

        self.set_login_time(time.time())
        self.set_token(token)

        return True

    def new_route(self, **kwargs):
        if not kwargs['uris']:
            raise Exception('no uris specified')

        http_verb = 'POST'
        url = 'routes/'
        route_id = kwargs['route_id']
        del kwargs['route_id']
        if route_id:
            http_verb = 'PUT'
            url = url + str(route_id)

        response = self.do_api(http_verb, url, kwargs)
        route_id = response['key'].split('/')[-1]

        return int(route_id)

    def get_route(self, route_id):
        if not route_id:
            raise Exception('no route_id specified')

        return self.do_api('GET', 'routes/' + str(route_id))

    def update_route(self, **kwargs):
        route_id = kwargs['route_id']
        if not route_id:
            raise Exception('no route_id specified')
        del kwargs['route_id']

        response = self.do_api('PUT', 'routes/' + str(route_id), kwargs)
        route_id = response['key'].split('/')[-1]

        return int(route_id)

    def del_route(self, route_id):
        if not route_id:
            raise Exception('no route_id specified')

        return self.do_api('DELETE', 'routes/' + str(route_id))

    def new_upstream(self, **kwargs):
        if not kwargs['type']:
            raise Exception('no type specified')
        if not kwargs['nodes']:
            raise Exception('no nodes specified')

        http_verb = 'POST'
        url = 'upstreams/'
        upstream_id = kwargs['upstream_id']
        del kwargs['upstream_id']
        if upstream_id:
            http_verb = 'PUT'
            url = url + str(upstream_id)

        response = self.do_api(http_verb, url, kwargs)
        upstream_id = response['key'].split('/')[-1]

        return int(upstream_id)

    def get_upstream(self, upstream_id):
        if not upstream_id:
            raise Exception('no upstream_id specified')

        return self.do_api('GET', 'upstreams/' + str(upstream_id))

    def update_upstream(self, **kwargs):
        upstream_id = kwargs['upstream_id']
        if not upstream_id:
            raise Exception('no upstream_id specified')
        del kwargs['upstream_id']

        response = self.do_api('PUT', 'upstreams/' + str(upstream_id), kwargs)
        upstream_id = response['key'].split('/')[-1]

        return int(upstream_id)

    def del_upstream(self, upstream_id):
        if not upstream_id:
            raise Exception('no upstream_id specified')

        return self.do_api('DELETE', 'upstreams/' + str(upstream_id))
