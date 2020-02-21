import json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


async def request(path, method='GET', data=None, header=None):
    http_client = AsyncHTTPClient()

    request = HTTPRequest(
        url=f'http://localhost:6666{path}',
        method=method,
        body=None if data is None else json.dumps(data),
        headers=header
    )

    return await http_client.fetch(request)
