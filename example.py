from typing import List, TypedDict

from simple_http.server import Server

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


@server.route('users/<_id:int>')
def user(_id: int) -> User:
    return user_list[_id]


@server.route('posts')
def posts() -> List[Post]:
    return post_list


@server.route('post/<_id:int>')
def post(_id: int) -> Post:
    return post_list[_id]


server.run()
