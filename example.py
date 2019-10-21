from typing import List, TypedDict

from simple_http.server import Server
from simple_http.errors import HttpErrorNotFound404

server = Server()


class User(TypedDict):
    username: str


class Post(TypedDict):
    title: str


user_list: List[User] = [{'username': 'NRiver'}, {'username': 'Potato'}]

post_list: List[Post] = [{'title': 'Potato Title'}, {'title': 'Cenoura Title'}]


@server.route('users')
def users() -> List[User]:
    return user_list


@server.route('users')
def user(_id: int) -> User:
    try:
        return user_list[_id]
    except IndexError:
        raise HttpErrorNotFound404('User not found.')


@server.route('posts')
def posts() -> List[Post]:
    return post_list


@server.route('post')
def post(_id: int) -> Post:
    try:
        return post_list[_id]
    except IndexError:
        raise HttpErrorNotFound404('Post not found.')


server.run()
