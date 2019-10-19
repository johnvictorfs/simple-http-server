import json
import re
from typing import List, Tuple, Callable
from dataclasses import dataclass
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler


class Server:
    def __init__(self, port: int = 8000):
        self.routes: List[Tuple[str, Callable]] = []
        self.port = port

    def add_route(self, route: Tuple[str, Callable]):
        """
        Adds a route to the Server's list of routes
        """
        self.routes.append(route)

    def route(self, path: str):
        """
        Decorator to add an API route, used like so::
            @server.route('users')
            def get_users():
                return [{'username': 'John', id: 4}, {'username': 'Davis', id: 2}]
        """
        def decorator(callback: Callable):
            result = (path, callback: Callable)
            self.add_route(result)
            return result

        return decorator

    def run(self):
        """
        Run the API Server
        """
        class RequestHandler(SimpleHTTPRequestHandler):
            def do_GET(handler_self):
                """
                Method run on every GET Request to the Server
                """
                for route_path, callback in self.routes:
                    # Check if current path matches any of the defined routes,
                    # and if it does, return the result function for that route
                    if re.match(fr'^\/?{route_path}\/?$', handler_self.path):
                        handler_self.send_response(200)
                        handler_self.end_headers()
                        return handler_self.wfile.write(json.dumps(callback()).encode())

                return handler_self.send_error(404, f'Path not found: {handler_self.path}')

        server_address = ('', self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()
