from pages.login_page import CinescopeLoginPage
from pages.register_page import CinescopeRegisterPage
from random import randint
from playwright.sync_api import expect
import allure
import pytest

@allure.epic("Тестирование UI")
@allure.feature("Регистрация")
@pytest.mark.ui
class TestLogin:
    @allure.title("Успешный вход в систему для нового пользователя")
    def test_login(self, login_page, page):
        with allure.step("Регистрация пользователя"):
            email = f"aqatest{randint(1, 999999)}@email.qa"
            # Для примера. Так-то уже есть фикстуры и генератор данных
            register_page = CinescopeRegisterPage(page)
            register_page.open()
            register_page.register("Иван Иванов", email, "qwerty123Q")
        with allure.step("Выполнение входа:"):
            login_page.login(email=email, password='qwerty123Q')
            expect(page.get_by_text("Вы вошли в аккаунт", exact=True)).to_be_visible()