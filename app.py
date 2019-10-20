from typing import List, TypedDict

from server import Server

server = Server()


class User(TypedDict):
    username: str


class Post(TypedDict):
    title: str


@server.route('users')
def users() -> List[User]:
    return [{'username': 'NRiver'}, {'username': 'Potato'}]


@server.route('posts')
def posts() -> List[Post]:
    return [{'title': 'Potato Title'}, {'title': 'Cenoura Title'}]


server.run()
