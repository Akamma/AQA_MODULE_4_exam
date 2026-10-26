# from random import randint
#
# import pytest
# import random
# import allure
#
# from http.client import responses
# from db_models.accounts_transaction_template import AccountTransactionTemplate
# from db_models.movies import MovieDBModel
# from data.data_generator import DataGenerator
# from sqlalchemy.orm import Session
# from clients.api_manager import ApiManager
# from api_models.base_models import TestUser, RegisterUserResponse
# from constants.roles import Roles
# import datetime
# from pytest_check import check
#
# def test_db_requests(super_admin, db_helper, created_test_user):
#     assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
#     assert db_helper.user_exists_by_email(created_test_user.email)
#
# def test_db_creation_film(db_helper, super_admin, created_movies_data):
#     assert db_helper.get_movie_by_name(created_movies_data['name']) == None
#     response = super_admin.api.movies_api.create_movies(movies_data=created_movies_data)
#     id = response.json()['id']
#     assert db_helper.get_movie_by_id(id).id == id
#     assert db_helper.get_movie_by_id(id).name == response.json()['name']
#     super_admin.api.movies_api.delete_movies(id=id)
#     assert db_helper.get_movie_by_id(movie_id=id) == None
#
#     # Modul_4\Cinescope\tests\api\test_other_api.py
#
# # def test_accounts_transaction_template(db_session: Session):
# #     # ====================================================================== Подготовка к тесту
# #     # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)
# #
# #     stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=1000)
# #     bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)
# #
# #     # Добавляем записи в сессию
# #     db_session.add_all([stan, bob])
# #     # Фиксируем изменения в базе данных
# #     db_session.commit()
# #
# #     def transfer_money(session, from_account, to_account, amount):
# #         # пример функции выполняющей транзакцию
# #         # представим что она написана на стороне тестируемого сервиса
# #         # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
# #         """
# #         Переводит деньги с одного счета на другой.
# #         :param session: Сессия SQLAlchemy.
# #         :param from_account_id: ID счета, с которого списываются деньги.
# #         :param to_account_id: ID счета, на который зачисляются деньги.
# #         :param amount: Сумма перевода.
# #         """
# #         # Получаем счета
# #         from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
# #         to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()
# #
# #         # Проверяем, что на счете достаточно средств
# #         if from_account.balance < amount:
# #             raise ValueError("Недостаточно средств на счете")
# #
# #         # Выполняем перевод
# #         from_account.balance -= amount
# #         to_account.balance += amount
# #
# #         # Сохраняем изменения
# #         session.commit()
# #
# #     # ====================================================================== Тест
# #     # Проверяем начальные балансы
# #     assert stan.balance == 1000
# #     assert bob.balance == 500
# #
# #     try:
# #         # Выполняем перевод 200 единиц от stan к bob
# #         transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)
# #
# #         # Проверяем, что балансы изменились
# #         assert stan.balance == 800
# #         assert bob.balance == 700
# #
# #     except Exception as e:
# #         # Если произошла ошибка, откатываем транзакцию
# #         db_session.rollback()  # откат всех введеных нами изменений
# #         pytest.fail(f"Ошибка при переводе денег: {e}")
# #
# #     finally:
# #         # Удаляем данные для тестирования из базы
# #         db_session.delete(stan)
# #         db_session.delete(bob)
# #         # Фиксируем изменения в базе данных
# #         db_session.commit()
#
# def test_accounts_transaction_template_with_no_money(db_session: Session):
#     # ====================================================================== Подготовка к тесту
#     # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)
#
#     stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=200)
#     bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)
#
#     # Добавляем записи в сессию
#     db_session.add_all([stan, bob])
#     # Фиксируем изменения в базе данных
#     db_session.commit()
#
#     def transfer_money(session, from_account, to_account, amount):
#
#         from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
#         to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()
#
#         # Проверяем, что на счете достаточно средств
#         if from_account.balance < amount:
#             raise ValueError("Недостаточно средств на счете")
#
#         # Выполняем перевод
#         from_account.balance -= amount
#         to_account.balance += amount
#
#         # Сохраняем изменения
#         session.commit()
#
#     try:
#         # Выполняем перевод 200 единиц от stan к bob
#         transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=300)
#
#         # Проверяем, что балансы изменились
#         assert stan.balance == -100
#         assert bob.balance == 800
#
#     except Exception as e:
#         # Если произошла ошибка, откатываем транзакцию
#         db_session.rollback()  # откат всех введеных нами изменений
#         assert stan.balance == 200
#         assert bob.balance == 500
#
#     finally:
#         # Удаляем данные для тестирования из базы
#         db_session.delete(stan)
#         db_session.delete(bob)
#         # Фиксируем изменения в базе данных
#         db_session.commit()
#
# def test_delete_movie(super_admin, db_session, created_movies_data_for_db):
#     movie = MovieDBModel(**created_movies_data_for_db)
#     db_session.add(movie)
#     db_session.commit()
#
#     created_movie = db_session.query(MovieDBModel).filter_by(id=movie.id).first()
#     assert created_movie != None
#
#     db_session.delete(movie)
#     db_session.commit()
#
#     deleted_movies = db_session.query(MovieDBModel).filter_by(id=movie.id).first()
#     assert deleted_movies == None
#
#
# @allure.epic("Тестирование транзакций")
# @allure.feature("Тестирование транзакций между счетами")
# class TestAccountTransactionTemplate:
#
#     @allure.story("Корректность перевода денег между двумя счетами")
#     @allure.description("""
#     Этот тест проверяет корректность перевода денег между двумя счетами.
#     Шаги:
#     1. Создание двух счетов: Stan и Bob.
#     2. Перевод 200 единиц от Stan к Bob.
#     3. Проверка изменения балансов.
#     4. Очистка тестовых данных.
#     """)
#     @allure.severity(allure.severity_level.CRITICAL)
#     @allure.label("qa_name", "Ivan Petrovich")
#     @allure.title("Тест перевода денег между счетами 200 рублей")
#     def test_accounts_transaction_template(self, db_session: Session):
#         # ====================================================================== Подготовка к тесту
#         with allure.step("Создание тестовых данных в базе данных: счета Stan и Bob"):
#             stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(10)}", balance=1000)
#             bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(10)}", balance=500)
#             db_session.add_all([stan, bob])
#             db_session.commit()
#
#         @allure.step("Функция перевода денег: transfer_money")
#         @allure.description("""
#             функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
#             и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
#             """)
#         def transfer_money(session, from_account, to_account, amount):
#             with allure.step(" Получаем счета"):
#                 from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
#                 to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()
#
#             with allure.step("Проверяем, что на счете достаточно средств"):
#                 if from_account.balance < amount:
#                     raise ValueError("Недостаточно средств на счете")
#
#             with allure.step("Выполняем перевод"):
#                 from_account.balance -= amount
#                 to_account.balance += amount
#
#             with allure.step("Сохраняем изменения"):
#                 session.commit()
#
#         # ====================================================================== Тест
#         with allure.step("Проверяем начальные балансы"):
#             assert stan.balance == 1000
#             assert bob.balance == 500
#
#         try:
#             with allure.step("Выполняем перевод 200 единиц от stan к bob"):
#                 transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)
#
#             with allure.step("Проверяем, что балансы изменились"):
#                 assert stan.balance == 800
#                 assert bob.balance == 700
#
#         except Exception as e:
#             with allure.step("ОШИБКА откаты транзакции"):
#                 db_session.rollback()
#
#             pytest.fail(f"Ошибка при переводе денег: {e}")
#
#         finally:
#             with allure.step("Удаляем данные для тестирования из базы"):
#                 db_session.delete(stan)
#                 db_session.delete(bob)
#                 db_session.commit()
#
#     @allure.title("Тест регистрации пользователя с помощью Mock")
#     @allure.severity(allure.severity_level.MINOR)
#     @allure.label("qa_name", "Ivan Petrovich")
#     def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
#         with allure.step(" Мокаем метод register_user в auth_api"):
#             mock_response = RegisterUserResponse(  # Фиктивный ответ
#                 id="id",
#                 email="email@email.com",
#                 fullName="fullName",
#                 verified=True,
#                 banned=False,
#                 roles=[Roles.SUPER_ADMIN],
#                 createdAt=str(datetime.datetime.now())
#             )
#
#             mocker.patch.object(
#                 api_manager.auth_api,  # Объект, который нужно замокать
#                 'register_user',  # Метод, который нужно замокать
#                 return_value=mock_response  # Фиктивный ответ
#             )
#
#         with allure.step("Вызываем метод, который должен быть замокан"):
#             register_user_response = api_manager.auth_api.register_user(test_user)
#
#         with allure.step("Проверяем, что ответ соответствует ожидаемому"):
#             with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
#                 with check:
#                     # Строка ниже выдаст исклющение и но выполнение теста продолжится
#                     check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
#                     check.equal(register_user_response.email, mock_response.email)
#
#             with allure.step("Проверка поля banned"):
#                 with check("Проверка поля banned"):  # можно использовать вместо allure.step
#                     check.equal(register_user_response.banned, mock_response.banned)