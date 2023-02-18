import inspect
import urllib.parse

from parse import parse
from requests import Session as RequestsSession
from webob import Request, Response
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


def default_response(response):
    response.status_code = 404
    response.text = "Not found"


def prepare_path(path):
    # декодирование url с кириллицей
    path = urllib.parse.unquote(path)
    # добавление закрывающего слеша
    return path if path.endswith('/') else f'{path}/'


class API:

    def __init__(self):
        self._routes = {}

        # cached requests session
        self._session = None

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def add_route(self, path, handler):
        """Добавляет новый маршрут"""
        assert path not in self._routes, "Такой маршрут уже существует"

        self._routes[path] = handler

    def route(self, path):
        """Декоратор, добавляющий новый маршрут"""

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def find_handler(self, request_path):
        # request_path = prepare_path(request_path)

        for path, handler in self._routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method now allowed", request.method)

            handler(request, response, **kwargs)
        else:
            default_response(response)

        return response

    def session(self, base_url="http://testserver"):
        """Cached Testing HTTP client based on Requests by Kenneth Reitz."""
        if self._session is None:
            session = RequestsSession()
            session.mount(base_url, RequestsWSGIAdapter(self))
            self._session = session
        return self._session
