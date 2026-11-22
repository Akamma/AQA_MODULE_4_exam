from pages.review_page import CinescopeReviewPage
from pages.register_page import CinescopeRegisterPage
from random import randint
from playwright.sync_api import expect
import allure
import pytest

@allure.epic("Тестирование UI")
@allure.feature("Отзыв")
@pytest.mark.ui
class TestReview:
    @allure.title("Успешное создание отзыва")
    def test_review_ui(self, login_page, page):
        with allure.step("Регистрация пользователя"):
            email = f"aqatest{randint(1, 999999)}@email.qa"
            # Для примера. Так-то уже есть фикстуры и генератор данных
            register_page = CinescopeRegisterPage(page)
            register_page.open()
            register_page.register("Иван Иванов", email, "qwerty123Q")
        with allure.step("Выполнение входа:"):
            login_page.login(email=email, password='qwerty123Q')
            expect(login_page.page.get_by_text("Вы вошли в аккаунт", exact=True)).to_be_visible()
        with allure.step("Создание отзыва"):
            review_page = CinescopeReviewPage(page)
            review_page.created_review()
            expect(review_page.page.get_by_text("Вы вошли в аккаунт", exact=True)).to_be_visible()





