from framework.api import API
from framework.template import render
from patterns.сreational_patterns import Engine, Logger

app = API()
site = Engine()
logger = Logger('main')


class BaseRoute:
    @staticmethod
    def get(request, response):
        response.json = dict(request.params)

    @staticmethod
    def post(request, response):
        response.json = dict(request.params)


# Main page

@app.route("/")
def home(request, response):
    response.text = render('index.html',
                           objects_list=site.categories)


# Category

@app.route("/create-category/")
class CreateCategory(BaseRoute):
    @staticmethod
    def get(request, response):
        response.text = render('create_category.html')

    @staticmethod
    def post(request, response):
        name = request.params['name']
        category = None
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        logger.log(f'Создана категория "{name}"')
        response.text = render('index.html',
                               objects_list=site.categories)


# Courses


@app.route("/create-course/")
class CreateCourse(BaseRoute):

    @staticmethod
    def get(request, response):
        cat = site.find_category_by_id(int(request.params['id']))
        response.text = render('create_course.html',
                               id=cat.id,
                               name=cat.name)

    @staticmethod
    def post(request, response):
        name = request.params['name']
        cat = site.find_category_by_id(int(request.params['id']))
        course = site.create_course('record', name, cat)
        site.courses.append(course)
        logger.log(f'Создан курс "{name}"')
        response.text = render('course_list.html',
                               id=cat.id,
                               name=cat.name,
                               objects_list=cat.courses)


@app.route("/courses-list/")
class CoursesList(BaseRoute):
    @staticmethod
    def get(request, response):
        cat = site.find_category_by_id(int(request.params['id']))
        response.text = render('course_list.html',
                               id=cat.id,
                               name=cat.name,
                               objects_list=cat.courses)


@app.route(("/copy-course/"))
class CopyCourse(BaseRoute):

    @staticmethod
    def get(request, response):
        name = site.get_course(request.params['name'])
        old_course = name
        if old_course:
            new_name = f'copy_{old_course.name}'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)
            cat = site.find_category_by_id(new_course.category.id)
            cat.courses.append(new_course)
            logger.log(f'Создана копия курса "{old_course.name}"')
        response.text = render('course_list.html',
                               id=cat.id,
                               name=cat.name,
                               objects_list=cat.courses)


# About

@app.route("/about/")
def about(request, response):
    response.text = render('about.html')


# Contacts

@app.route("/contacts/")
class Contacts(BaseRoute):
    @staticmethod
    def get(request, response):
        response.text = render('contacts.html')

    @staticmethod
    def post(request, response):
        response.text = render('contacts-resp.html',
                               data=dict(request.params))
