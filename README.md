# Simple HTTP Server

A toy HTTP Server with **no dependencies** made with [`http.server`](https://docs.python.org/3/library/http.server.html) module from Python's Standard Library (**Not Suitable for Production**)

Heavily inspired by [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Django](https://www.djangoproject.com/)

---

## Installation:

* Not available yet

---

## Examples:

- Example app: [`example.py`](example.py)

* Server Setup

  ```python
  # app.py

  from simple_http.server import Server

  server = Server(port=8000)
  server.run()
  ```

  * Run with `python app.py`
    * By default server will run at `http://localhost:8000`

---

* Registering Routes

```python
# http://localhost:8000/users

@server.route('users')
def users() -> List[User]:
    return [{'username': 'NRiver'}, {'username': 'Potato'}]
```

---

* Routes with Arguments Typing inferred by Type Annotations

```python
# http://localhost:8000/users/4
# http://localhost:8000/users/2
# http://localhost:8000/users/asdasd Fails

@server.route('users')
def user(_id: int) -> User:
    return user_list[_id]  # _id is cast to int already
```
