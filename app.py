from server import Server

server = Server()


@server.route('users')
def users():
    return [{'username': 'NRiver'}, {'username': 'Potato'}]


@server.route('posts')
def posts():
    return [{'title': 'Potato Title'}, {'title': 'Cenoura Title'}]


server.run()
