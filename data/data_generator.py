from faker import Faker
from uuid import uuid4
import random

fake = Faker(locale="en_US")

class DataGenerator:
    def generate_random_film_name(self):
        return " ".join(fake.words()).capitalize()

    def generate_random_image_url(self):
        return fake.image_url()

    def generate_random_prise(self):
        return fake.random_int(min=50, max=1000)

    def generate_random_description(self):
        return " ".join(fake.words(nb=10))

    def generate_location(self):
        location = ["MSK", "SPB"]
        return fake.random_element(location)

    def generete_published(self):
        return fake.boolean()

    def generate_random_id(self):
        return fake.random_int()

    def generate_random_page_size(self):
        return fake.random_int(min=1, max=20)

    def generate_random_page(self):
        return fake.random_int()

    def generate_random_created_at(self):
        created_at = ["asc", "desc"]
        return fake.random_element(created_at)

    def generate_random_full_name(self):
        full_name = fake.first_name() + " " + fake.last_name()
        return full_name

    def generate_random_password(self):
        return fake.password()

    def generate_random_email(self):
        # return fake.email()
        return f"u{uuid4().hex[:16]}@gmail.com"

    def generate_random_rating(self):
        return fake.random_int(min=1, max=5)

    def generate_random_review_data(self):
        review_data = {
            # "rating": fake.random_int(min=1, max=5),
            # "text": " ".join(fake.words(nb=10))
            "rating": self.generate_random_rating(),
            "text": self.generate_random_description()
        }
        return review_data

    def generate_random_user_data(self):
        email = self.generate_random_email()
        password = self.generate_random_password()
        user_data = {
            "email": email,
            "fullName": self.generate_random_full_name(),
            "password": password,
            "passwordRepeat": password
        }
        return user_data

    def generate_random_params_for_get_movies(self):
        min_prise = self.generate_random_prise()
        params = {
            "pageSize": self.generate_random_page_size(),
            "page": self.generate_random_page_size(),
            "minPrice": min_prise,
            "maxPrice": min_prise + random.randrange(1, 1000),
            "locations": self.generate_location(),
            "published": self.generete_published(),
            "genreId": self.generate_random_id(),
            "createdAt": self.generate_random_created_at()
        }
        return params

    def generate_random_data_movies(self):
        body_movies = {
            "name": self.generate_random_film_name(),
            "imageUrl": self.generate_random_image_url(),
            "price": self.generate_random_prise(),
            "description": self.generate_random_description(),
            "location": self.generate_location(),
            "published": self.generete_published(),
            "genreId": 186
        }

        return body_movies
