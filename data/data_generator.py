from faker import Faker
from uuid import uuid4
import datetime
import random

fake = Faker(locale="en_US")

class DataGenerator:

    @staticmethod
    def generate_random_film_name():
        return " ".join(fake.words()).capitalize()

    @staticmethod
    def generate_random_image_url():
        return fake.image_url()

    @staticmethod
    def generate_random_prise():
        return fake.random_int(min=50, max=1000)

    @staticmethod
    def generate_random_max_prise(generate_random_prise):
        return generate_random_prise + DataGenerator.generate_random_prise()

    @staticmethod
    def generate_random_min_prise(generate_random_prise):
        return generate_random_prise - DataGenerator.generate_random_prise()

    @staticmethod
    def generate_random_description():
        return " ".join(fake.words(nb=10))

    @staticmethod
    def generate_location():
        location = ["MSK", "SPB"]
        return fake.random_element(location)

    @staticmethod
    def generete_published():
        return fake.boolean()

    @staticmethod
    def generate_random_id():
        return fake.random_int()

    @staticmethod
    def generate_random_page_size():
        return fake.random_int(min=1, max=20)

    @staticmethod
    def generate_random_page():
        return fake.random_int()

    @staticmethod
    def generate_random_created_at():
        created_at = ["asc", "desc"]
        return fake.random_element(created_at)

    @staticmethod
    def generate_random_full_name():
        full_name = fake.first_name() + " " + fake.last_name()
        return full_name

    @staticmethod
    def generate_random_password():
        return fake.password(special_chars=False)

    @staticmethod
    def generate_random_email():
        # return fake.email()
        return f"u{uuid4().hex[:16]}@gmail.com"

    @staticmethod
    def generate_random_rating():
        return fake.random_int(min=1, max=5)

    @staticmethod
    def generate_random_int(x):
        return fake.random_int(x)

    @staticmethod
    def generate_random_review_data():
        review_data = {
            # "rating": fake.random_int(min=1, max=5),
            # "text": " ".join(fake.words(nb=10))
            "rating": DataGenerator.generate_random_rating(),
            "text": DataGenerator.generate_random_description()
        }
        return review_data

    @staticmethod
    def generate_random_user_data():
        email = DataGenerator.generate_random_email()
        password = DataGenerator.generate_random_password()
        user_data = {
            "email": email,
            "fullName": DataGenerator.generate_random_full_name(),
            "password": password,
            "passwordRepeat": password
        }
        return user_data

    @staticmethod
    def generate_random_params_for_get_movies():
        min_prise = DataGenerator.generate_random_prise()
        params = {
            "pageSize": DataGenerator.generate_random_page_size(),
            "page": DataGenerator.generate_random_page_size(),
            "minPrice": min_prise,
            "maxPrice": min_prise + random.randrange(1, 1000),
            "locations": DataGenerator.generate_location(),
            "published": DataGenerator.generete_published(),
            "genreId": DataGenerator.generate_random_id(),
            "createdAt": DataGenerator.generate_random_created_at()
        }
        return params

    @staticmethod
    def generate_random_data_movies():
        body_movies = {
            "name": DataGenerator.generate_random_film_name(),
            "imageUrl": DataGenerator.generate_random_image_url(),
            "price": DataGenerator.generate_random_prise(),
            "description": DataGenerator.generate_random_description(),
            "location": DataGenerator.generate_location(),
            "published": DataGenerator.generete_published(),
            "genreId": 186
        }

        return body_movies

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_full_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }
