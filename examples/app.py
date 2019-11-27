from typing import List, TypedDict

from simple_http.server import Server
from simple_http.errors import HttpError

server = Server()


class User(TypedDict):
    username: str


class Post(TypedDict):
    title: str


user_list: List[User] = [{'username': 'NRiver'}, {'username': 'Potato'}]

post_list: List[Post] = [{'title': 'Potato Title'}, {'title': 'Cenoura Title'}]


@server.route('users')
def users() -> List[User]:
    """
    Get all Users
    """
    return user_list


@server.route('users')
def user(_id: int) -> User:
    """
    Get one User by _id (index)
    """
    try:
        return user_list[_id]
    except IndexError:
        raise HttpError(404, 'User not found.')


@server.route('posts')
def posts() -> List[Post]:
    """
    Get all posts
    """
    return post_list


@server.route('post')
def post(_id: int) -> Post:
    """
    Get one post by _id (index)
    """
    try:
        return post_list[_id]
    except IndexError:
        raise HttpError(404, 'Post not found.')


server.run()
