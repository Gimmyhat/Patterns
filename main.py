from wsgiref.simple_server import make_server

from framework.api import API
from framework.template import render
from variables import PORT

app = API()


@app.route("/")
def home(request, response):
    response.text = render('index.html')


@app.route("/about/")
def about(request, response):
    response.text = render('about.html')


@app.route("/hello/{name}/")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


if __name__ == '__main__':
    # для отладки
    with make_server('', PORT, app) as httpd:
        print(f"Запуск на порту {PORT}...")
        httpd.serve_forever()
