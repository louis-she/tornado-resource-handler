import inspect
import tornado.ioloop
import tornado.web
import asyncio
from pytest import fixture
from .mock_handlers import (
    BooksHandler,
    BooksReviewHandler,
)

def make_app():
    routes = [
        *BooksHandler.routes(nested=[
            *BooksReviewHandler.routes(),
        ]),
        *BooksHandler.routes(prefix='/api/v1/')
    ]

    return tornado.web.Application(routes)


@fixture(scope='module')
def event_loop(request):
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    return event_loop


@fixture(scope='module')
def app(request, event_loop):
    """Mock a tornado app for testing"""
    app = make_app()
    app.listen(6666)

    return app
