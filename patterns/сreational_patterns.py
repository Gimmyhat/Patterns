from copy import deepcopy


# абстрактный пользователь
class User:
    pass


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# интерактивный курс
class InteractiveCourse(Course):
    pass


# курс в записи
class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
    auto_id = 0

    def __init__(self, name, parent=None):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.parent = parent
        self.children = []
        self.courses = []

        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        self.children.append(child)

    def course_count(self):
        count = len(self.courses)
        for child in self.children:
            count += child.course_count()
        return count


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.root_categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    def create_category(self, name, parent=None):
        category = Category(name, parent)
        if parent is None:
            self.root_categories.append(category)
        return category

    def find_category_by_id(self, id):
        for root in self.root_categories:
            category = self._find_category_by_id(id, root)
            if category is not None:
                return category
        raise Exception(f'Нет категории с id = {id}')

    def _find_category_by_id(self, id, category):
        if category.id == int(id):
            return category

        for child in category.children:
            subcategory = self._find_category_by_id(id, child)
            if subcategory is not None:
                return subcategory

        return None

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def add_category(self, category):
        self.root_categories.append(category)

    def add_course(self, course):
        self.courses.append(course)

    def get_category_tree(self, category=None, with_courses=False):
        if category is None:
            categories = self.root_categories
        else:
            categories = category.children

        category_list = []
        for cat in categories:
            cat_info = {'name': cat.name, 'id': cat.id}

            if with_courses and cat.courses:
                cat_info['courses'] = [course.name for course in cat.courses]

            subcategories = self.get_category_tree(cat, with_courses)
            if subcategories:
                cat_info['subcategories'] = subcategories

            category_list.append(cat_info)

        return category_list

    def count_courses(self, category):
        count = len(category.get('courses', []))
        for subcategory in category.get('subcategories', []):
            count += self.count_courses(subcategory)
        return count


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
