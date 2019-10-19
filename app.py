from typing import List, Dict

from server import Server

server = Server()


@server.route('users')
def users() -> List[Dict[str, str]]:
    return [{'username': 'NRiver'}, {'username': 'Potato'}]


@server.route('posts')
def posts() -> List[Dict[str, str]]:
    return [{'title': 'Potato Title'}, {'title': 'Cenoura Title'}]


server.run()
