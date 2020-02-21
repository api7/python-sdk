# Python SDK for Apache APISIX

### Synopsis
```python

from apisix import A6Client

client = A6Client('http://apisix.iresty.com')

upstream_id = 1
ok = client.new_upstream(upstream_id = upstream_id, type = 'roundrobin',
                         nodes = {"127.0.0.1:80": 1, "127.0.0.2:80": 2, "foo.com:80": 0}
                        )

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


