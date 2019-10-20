import json
import re
from typing import List, Tuple, Callable
from http.server import HTTPServer, SimpleHTTPRequestHandler

from simple_http.colors import red, green


class Server:
    def __init__(self, port: int = 8000, host: str = 'localhost'):
        self.routes: List[Tuple[str, Callable]] = []
        self.port = port
        self.host = host

    def add_route(self, route: Tuple[str, Callable]):
        """
        Adds a route to the Server's list of routes
        """
        self.routes.append(route)

    def route(self, path: str) -> Callable:
        """
        Decorator to add an API route, used like so::
            @server.route('users')
            def get_users():
                return [{'username': 'John', id: 4}, {'username': 'Davis', id: 2}]
        """
        def decorator(callback: Callable) -> Tuple[str, Callable]:
            result = (path, callback)
            self.add_route(result)
            return result

        return decorator

    def run(self):
        """
        Run the HTTP Server
        """
        production_warning = (
            'This HTTP Server is not suitable for Production. As noted on the official http.server Python Docs.\n'
            'Read more at: https://docs.python.org/3/library/http.server.html\n'
        )
        print(f'{red("Warning: ")}\033[0m{production_warning}')

        class RequestHandler(SimpleHTTPRequestHandler):
            def set_headers(handler_self, code: int, content_type: str = 'application/json'):
                """
                Sends response code and Content-type headers
                """
                handler_self.send_response(code)
                handler_self.send_header('Content-type', content_type)
                handler_self.end_headers()

            def do_GET(handler_self):
                """
                Method run on every GET Request to the Server
                """
                for route_path, callback in self.routes:
                    route_pattern = fr'^\/?{route_path}'

                    # Route callback type hinting
                    arg_list = list(callback.__annotations__.items())

                    for arg_name, arg_type in arg_list:
                        if arg_name == 'return':
                            # Ignore callback return type hints
                            continue
                        # Look for the arguments in the current path using the route callback type hints
                        if arg_type is int:
                            route_pattern += r'/(\d+)'
                        elif arg_type is str:
                            route_pattern += r'/(\w+)'
                        elif arg_type is bool:
                            route_pattern += r'/(false|true|False|True)'

                    # Accept trailing '/' if it exists
                    route_pattern += r'\/?$'

                    # Check if current path matches any of the defined routes,
                    # and if it does, return the result function for that route
                    match = re.match(route_pattern, handler_self.path)

                    if match:
                        args = match.groups()
                        kwargs = {}

                        # Map URL arguments into kwargs, casting them to its appropriate type
                        for i, arg in enumerate(args):
                            arg_name, arg_type = arg_list[i]
                            arg_value = arg_type(arg)
                            kwargs[arg_name] = arg_value

                        try:
                            data = callback(**kwargs) if kwargs else callback()
                        except Exception as e:
                            # Return Exception as error message in case any Exception is thrown
                            # when running the route's callback
                            handler_self.set_headers(500)
                            return handler_self.wfile.write(json.dumps({'error': str(e)}).encode())

                        handler_self.set_headers(200)
                        return handler_self.wfile.write(json.dumps(data).encode())

                handler_self.set_headers(404)
                return handler_self.wfile.write(json.dumps({'error': f'Path not found: {handler_self.path}'}).encode())

        server_address = (self.host, self.port)
        httpd = HTTPServer(server_address, RequestHandler)

        host, port = httpd.server_address
        print(f'{green("Running HTTP server at: ")}http://{host}:{port}')

        httpd.serve_forever()
