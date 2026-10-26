from pytest_check import check

import pytest
from api_models.base_models import GetMoviesResponse, PostMovies
import allure

from data.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@pytest.mark.smoke
@allure.title("GET /movies")
@allure.description("Проверка запроса списка фильмов")
@allure.step("Начало теста")
def test_get_movies(api_manager):
    with allure.step("Выполнение запроса"):
        response = api_manager.movies_api.get_movies(expected_status=200)
        GetMoviesResponse(**response.json())


@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@pytest.mark.smoke
@allure.title("GET /movies с фильтрацией")
@allure.description("Проверка метода GET MOVIES с фильтрацией")
@pytest.mark.parametrize('min_price,max_price,location,genreId', [
    (500, 1000, "MSK", 186),
    (400, 700, "SPB", 186),
], ids=["MSK","SPB"])
def test_get_movies_with_filter(min_price, max_price, location, genreId, api_manager):
    param = {
        "minPrice" : min_price,
        "maxPrice" : max_price,
        "locations" : location,
        "genreId" : genreId
    }
    response = api_manager.movies_api.get_movies(params=param).json()
    GetMoviesResponse(**response)

    for movie in response['movies']:
        assert float(movie['price']) <= float(max_price)
        assert float(movie['price']) >= float(min_price)
        assert movie['location'] == location
        assert movie['genreId'] == genreId

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по pagesize")
@allure.description("Проверка метода GET MOVIES с фильтрацией по pagesize")
@pytest.mark.smoke
def test_get_movies_with_filter_pagesize(api_manager, params_get_movies):
    params = {"pageSize" : params_get_movies["pageSize"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    assert len(response.json()["movies"]) == params["pageSize"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по page")
@allure.description("Проверка метода GET MOVIES с фильтрацией по page")
@pytest.mark.smoke
def test_get_movies_with_filter_page(api_manager, params_get_movies):
    params_page_size = {"pageSize": params_get_movies["pageSize"]}
    params_page = {"page": params_get_movies["page"]}
    params = {}
    params.update(params_page_size)
    params.update(params_page)
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    assert len(response.json()["movies"]) == params["pageSize"]
    assert response.json()["page"] == params["page"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по min_price")
@allure.description("Проверка метода GET MOVIES с фильтрацией по min_price")
@pytest.mark.smoke
def test_get_movies_with_filter_min_price(api_manager, params_get_movies):
    params = {"minPrice": params_get_movies["minPrice"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    for movie in response.json()["movies"]:
        assert movie["price"] >= params_get_movies["minPrice"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по max_price")
@allure.description("Проверка метода GET MOVIES с фильтрацией по max_price")
@pytest.mark.smoke
def test_get_movies_with_filter_max_price(api_manager, params_get_movies):
    params = {"maxPrice": params_get_movies["maxPrice"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    for movie in response.json()["movies"]:
        assert movie["price"] <= params_get_movies["maxPrice"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по locations")
@allure.description("Проверка метода GET MOVIES с фильтрацией по locations")
@pytest.mark.smoke
def test_get_movies_with_filter_locations(api_manager, params_get_movies):
    params = {"locations": params_get_movies["locations"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    for movie in response.json()["movies"]:
        assert movie["location"] == params_get_movies["locations"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по published")
@allure.description("Проверка метода GET MOVIES с фильтрацией по published")
@pytest.mark.smoke
def test_get_movies_with_filter_published(api_manager, params_get_movies):
    params = {"published": str(params_get_movies["published"]).lower()}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    for movie in response.json()["movies"]:
        assert str(movie["published"]).lower() == str(params_get_movies["published"]).lower()

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по genreId")
@allure.description("Проверка метода GET MOVIES с фильтрацией по genreId")
@pytest.mark.smoke
def test_get_movies_with_filter_genreId(api_manager, params_get_movies):
    params = {"genreId": params_get_movies["genreId"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    for movie in response.json()["movies"]:
        assert movie["genreId"] == params_get_movies["genreId"]

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies с фильтрацией по created_at")
@allure.description("Проверка метода GET MOVIES с фильтрацией по created_at")
@pytest.mark.smoke
def test_get_movies_with_filter_created_at(api_manager, params_get_movies):
    params = {"createdAt": params_get_movies["createdAt"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    GetMoviesResponse(**response.json())
    if params["createdAt"] == "asc":
        asc = ""
        for movie in response.json()["movies"]:
            if asc < movie["createdAt"]:
                asc = movie["createdAt"]
            else:
                raise Exception("Сортировка по возрастанию не работает")

    if params["createdAt"] == "desc":
        asc = "9999-12-31T23:59:59.999Z"
        for movie in response.json()["movies"]:
            if asc > movie["createdAt"]:
                asc = movie["createdAt"]
            else:
                raise Exception("Сортировка по убыванию не работает")

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies")
@allure.description("Проверка получения фильма с не корректными параметрами")
def test_get_movies_with_invalid_params(api_manager, params_get_movies):
    params = {"pageSize": "qwe"}
    api_manager.movies_api.get_movies(expected_status=400, params=params)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("POST /movies")
@allure.description("Проверка создания пользователя с ролью SUPER_ADMIN")
@pytest.mark.smoke
@pytest.mark.db
def test_created_movies_with_super_admin_creds(created_movies, created_movies_data, super_admin, db_helper):
    response = created_movies.json()
    response_for_bd = response.copy()
    PostMovies(**response)
    id = response["id"]
    del response["id"]
    del response["genre"]
    del response["createdAt"]
    del response["rating"]
    assert response == created_movies_data, \
    f"Создание фильма не было выполнено с заданными значениям"

    movies_db = db_helper.get_movie_by_id(movie_id=id)
    db_created_at = movies_db.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


    with check:
        assert movies_db.id == response_for_bd['id']
        assert movies_db.name == response_for_bd['name']
        assert movies_db.price == response_for_bd['price']
        assert movies_db.description == response_for_bd['description']
        assert movies_db.image_url == response_for_bd['imageUrl']
        assert movies_db.location == response_for_bd['location']
        assert movies_db.published == response_for_bd['published']
        assert movies_db.genre_id == response_for_bd['genreId']
        assert db_created_at== response_for_bd['createdAt']
        assert movies_db.rating == response_for_bd['rating']

    response_get_movies_id = super_admin.api.movies_api.get_movies_by_id(id=id).json()
    del response_get_movies_id["genre"]
    del response_get_movies_id["reviews"]
    del response_get_movies_id["createdAt"]
    del response_get_movies_id["rating"]
    del response_get_movies_id["id"]
    assert response_get_movies_id == created_movies_data, \
    f"Данные в записаны не корректно"

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("POST /movies")
@allure.description("Проверка отсутствия возможности создания фильма без роли SUPER_ADMIN")
def test_created_movies_without_admin_creds(created_movies_without_admin_creds):
    pass

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("POST /movies")
@allure.description("Проверка отсутствия возможности создания фильма с не валидными параметрами")
def test_created_movies_with_invalid_params(super_admin):
    super_admin.api.movies_api.create_movies(movies_data={}, expected_status=400)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("POST /movies:")
@allure.description("Валидация возможности создания нескольких одинаковых фильмов")
def test_created_movies_already_exists(created_movies_data, created_movies, super_admin):
    super_admin.api.movies_api.create_movies(movies_data=created_movies_data, expected_status=409)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("GET /movies/{id}:")
@allure.description("Запрос фильма с несуществующим ID")
def test_get_film_by_invalid_id(common_user):
    common_user.api.movies_api.get_movies_by_id(id=9999999, expected_status=404)

# def test_delete_movies_with_super_admin_creds(created_movies, super_admin):
#     response = created_movies.json()
#     id = response["id"]
#     super_admin.api.movies_api.delete_movies(id)
#     super_admin.api.movies_api.get_movies_by_id(id, expected_status=404)
#
# def test_delete_movies_without_super_admin_creds(created_movies, common_user):
#     response = created_movies.json()
#     id = response["id"]
#     common_user.api.movies_api.delete_movies(id, expected_status=403)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("DELETE /movies/{id}: ")
@allure.description("Удаление фильма с несуществующим ID")
def test_delete_movies_with_invalid_id(super_admin):
    super_admin.api.movies_api.delete_movies(id=9999999, expected_status=404)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("DELETE /movies/{id}:")
@allure.description("Удаление фильма")
@pytest.mark.smoke
@pytest.mark.parametrize("user,expected_status", [("super_admin", 200), ("common_user", 403)])
def test_delete_movies(user, request, created_movies, common_user, expected_status):
    with allure.step(f"Удаление с полномочиями {user}"):
        user = request.getfixturevalue(user)
        response = created_movies.json()
        id = response["id"]
        user.api.movies_api.delete_movies(id, expected_status=expected_status)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("PATCH /movies/{id}: ")
@allure.description("Обновление фильма")
@pytest.mark.smoke
@pytest.mark.db
def test_update_movies_with_super_admin_creds(super_admin, created_movies, update_movies_data, db_helper):
    id = created_movies.json()["id"]
    super_admin.api.movies_api.get_movies_by_id(id)
    response = super_admin.api.movies_api.update_movies(id=id, movies_data=update_movies_data).json()
    PostMovies(**response)
    response_for_bd = response.copy()
    del response["id"]
    del response["genre"]
    del response["createdAt"]
    del response["rating"]
    assert response == update_movies_data

    movies_db = db_helper.get_movie_by_id(movie_id=id)
    db_created_at = movies_db.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    with check:
        assert movies_db.id == response_for_bd['id']
        assert movies_db.name == response_for_bd['name']
        assert movies_db.price == response_for_bd['price']
        assert movies_db.description == response_for_bd['description']
        assert movies_db.image_url == response_for_bd['imageUrl']
        assert movies_db.location == response_for_bd['location']
        assert movies_db.published == response_for_bd['published']
        assert movies_db.genre_id == response_for_bd['genreId']
        assert db_created_at == response_for_bd['createdAt']
        assert movies_db.rating == response_for_bd['rating']

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("PATCH /movies/{id}:")
@allure.description("Обновление фильма без полномочий SUPER_ADMIN")
def test_update_movies_without_super_admin_creds(common_user, created_movies, update_movies_data):
    id = created_movies.json()["id"]
    common_user.api.movies_api.get_movies_by_id(id)
    common_user.api.movies_api.update_movies(id=id, movies_data=update_movies_data, expected_status=403)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("PATCH /movies/{id}:")
@allure.description("Обновление фильма с не валидными параметрами")
def test_update_movies_with_invalid_data(super_admin, created_movies):
    id = created_movies.json()["id"]
    super_admin.api.movies_api.get_movies_by_id(id)
    super_admin.api.movies_api.update_movies(id=id, movies_data={"genreId" : "qwe"}, expected_status=400)

@allure.epic("Cinescop")
@allure.feature("movie_api")
@allure.label("qa_name", "Denis T")
@allure.title("PATCH /movies/{id}:")
@allure.description("Обновление фильма с не валидным id")
def test_update_movies_with_invalid_id(super_admin):
    super_admin.api.movies_api.update_movies(id=9999999, movies_data=None, expected_status=404)




