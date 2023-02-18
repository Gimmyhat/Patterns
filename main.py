import datetime
from wsgiref.simple_server import make_server

from framework.api import API
from framework.template import render
from variables import PORT

app = API()


@app.route("/")
def home(request, response):
    response.text = render('index.html', data=datetime.date.today())


@app.route("/about/")
def about(request, response):
    response.text = render('about.html')


class BaseRoute:
    @staticmethod
    def get(request, response):
        response.json = dict(request.params)

    @staticmethod
    def post(request, response):
        response.json = dict(request.params)


@app.route("/contacts/")
class Contacts(BaseRoute):
    @staticmethod
    def get(request, response):
        response.text = render('contacts.html')

    @staticmethod
    def post(request, response):
        response.text = render('contacts-resp.html', data=dict(request.params))


if __name__ == '__main__':
    # для отладки
    with make_server('', PORT, app) as httpd:
        print(f"Запуск на порту {PORT}...")
        httpd.serve_forever()
