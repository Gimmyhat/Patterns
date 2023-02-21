from framework.api import API, DebugApplication, FakeApplication
from framework.template import render
from patterns.structural_patterns import Debug
from patterns.сreational_patterns import Engine, Logger

app = API()
site = Engine()
logger = Logger('main')


class Base:
    @staticmethod
    def get(request, response):
        ...

    @staticmethod
    def post(request, response):
        ...


# Main page

@app.route("/", methods=['get'])
@Debug(name='Index')
def home(request, response):
    response.text = render('index.html',
                           objects_list=site.root_categories)


# Category

@app.route("/create-category/")
class CreateCategory(Base):
    @staticmethod
    def get(request, response):
        response.text = render('create_category.html')

    @staticmethod
    @Debug(name='Create Category')
    def post(request, response):
        parent = None
        cat_id = request.params.get('id')
        if cat_id:
            parent = site.find_category_by_id(int(cat_id))
        name = request.params['name']
        new_category = site.create_category(name, parent=parent)
        logger.log(f'Создана категория "{name}"')
        response.text = render('index.html',
                               objects_list=site.root_categories,
                               id=cat_id)


@app.route('/category-list/')
class CategoryList(Base):
    @staticmethod
    def get(request, response):
        categories = site.get_category_tree(with_courses=True)
        count_courses = site.count_courses
        response.text = render('category_list.html',
                               categories=categories,
                               count_courses=count_courses)


# Courses


@app.route("/create-course/")
class CreateCourse(Base):

    @staticmethod
    def get(request, response):
        cat = site.find_category_by_id(int(request.params['id']))
        response.text = render('create_course.html',
                               id=cat.id,
                               name=cat.name)

    @staticmethod
    @Debug(name='Create Course')
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
class CoursesList(Base):
    @staticmethod
    def get(request, response):
        cat = site.find_category_by_id(int(request.params['id']))
        response.text = render('course_list.html',
                               id=cat.id,
                               name=cat.name,
                               objects_list=cat.courses)


@app.route(("/copy-course/"))
class CopyCourse(Base):

    @staticmethod
    def get(request, response):
        name = site.get_course(request.params['name'])
        old_course = name
        cat = None
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

@app.route("/about/", methods=['get'])
def about(request, response):
    response.text = render('about.html')


# Contacts

@app.route("/contacts/")
class Contacts(Base):
    @staticmethod
    def get(request, response):
        response.text = render('contacts.html')

    @staticmethod
    def post(request, response):
        response.text = render('contacts-resp.html',
                               data=dict(request.params))
