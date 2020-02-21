# Python SDK for Apache APISIX

More detailed documentation please refer to:
- https://github.com/apache/incubator-apisix/blob/master/doc/admin-api-cn.md

- https://github.com/apache/incubator-apisix/blob/master/doc/architecture-design-cn.md

### Synopsis
```python

from apisix import A6Client

client = A6Client('http://apisix.iresty.com')

# https://github.com/apache/incubator-apisix/blob/master/doc/architecture-design-cn.md#upstream
upstream_id = 1
ok = client.new_upstream(upstream_id = upstream_id, type = 'roundrobin',
                         nodes = {"127.0.0.1:80": 1, "127.0.0.2:80": 2, "foo.com:80": 0}
                        )

client.update_upstream(upstream_id = upstream_id,
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

# https://github.com/apache/incubator-apisix/blob/master/doc/admin-api-cn.md#route
route_id = 1
ok = self.client.new_route(route_id = route_id, uris = ['/test.html'], upstream_id = upstream_id)
```

### Prerequisites
You need to install `pip` first.

Then install packages as:
```
cd apache-apisix-python-sdk
make init
```

### Run test cases
```
cd apache-apisix-python-sdk
make clean test
```


