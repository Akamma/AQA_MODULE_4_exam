from pages.base_page import BasePage
from playwright.sync_api import Page

class CinescopeReviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url
        self.open_movies = '[data-qa-id="more_button"]'
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.send_review = '[data-qa-id="movie_review_submit_button"]'

    def open(self):
        self.open_url(self.url)

    def created_review(self):
        self.click(self.open_movies)
        self.enter_text(self.review_input, "Отзыв оставлен")
        self.click(self.send_review)


