# Simple HTTP Server

A toy HTTP Server Library with **no dependencies** and [unit tests](tests) that wraps the [`http.server`](https://docs.python.org/3/library/http.server.html) module from Python's Standard Library (**Not Suitable for Production**)

Heavily inspired by the [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Django](https://www.djangoproject.com/) Web Frameworks

---

## Installation:

* Not available yet

---

## Usage:

- Example app: [`example.py`](example.py)

##### Server Setup

  ```python
  # app.py

  from simple_http.server import Server

  server = Server(port=8000)
  server.run()
  ```

  * Run with `python app.py`
    * By default server will run at `http://localhost:8000`

---

##### Registering Routes

```python
# http://localhost:8000/users

@server.route('users')
def users() -> List[User]:
    return  [{'username': 'NRiver'}, {'username': 'Potato'}]
```

---

##### Routes with Arguments Typing inferred by Type Annotations

```python
# http://localhost:8000/users/<id:int>

@server.route('users')
def user(_id: int) -> User:
    # _id is already cast to int
    return user_list[_id]
```

* `curl http://localhost:8000/users/1`
    * Returns `200` Success
    ```json
    {"username": "Potato"}
    ```

---

##### Raising HTTP Errors
```python
from simple_http.errors import HttpErrorNotFound404

user_list = [{'username': 'NRiver'}, {'username': 'Potato'}]

@server.route('users')
def user(_id: int) -> User:
    try:
        return user_list[_id]
    except IndexError:
        # Raise HTTP Errors
        HttpErrorNotFound404('User not found.')
```

* `curl http://localhost:8000/users/4`
    * Returns `404` Not Found (no user at index `4`)
    ```json
    {"error": "User not found."}
    ```
* `curl http://localhost:8000/users/1`
    * Returns `200` Success
    ```json
    {"username": "Potato"}
    ```
* `curl http://localhost:8000/users/asdaasd`
    * Returns `404` Not Found (wrong type for `_id`)
    ```json
    {"error": "Path not found: /users/asdaasd"}
    ```
