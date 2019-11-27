# Simple HTTP Server

A toy HTTP Server Library with **no dependencies** and [unit tests](tests) that wraps the [`http.server`](https://docs.python.org/3/library/http.server.html) module from Python's Standard Library (**Not Suitable for Production**)

Inspired by the [Flask](https://flask.palletsprojects.com) and [FastAPI](https://fastapi.tiangolo.com) Web Frameworks

---

## Installation:

* Not available yet

---

## Usage:

- Example app: [`examples/app.py`](examples/app.py)

---

#### Basic Setup

  ```python
  # app.py

  from simple_http.server import Server

  server = Server(port=8000)
  server.run()
  ```

  * Run with `python app.py`
    * By default server will run at `http://localhost:8000`

---

#### Registering Routes

```python
# http://localhost:8000/users

@server.route('users')
def users() -> List[User]:
    return  [{'username': 'NRiver'}, {'username': 'Potato'}]
```

---

#### Routes with Arguments Typing inferred by Type Annotations

```python
# http://localhost:8000/users/<id:int>

@server.route('users')
def user(_id: int) -> User:
    # _id is already cast to int
    return user_list[_id]
```

* `curl http://localhost:8000/users/1` will return 200 Success
    ```json
    {"username": "Potato"}
    ```

---

#### Raising HTTP Errors

```python
from simple_http.errors import HttpError

user_list = [{'username': 'NRiver'}, {'username': 'Potato'}]

@server.route('users')
def user(_id: int) -> User:
    try:
        return user_list[_id]
    except IndexError:
        # Raise HTTP Error with Code 404
        raise HttpError(404, 'User not found.')
```

| URL                             | Response                                  | Code  | Reason                  |
| --------------------------------|:-----------------------------------------:|:-----:|:-----------------------:|
| http://localhost:8000/users/4   | `{"error": "User not found."}`            | 404   | No user with _id `4`    |
| http://localhost:8000/users/1   | `{"username": "Potato"}`                  | 200   | Found user with _id `1` |
| http://localhost:8000/users/asd | `{"error": "Path not found: /users/asd"}` | 404   | Wrong type for _id      |
