# Patterns
Architecture and design patterns in Python

Запускаем Waitress WSGI-сервер и проверяем, что simple_wsgi.py работает:
```sh
$ waitress-serve --listen=*:8000 simple_wsgi:application
```


Запуск фреймворка 
```sh
$ waitress-serve --listen=*:8000 main:app
```

http://127.0.0.1:8000