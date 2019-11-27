from typing import List, Dict, Tuple, Any
import threading

import requests

from simple_http.server import Server
from simple_http.errors import HttpError

user_list = [{'username': 'John'}, {'username': 'Dave'}]


class TestApiRoutes:
    server: Server

    def setup_class(self):
        """Setup Test Server"""
        self.host = 'localhost'
        self.port = 8000
        self.server = Server(host=self.host, port=self.port)
        self.setup_routes(self.server)
        self.user_not_found = 'User not found.'

        # Run Test Server in another Thread as to not block tests
        thread = threading.Thread(target=self.server.run)
        thread.daemon = True
        thread.start()

    def teardown_class(self):
        """Shutdown Test Server"""
        self.server.close()

    @staticmethod
    def setup_routes(server: Server):
        """Setup Routes used for tests"""
        @server.route('users')
        def users() -> List[Dict[str, str]]:
            return user_list

        @server.route('users')
        def user(index: int) -> Dict[str, str]:
            try:
                return user_list[index]
            except IndexError:
                raise HttpError(404, 'User not found.')

        @server.route('server_error')
        def server_error() -> None:
            5 / 0

    @property
    def api_url(self):
        return f'http://{self.host}:{self.port}'

    def get(self, url: str) -> Tuple[requests.Response, Any]:
        """
        Makes a GET request to the Test Server and returns its Response and Json data, if available
        """
        request = requests.get(f'{self.api_url}/{url}')
        return request, request.json()

    def test_get_route_data(self):
        request, data = self.get('users')
        assert request.status_code == 200
        assert data == user_list
        assert data[0]['username'] == user_list[0]['username']

    def test_get_route_arguments(self):
        index = 1
        request, data = self.get(f'users/{index}')
        assert request.status_code == 200
        assert data == user_list[index]
        assert data['username'] == user_list[index]['username']

    def test_get_wrong_route_arguments(self):
        index = 4
        request, data = self.get(f'users/{index}')

        assert request.status_code == 404
        assert data['error'] == self.user_not_found

    def test_server_error(self):
        request, data = self.get('server_error')

        assert request.status_code == 500
        assert data['error'] == 'division by zero'
