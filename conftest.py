import pytest
import requests
from datetime import date

from data.data_generator import DataGenerator
from clients.api_manager import ApiManager
from config.config import ADMIN_PASSWORD, ADMIN_LOGIN
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from api_models.base_models import TestUser, RegisterUserResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

@pytest.fixture
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def api_manager(session):
    return ApiManager(session)

@pytest.fixture
def params_get_movies():
    params = DataGenerator.generate_random_params_for_get_movies()
    return params

@pytest.fixture
def created_movies_data():
    body_movies = DataGenerator.generate_random_data_movies()
    return body_movies

@pytest.fixture
def update_movies_data():
    body_movies = DataGenerator.generate_random_data_movies()
    return body_movies

# @pytest.fixture
# def auth_with_admin_credentials(api_manager):
#     admin_credentials = (ADMIN_LOGIN, ADMIN_PASSWORD)
#     api_manager.auth_api.authenticate(admin_credentials)

@pytest.fixture
def created_movies(created_movies_data, super_admin):
    return super_admin.api.movies_api.create_movies(movies_data=created_movies_data)

@pytest.fixture
def created_movies_without_admin_creds(created_movies_data, common_user):
    return common_user.api.movies_api.create_movies(
        movies_data=created_movies_data,
        expected_status=403
    )

# @pytest.fixture
# def auth_without_admin_credentials(api_manager):
#     user_data = generate.generate_random_user_data()
#     email = user_data['email']
#     password = user_data['password']
#     api_manager.auth_api.register_user(user_data=user_data)
#     api_manager.auth_api.authenticate((email, password))

# @pytest.fixture
# def created_review_data():
#     review_data = generate.generate_random_review_data()
#     return review_data
#
# @pytest.fixture
# def created_review(api_manager, auth_with_admin_credentials, created_movies, created_review_data):
#     return api_manager.movies_api.create_movies_review(
#         id_movies=created_movies.json()["id"],
#         reviews_data=created_review_data
#     )
#
# @pytest.fixture
# def created_review_by_user(api_manager_with_role_user, created_movies, created_review_data, auth_without_admin_credentials):
#     return api_manager_with_role_user.movies_api.create_movies_review(
#         id_movies=created_movies.json()["id"],
#         reviews_data=created_review_data
#     )
#
# @pytest.fixture
# def creation_multiple_reviews(created_movies):
#     def creation_review():
#         session_in = requests.Session()
#         api = ApiManager(session_in)
#         user_data = generate.generate_random_user_data()
#         email = user_data['email']
#         password = user_data['password']
#
#         api.auth_api.register_user(user_data=user_data)
#         api.auth_api.authenticate((email,password))
#         review_data = generate.generate_random_review_data()
#         response = api.movies_api.create_movies_review(id_movies=created_movies.json()['id'], reviews_data=review_data)
#         return response
#     return creation_review

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

# @pytest.fixture(scope="function")
# def test_user():
#     password = generate.generate_random_password()
#     return {
#         "email": generate.generate_random_email(),
#         "fullName": generate.generate_random_full_name(),
#         "password": password,
#         "passwordRepeat": password,
#         "roles": [Roles.USER.value]
#     }

# @pytest.fixture(scope="function")
# def creation_user_data(test_user):
#     updated_data = test_user.copy()
#     updated_data.update({
#         "verified": True,
#         "banned": False
#     })
#     return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_full_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]      # указываем явно, см. ловушку exclude_unset в главе 6
    )

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(update={"verified": True, "banned": False})

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture()
def created_movies_data_for_db():
    return {
        "id" : 9999999,
        "name" : DataGenerator.generate_random_film_name(),
        "price" : DataGenerator.generate_random_prise(),
        "description" : DataGenerator.generate_random_description(),
        "image_url" : DataGenerator.generate_random_image_url(),
        "location" : DataGenerator.generate_location(),
        "published" : DataGenerator.generete_published(),
        "rating" : DataGenerator.generate_random_rating(),
        "genre_id" : 186,
        "created_at" : date.today()
    }




