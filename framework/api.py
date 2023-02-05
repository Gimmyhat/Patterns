from parse import parse
from webob import Request, Response


def default_response(response):
    response.status_code = 404
    response.text = "Not found"


def prepare_path(path):
    if not path.endswith('/'):
        return f'{path}/'
    return path


class API:

    def __init__(self):
        self.routes = {}

    # наполняем словарь routes элементами для передачи контроллерам
    # отработка паттерна front controller
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            handler(request, response, **kwargs)
        else:
            default_response(response)
        return response

    # находим нужный контроллер
    # отработка паттерна page controller
    def find_handler(self, request_path):
        request_path = prepare_path(request_path)

        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
