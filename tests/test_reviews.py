from data.data_generator import DataGenerator
from clients.api_manager import ApiManager
import requests

generate = DataGenerator()

def test_get_review_on_movies(created_review, created_review_data, api_manager, created_movies):
    response = created_review.json()
    assert response["rating"] == created_review_data["rating"]
    assert response["text"] == created_review_data["text"]
    assert response["user"]["fullName"] == api_manager.user_api.get_user_me().json()["fullName"]

    response_review = api_manager.movies_api.get_movies_review(id_movies=created_movies.json()["id"]).json()
    assert response_review[0]["rating"] == created_review_data["rating"]
    assert response_review[0]["text"] == created_review_data["text"]
    assert response_review[0]["user"]["fullName"] == api_manager.user_api.get_user_me().json()["fullName"]

def test_get_reviews_on_nonexist_movies(api_manager):
    response = api_manager.movies_api.get_movies_review(id_movies=99999, expected_status=404)

def test_get_empty_reviews_on_movies(api_manager, created_movies):
    response = api_manager.movies_api.get_movies_review(id_movies=created_movies.json()['id'])
    assert response.json() == []

def test_creation_reviews_on_multiple_users(api_manager, creation_multiple_reviews, created_movies):
    review1 = creation_multiple_reviews().json()
    review2 = creation_multiple_reviews().json()
    reviews = [review1, review2]
    response_review = api_manager.movies_api.get_movies_review(id_movies=created_movies.json()['id'])
    for review in reviews:
        assert review in response_review.json()

def test_created_review_on_invalid_movies_id(api_manager, created_review_data, auth_with_admin_credentials):
    api_manager.movies_api.create_movies_review(id_movies=99999, reviews_data=created_review_data, expected_status=404)

def test_created_review_without_auth(created_review_data, created_movies, unauthenticated_api_manager):
    unauthenticated_api_manager.movies_api.create_movies_review(
        id_movies=created_movies.json()['id'],
        reviews_data=created_review_data,
        expected_status=401
    )

def test_creation_multiple_reviews_on_one_user(api_manager, created_review_data, created_movies, auth_with_admin_credentials):
    id = created_movies.json()['id']
    api_manager.movies_api.create_movies_review(id_movies=id, reviews_data=created_review_data)
    api_manager.movies_api.create_movies_review(id_movies=id, reviews_data=created_review_data, expected_status=409)

def test_creation_reviews_on_delete_movies(api_manager, created_movies, auth_with_admin_credentials, created_review_data):
    id = created_movies.json()['id']
    api_manager.movies_api.delete_movies(id=id)
    response = api_manager.movies_api.create_movies_review(id_movies=id, reviews_data=created_review_data, expected_status=404)
    assert response.json()['message'] == 'Фильм не найден'

def test_edit_own_review(api_manager_with_role_user, created_movies, created_review_by_user):
    review_data = generate.generate_random_review_data()
    response = api_manager_with_role_user.movies_api.update_movies_review(
        id_movies=created_movies.json()['id'],
        data_review=review_data
    )
    assert response.json()['text'] == review_data['text']
    assert response.json()['rating'] == review_data['rating']
    assert response.json()['text'] == review_data['text']

def test_edit_other_user_review(created_movies, created_review_by_user, api_manager_with_role_user):
    review_data = generate.generate_random_review_data()
    user = generate.generate_random_user_data()
    api_manager_with_role_user.auth_api.register_user(user_data=user)
    api_manager_with_role_user.auth_api.authenticate((user["email"], user['password']))

    response = api_manager_with_role_user.movies_api.update_movies_review(
        id_movies=created_movies.json()['id'],
        data_review=review_data,
        expected_status=404
    )
    assert response.json()['message'] == 'Отзыв не найден'

def test_update_review_without_auth(unauthenticated_api_manager, created_movies, created_review, created_review_data):
    unauthenticated_api_manager.movies_api.update_movies_review(
        id_movies=created_movies.json()['id'],
        data_review=created_review_data,
        expected_status=401
    )

def test_edit_invalid_review(api_manager, created_movies, created_review_data):
    response = api_manager.movies_api.update_movies_review(
        id_movies=created_movies.json()['id'],
        data_review=created_review_data,
        expected_status=404
    )
    assert response.json()['message'] == 'Отзыв не найден'

def test_delete_own_review_with_admin_auth(api_manager, created_movies, created_review):
    api_manager.movies_api.delete_movies_review(id_movies=created_movies.json()['id'])
    response = api_manager.movies_api.get_movies_review(id_movies=created_movies.json()['id'])
    assert response.json() == []

def test_delete_own_review_with_user_role_auth(api_manager_with_role_user, created_movies, created_review_by_user):
    api_manager_with_role_user.movies_api.delete_movies_review(id_movies=created_movies.json()['id'])
    response = api_manager_with_role_user.movies_api.get_movies_review(id_movies=created_movies.json()['id'])
    assert response.json() == []

def test_delete_other_user_review_with_admin_auth(api_manager, api_manager_with_role_user, created_movies, created_review_by_user):
    id = api_manager_with_role_user.user_api.get_user_me().json()['id']
    api_manager.movies_api.delete_movies_review(id_movies=created_movies.json()['id'], params={'userId' : id})
    response = api_manager_with_role_user.movies_api.get_movies_review(id_movies=created_movies.json()['id'])
    assert response.json() == []

def test_delete_other_user_review_with_user_auth(api_manager_with_role_user, created_movies, created_review_by_user):
    session = requests.Session()
    api_manager = ApiManager(session)
    user = generate.generate_random_user_data()
    api_manager.auth_api.register_user(user)
    api_manager.auth_api.authenticate((user['email'], user['password']))
    id = api_manager_with_role_user.user_api.get_user_me().json()['id']
    api_manager.movies_api.delete_movies_review(
        id_movies=created_movies.json()['id'],
        params={'userId': id},
        expected_status=403
    )

def test_delete_invalid_review(api_manager, created_movies):
    api_manager.movies_api.delete_movies_review(id_movies=created_movies.json()['id'], expected_status=404)

def test_deleted_review_on_deleted_movies(api_manager, created_movies, created_review):
    id = created_movies.json()['id']
    api_manager.movies_api.delete_movies(id=id)
    api_manager.movies_api.delete_movies_review(id_movies=id, expected_status=404)

def test_hide_review_with_admin_auth(api_manager, created_movies, created_review):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.hide_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )
def test_hide_review_with_user_role_auth(api_manager_with_role_user, created_movies, created_review_by_user):
    id_user = api_manager_with_role_user.user_api.get_user_me().json()['id']
    api_manager_with_role_user.movies_api.hide_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user,
        expected_status=403
    )

def test_hide_invalid_review(api_manager, created_movies):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.hide_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user,
        expected_status=404
    )

def test_show_review_with_admin_auth(api_manager, created_movies, created_review):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.hide_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

    api_manager.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

def test_show_review_with_user_role_auth(api_manager_with_role_user, created_movies, created_review, api_manager, auth_without_admin_credentials):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.hide_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

    api_manager_with_role_user.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user,
        expected_status=403
    )

def test_show_review_already_showed(api_manager, created_movies, created_review):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

    api_manager.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

def test_hide_review_already_hided(api_manager, created_movies, created_review):
    id_user = api_manager.user_api.get_user_me().json()['id']
    api_manager.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )

    api_manager.movies_api.show_review_on_movies(
        id_movies=created_movies.json()['id'],
        id_user=id_user
    )



















