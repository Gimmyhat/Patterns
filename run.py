from wsgiref.simple_server import make_server

import routes
from variables import PORT

app = routes.app

if __name__ == '__main__':
    # для отладки
    with make_server('', PORT, app) as httpd:
        print(f"Запуск на порту {PORT}...")
        httpd.serve_forever()
