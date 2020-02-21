# -*- coding: utf-8 -*-
import os
import sys
import random
import unittest

curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, curpath)

from apisix import A6Client

HOST = os.getenv('HOST')
# USER_NAME = os.getenv('USER_NAME')
# PASSWORD = os.getenv('PASSWORD')
random.seed()


class TestAPISIX(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = A6Client(HOST)

    def test_route(self):
        route_id = 1
        ok = self.client.new_route(route_id = route_id, uris = ['/test.html'], plugins = [])
        self.assertEqual(ok, route_id)

        data = self.client.get_route(route_id)
        self.assertEqual(data['key'], '/apisix/routes/' + str(route_id))
        self.assertEqual(data['value']['uris'], ['/test.html'])
        self.assertEqual(data['value']['plugins'], {})

        ok = self.client.update_route(route_id = route_id,
                                      uris = ['/test.html'],
                                      hosts = ['foo.com', '*.bar.com'],
                                      plugins = {
                                          'limit-count': {
                                              'count': 2,
                                              'time_window': 60,
                                              'rejected_code': 503,
                                              'key': 'remote_addr'
                                          },
                                          'prometheus': {}
                                      }
                                      )
        self.assertEqual(ok, route_id)

        data = self.client.get_route(route_id)
        self.assertEqual(data['key'], '/apisix/routes/' + str(route_id))
        self.assertEqual(data['value']['uris'], ['/test.html'])
        self.assertEqual(data['value']['hosts'], ['foo.com', '*.bar.com'])
        self.assertEqual(data['value']['plugins']['limit-count']['time_window'], 60)
        self.assertEqual(data['value']['plugins']['prometheus'], {})

        ok = self.client.del_route(route_id)
        self.assertTrue(ok)

        data = self.client.get_route(route_id)
        self.assertEqual(data, None)

    def test_upstream(self):
        upstream_id = 1
        ok = self.client.new_upstream(upstream_id = upstream_id, type = 'roundrobin',
                                      nodes = {"127.0.0.1:80": 1, "127.0.0.2:80": 2, "foo.com:80": 0}
                                      )
        self.assertEqual(ok, upstream_id)

        data = self.client.get_upstream(upstream_id = upstream_id)
        self.assertEqual(data['value']['type'], 'roundrobin')
        self.assertEqual(data['value']['nodes']['127.0.0.1:80'], 1)
        self.assertEqual(data['value']['nodes']['foo.com:80'], 0)

        ok = self.client.update_upstream(upstream_id = upstream_id,
                                         type = 'roundrobin',
                                         nodes = {"127.0.0.1:8000": 1, "127.0.0.2:80": 1, "foo.com:80": 1}
                                         )
        self.assertTrue(ok)

        data = self.client.get_upstream(upstream_id = upstream_id)
        self.assertEqual(data['value']['type'], 'roundrobin')
        self.assertEqual(data['value']['nodes']['127.0.0.1:8000'], 1)
        self.assertEqual(data['value']['nodes']['foo.com:80'], 1)

        ok = self.client.update_upstream(upstream_id = upstream_id,
                                         type = 'chash',
                                         key = 'remote_addr',
                                         nodes = {"127.0.0.1:8000": 1, "foo.com:80": 1}
                                         )
        self.assertTrue(ok)

        data = self.client.get_upstream(upstream_id)
        self.assertEqual(data['value']['type'], 'chash')
        self.assertEqual(data['value']['nodes']['127.0.0.1:8000'], 1)
        self.assertEqual(data['value']['nodes']['foo.com:80'], 1)

        ok = self.client.update_upstream(upstream_id = upstream_id,
                                         type = 'chash',
                                         key = 'remote_addr',
                                         nodes = {"127.0.0.1:8000": 1, "foo.com:80": 1},
                                         checks = {
                                             "active": {
                                                 "http_path": "/status",
                                                 "host": "foo.com",
                                                 "healthy": {
                                                     "interval": 2,
                                                     "successes": 1
                                                 },
                                                 "unhealthy": {
                                                     "interval": 1,
                                                     "http_failures": 2
                                                 }
                                             }
                                         })
        self.assertTrue(ok)

        data = self.client.get_upstream(upstream_id)
        self.assertEqual(data['value']['type'], 'chash')
        self.assertEqual(data['value']['nodes']['127.0.0.1:8000'], 1)
        self.assertEqual(data['value']['nodes']['foo.com:80'], 1)
        self.assertEqual(data['value']['checks']['active']['http_path'], '/status')

        ok = self.client.del_upstream(upstream_id)
        self.assertTrue(ok)

        data = self.client.get_upstream(upstream_id)
        self.assertEqual(data, None)

    def test_upstream_id(self):
        upstream_id = 2
        ok = self.client.new_upstream(upstream_id = upstream_id, type = 'roundrobin',
                                      nodes = {"127.0.0.1:80": 1, "127.0.0.2:80": 2, "foo.com:80": 0}
                                      )
        self.assertEqual(ok, upstream_id)

        route_id = 2
        ok = self.client.new_route(route_id = route_id, uris = ['/test.html'], upstream_id = upstream_id)
        self.assertEqual(ok, route_id)

        data = self.client.get_route(route_id)
        self.assertEqual(data['key'], '/apisix/routes/' + str(route_id))
        self.assertEqual(data['value']['upstream_id'], upstream_id)

        ok = self.client.del_route(route_id)
        self.assertTrue(ok)

        data = self.client.get_route(route_id)
        self.assertEqual(data, None)

        ok = self.client.del_upstream(upstream_id)
        self.assertTrue(ok)

        data = self.client.get_upstream(upstream_id)
        self.assertEqual(data, None)
