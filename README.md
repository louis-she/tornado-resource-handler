## Tornado Resource Handler

[![pypi](https://img.shields.io/pypi/v/tornado_resource_handler.svg)](https://pypi.python.org/pypi/tornado-resource-handler)
[![travis](https://travis-ci.com/louis-she/tornado-resource-handler.svg?branch=master)](https://travis-ci.com/louis-she/tornado-resource-handler)

Organize the handlers as resources, inspired from Ruby on Rails. The [mock handlers](./tests/mock_handlers.py) in the test is a live demo to see how to use the `ResourceHandler`.

### Installation

```
pip install tornado-resource-handler
```

### Basic Usage

Create a handler with the 7 actions like the controller of Ruby on Rails.


| HTTP Verb | Path             | Handler#Action | Used for                                       |
|-----------|------------------|----------------|------------------------------------------------|
| GET       | /photos          | photos#index   | display a list of all photos                   |
| GET       | /photos/new      | photos#new     | return an HTML form for creating a new photo   |
| POST      | /photos          | photos#create  | create a new photo                             |
| GET       | /photos/:id      | photos#show    | display a specific photo                       |
| GET       | /photos/:id/edit | photos#edit    | return an HTML form for editing a photo        |
| PATCH/PUT | /photos/:id      | photos#update  | update a specific photo                        |
| DELETE    | /photos/:id      | photos#destroy | delete a specific photo                        |

```Python
import tornado.ioloop
import tornado.web

from tornado_resource_handler import create_resource_handler

ResourceHandler = create_resource_handler()


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


def make_app():
    return tornado.web.Application([
      *BooksHandler.routes()
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

After start up the server, these routes become available:

```
GET    http://localhost:8888/books         # To list all the books
GET    http://localhost:8888/books/new     # To show the book creating page
POST   http://localhost:8888/books         # To create a book
GET    http://localhost:8888/books/1/edit  # To edit book(id: 1)
GET    http://localhost:8888/books/1/edit  # To show the editing page of book(id: 1)
PATCH  http://localhost:8888/books/1       # To update the book(id: 1)
DELETE http://localhost:8888/books/1       # To delete the book(id: 1)
```

> Take a closer look at the [mock handlers](./tests/mock_handlers.py) for more advanced usage.
