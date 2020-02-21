"""Tests for `tornado_resource_handler` package."""

import pytest
from .utils import request
import tornado

from tornado_resource_handler import tornado_resource_handler

pytestmark = pytest.mark.asyncio


async def test_index(app):
    response = await request('/books')
    assert response.code == 200
    assert response.body == b'Page of book list'


async def test_index_with_prefix(app):
    response = await request('/api/v1/books')
    assert response.code == 200
    assert response.body == b'Page of book list'


async def test_edit(app):
    response = await request('/books/10/edit')
    assert response.code == 200
    assert response.body == b'Page of editing book 10'


async def test_edit_with_prefix(app):
    response = await request('/api/v1/books/10/edit')
    assert response.code == 200
    assert response.body == b'Page of editing book 10'


async def test_show(app):
    response = await request('/books/10')
    assert response.code == 200
    assert response.body == b'Page of book 10 details'


async def test_new(app):
    response = await request('/books/new')
    assert response.code == 200
    assert response.body == b'Page of create new book'


async def test_create(app):
    response = await request('/books', method='POST', data={'name': 'Python Cookbook'})
    assert response.code == 200
    assert response.body == b'Create new book with name Python Cookbook'


async def test_update(app):
    response = await request('/books/10', method='PATCH', data={'name': 'Machine Learning'})
    assert response.code == 200
    assert response.body == b'Update book 10 with name Machine Learning'


async def test_destroy(app):
    response = await request('/books/10', method='DELETE')
    assert response.code == 200
    assert response.body == b'Delete book 10'


async def test_nested_index(app):
    response = await request('/books/10/reviews')
    assert response.code == 200
    assert response.body == b'Page of review list of book 10'


async def test_nested_create_without_token(app):
    with pytest.raises(tornado.httpclient.HTTPClientError) as excinfo:
        response = await request('/books/10/reviews', 'POST', {})
    assert excinfo.value.code == 401


async def test_nested_create_with_token(app):
    response = await request('/books/10/reviews', 'POST', {}, {'Token': 'secret_token'})
    assert response.code == 200
    assert response.body == b'Create review of book 10'


async def test_undefined_action(app):
    with pytest.raises(tornado.httpclient.HTTPClientError) as excinfo:
        await request('/books/10/reviews', 'PATCH', {}, {'Token': 'secret_token'})
    assert excinfo.value.code == 405
