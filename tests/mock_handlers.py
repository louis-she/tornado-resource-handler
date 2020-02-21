from tornado_resource_handler import ResourceHandler
from tornado.web import HTTPError
from tornado.escape import json_decode
from functools import wraps


class BooksHandler(ResourceHandler):

    def index(self):
        self.write("Page of book list")

    def edit(self, id):
        self.write(f'Page of editing book {id}')

    def show(self, id):
        self.write(f'Page of book {id} details')

    def new(self):
        self.write('Page of create new book')

    def create(self):
        data = json_decode(self.request.body)
        self.write(f'Create new book with name {data["name"]}')

    def update(self, id):
        data = json_decode(self.request.body)
        self.write(f'Update book {id} with name {data["name"]}')

    def destroy(self, id):
        self.write(f'Delete book {id}')


def authenticate_token(func):

    @wraps(func)
    def _decorator(self, *args, **kwargs):
        if self.request.headers.get('Token') != 'secret_token':
            raise HTTPError(status_code=401, log_message="Invalid Token")
        func(self, *args, **kwargs)

    return _decorator


class BooksReviewHandler(ResourceHandler):

    resource_name = 'reviews'

    def prepare(self):
        super().prepare()
        self.book_id = self.path_kwargs.get('parent_id')

    def index(self):
        self.write(f'Page of review list of book {self.book_id}')

    @authenticate_token
    def create(self):
        self.write(f'Create review of book {self.book_id}')


routes = [
    *BooksHandler.routes(nested=[
        *BooksReviewHandler.routes(),
    ]),
    *BooksHandler.routes(prefix='/api/v1/')
]
