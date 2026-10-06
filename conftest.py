import pytest
import requests

from data.data_generator import DataGenerator
from clients.api_manager import ApiManager
from config.config import ADMIN_PASSWORD, ADMIN_LOGIN

generate = DataGenerator()

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
    params = generate.generate_random_params_for_get_movies()
    return params

@pytest.fixture
def created_movies_data():
    body_movies = generate.generate_random_data_movies()
    return body_movies

@pytest.fixture
def update_movies_data():
    body_movies = generate.generate_random_data_movies()
    return body_movies

@pytest.fixture
def auth_with_admin_credentials(api_manager):
    admin_credentials = (ADMIN_LOGIN, ADMIN_PASSWORD)
    api_manager.auth_api.authenticate(admin_credentials)

@pytest.fixture
def created_movies(created_movies_data, api_manager, auth_with_admin_credentials):
    return api_manager.movies_api.create_movies(movies_data=created_movies_data)

@pytest.fixture
def created_movies_without_admin_creds(created_movies_data, api_manager, auth_without_admin_credentials):
    return api_manager.movies_api.create_movies(
        movies_data=created_movies_data,
        expected_status=403
    )

@pytest.fixture
def auth_without_admin_credentials(api_manager):
    user_data = generate.generate_random_user_data()
    email = user_data['email']
    password = user_data['password']
    api_manager.auth_api.register_user(user_data=user_data)
    api_manager.auth_api.authenticate((email, password))

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








