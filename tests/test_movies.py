def test_get_movies(api_manager):
    api_manager.movies_api.get_movies(expected_status=200)

def test_get_movies_with_filter_pagesize(api_manager, params_get_movies):
    params = {"pageSize" : params_get_movies["pageSize"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    assert len(response.json()["movies"]) == params["pageSize"]

def test_get_movies_with_filter_page(api_manager, params_get_movies):
    params_page_size = {"pageSize": params_get_movies["pageSize"]}
    params_page = {"page": params_get_movies["page"]}
    params = {}
    params.update(params_page_size)
    params.update(params_page)
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    assert len(response.json()["movies"]) == params["pageSize"]
    assert response.json()["page"] == params["page"]

def test_get_movies_with_filter_min_price(api_manager, params_get_movies):
    params = {"minPrice": params_get_movies["minPrice"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    for movie in response.json()["movies"]:
        assert movie["price"] >= params_get_movies["minPrice"]

def test_get_movies_with_filter_max_price(api_manager, params_get_movies):
    params = {"maxPrice": params_get_movies["maxPrice"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    for movie in response.json()["movies"]:
        assert movie["price"] <= params_get_movies["maxPrice"]

def test_get_movies_with_filter_locations(api_manager, params_get_movies):
    params = {"locations": params_get_movies["locations"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    for movie in response.json()["movies"]:
        assert movie["location"] == params_get_movies["locations"]

def test_get_movies_with_filter_published(api_manager, params_get_movies):
    params = {"published": str(params_get_movies["published"]).lower()}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    for movie in response.json()["movies"]:
        assert str(movie["published"]).lower() == str(params_get_movies["published"]).lower()

def test_get_movies_with_filter_genreId(api_manager, params_get_movies):
    params = {"genreId": params_get_movies["genreId"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)
    for movie in response.json()["movies"]:
        assert movie["genreId"] == params_get_movies["genreId"]

def test_get_movies_with_filter_created_at(api_manager, params_get_movies):
    params = {"createdAt": params_get_movies["createdAt"]}
    response = api_manager.movies_api.get_movies(expected_status=200, params=params)

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

def test_get_movies_with_invalid_params(api_manager, params_get_movies):
    params = {"pageSize": "qwe"}
    response = api_manager.movies_api.get_movies(expected_status=400, params=params)


def test_created_movies_with_admin_creds(created_movies, created_movies_data, api_manager):
    response = created_movies.json()
    id = response["id"]
    del response["id"]
    del response["genre"]
    del response["createdAt"]
    del response["rating"]
    assert response == created_movies_data, \
    f"Создание фильма не было выполнено с заданными значениям"

    response_get_movies_id = api_manager.movies_api.get_movies_by_id(id=id).json()
    del response_get_movies_id["genre"]
    del response_get_movies_id["reviews"]
    del response_get_movies_id["createdAt"]
    del response_get_movies_id["rating"]
    del response_get_movies_id["id"]
    assert response_get_movies_id == created_movies_data, \
    f"Данные в БД записаны не корректно"

def test_created_movies_without_admin_creds(created_movies_without_admin_creds, created_movies_data, api_manager):
    pass

def test_created_movies_with_invalid_params(api_manager, auth_with_admin_credentials):
    api_manager.movies_api.create_movies(movies_data={}, expected_status=400)

def test_created_movies_already_exists(created_movies_data, api_manager, auth_with_admin_credentials, created_movies):
    api_manager.movies_api.create_movies(movies_data=created_movies_data, expected_status=409)

def test_get_film_by_invalid_id(api_manager):
    response = api_manager.movies_api.get_movies_by_id(id=9999999, expected_status=404)

def test_delete_movies_with_admin_creds(api_manager, auth_with_admin_credentials, created_movies):
    response = created_movies.json()
    id = response["id"]
    api_manager.movies_api.delete_movies(id)
    api_manager.movies_api.get_movies_by_id(id, expected_status=404)

def test_delete_movies_without_admin_creds(api_manager, created_movies, auth_without_admin_credentials, api_manager_with_role_user):
    response = created_movies.json()
    id = response["id"]
    api_manager_with_role_user.movies_api.delete_movies(id, expected_status=403)

def test_delete_movies_with_invalid_id(api_manager, auth_with_admin_credentials):
    api_manager.movies_api.delete_movies(id=9999999, expected_status=404)

def test_update_movies_with_admin_creds(api_manager, created_movies, update_movies_data):
    id = created_movies.json()["id"]
    api_manager.movies_api.get_movies_by_id(id)
    response = api_manager.movies_api.update_movies(id=id, movies_data=update_movies_data).json()

    del response["id"]
    del response["genre"]
    del response["createdAt"]
    del response["rating"]
    assert response == update_movies_data

def test_update_movies_without_admin_creds(api_manager_with_role_user, created_movies, update_movies_data, auth_without_admin_credentials):
    id = created_movies.json()["id"]
    api_manager_with_role_user.movies_api.get_movies_by_id(id)
    api_manager_with_role_user.movies_api.update_movies(id=id, movies_data=update_movies_data, expected_status=403)

def test_update_movies_with_invalid_data(api_manager, created_movies):
    id = created_movies.json()["id"]
    api_manager.movies_api.get_movies_by_id(id)
    response = api_manager.movies_api.update_movies(id=id, movies_data={"genreId" : "qwe"}, expected_status=400)

def test_update_movies_with_invalid_id(api_manager, auth_with_admin_credentials):
    api_manager.movies_api.update_movies(id=9999999, movies_data=None, expected_status=404)




