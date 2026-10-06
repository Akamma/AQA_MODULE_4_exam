from custom_requester.custom_requester import CustomRequester
from config.config import MOVIES_BASE_URL

MOVIES = '/movies'
REVIEWS = "/reviews"
GENRES = '/genres'

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_BASE_URL)

    def get_movies(self, expected_status=200, params=None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            expected_status=expected_status,
            params=params,
            **kwargs
        )

    def get_movies_by_id(self, id, expected_status=200, params=None, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{id}",
            expected_status=expected_status,
            params=params,
            **kwargs
        )

    def create_movies(self, movies_data, params=None,expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            expected_status=expected_status,
            data=movies_data,
            **kwargs
        )

    def delete_movies(self, id,expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{id}",
            expected_status=expected_status,
            **kwargs
        )

    def update_movies(self, id, movies_data, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{id}",
            data=movies_data,
            expected_status=expected_status,
            **kwargs
        )

    def create_movies_review(self, id_movies, reviews_data, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}",
            data=reviews_data,
            expected_status=expected_status,
            **kwargs
        )

    def get_movies_review(self, id_movies, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}",
            expected_status=expected_status,
            **kwargs
        )

    def update_movies_review(self, id_movies, data_review, expected_status=200, **kwargs):
        return self.send_request(
            method="PUT",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}",
            data=data_review,
            expected_status=expected_status,
            **kwargs
        )

    def delete_movies_review(self, id_movies, params=None, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}",
            expected_status=expected_status,
            params=params,
            **kwargs
        )

    def hide_review_on_movies(self, id_movies, id_user, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}/hide/{id_user}",
            expected_status=expected_status,
            **kwargs
        )

    def show_review_on_movies(self,  id_movies, id_user, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{id_movies}{REVIEWS}/show/{id_user}",
            expected_status=expected_status,
            **kwargs
        )

    def get_genres(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{GENRES}",
            expected_status=expected_status,
            **kwargs
        )








