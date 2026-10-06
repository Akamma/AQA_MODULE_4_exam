import pytest
import requests
import random

from data.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_BASE_URL
from clients.api_manager import ApiManager
from config.admin_credentials import ADMIN_PASSWORD, ADMIN_LOGIN

generate = DataGenerator()

#Сессия для супер админа
@pytest.fixture
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

#Сессия для роли USER
@pytest.fixture
def session_with_role_user():
    http_session = requests.Session()
    yield http_session
    http_session.close()

#Сессия без токена
@pytest.fixture
def unauthenticated_session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def api_manager(session):
    return ApiManager(session)

@pytest.fixture
def unauthenticated_api_manager(unauthenticated_session):
    return ApiManager(unauthenticated_session)

@pytest.fixture
def api_manager_with_role_user(session_with_role_user):
    return ApiManager(session_with_role_user)

@pytest.fixture
def params_get_movies():
    generate = DataGenerator()
    min_prise = generate.generate_random_prise()
    params = {
        "pageSize": generate.generate_random_page_size(),
        "page": generate.generate_random_page_size(),
        "minPrice": min_prise,
        "maxPrice": min_prise + random.randrange(1, 1000),
        "locations": generate.generate_location(),
        "published": generate.generete_published(),
        "genreId": generate.generate_random_id(),
        "createdAt": generate.generate_random_created_at()
    }
    return params

@pytest.fixture
def created_movies_data():
    generate = DataGenerator()
    body_movies = {
        "name": generate.generate_random_film_name(),
        "imageUrl": generate.generate_random_image_url(),
        "price": generate.generate_random_prise(),
        "description": generate.generate_random_description(),
        "location": generate.generate_location(),
        "published": generate.generete_published(),
        "genreId": 186
    }

    return body_movies

@pytest.fixture
def update_movies_data():
    generate = DataGenerator()
    body_movies = {
        "name": generate.generate_random_film_name(),
        "imageUrl": generate.generate_random_image_url(),
        "price": generate.generate_random_prise(),
        "description": generate.generate_random_description(),
        "location": generate.generate_location(),
        "published": generate.generete_published(),
        "genreId": 186
    }

    return body_movies

@pytest.fixture
def auth_with_admin_credentials(api_manager):
    admin_credentials = (ADMIN_LOGIN, ADMIN_PASSWORD)
    api_manager.auth_api.authenticate(admin_credentials)

@pytest.fixture
def created_movies(created_movies_data, api_manager, auth_with_admin_credentials):
    return api_manager.movies_api.create_movies(movies_data=created_movies_data)

@pytest.fixture
def created_movies_without_admin_creds(created_movies_data, api_manager_with_role_user, auth_without_admin_credentials):
    return api_manager_with_role_user.movies_api.create_movies(
        movies_data=created_movies_data,
        expected_status=403
    )


@pytest.fixture
def auth_without_admin_credentials(api_manager_with_role_user):
    user_data = generate.generate_random_user_data()
    email = user_data['email']
    password = user_data['password']
    api_manager_with_role_user.auth_api.register_user(user_data=user_data)
    api_manager_with_role_user.auth_api.authenticate((email, password))

@pytest.fixture
def created_review_data():
    review_data = generate.generate_random_review_data()
    return review_data

@pytest.fixture
def created_review(api_manager, auth_with_admin_credentials, created_movies, created_review_data):
    return api_manager.movies_api.create_movies_review(
        id_movies=created_movies.json()["id"],
        reviews_data=created_review_data
    )

@pytest.fixture
def created_review_by_user(api_manager_with_role_user, created_movies, created_review_data, auth_without_admin_credentials):
    return api_manager_with_role_user.movies_api.create_movies_review(
        id_movies=created_movies.json()["id"],
        reviews_data=created_review_data
    )

@pytest.fixture
def creation_multiple_reviews(created_movies):
    def creation_review():
        session_in = requests.Session()
        api = ApiManager(session_in)
        user_data = generate.generate_random_user_data()
        email = user_data['email']
        password = user_data['password']

        api.auth_api.register_user(user_data=user_data)
        api.auth_api.authenticate((email,password))
        review_data = generate.generate_random_review_data()
        response = api.movies_api.create_movies_review(id_movies=created_movies.json()['id'], reviews_data=review_data)
        return response
    return creation_review








