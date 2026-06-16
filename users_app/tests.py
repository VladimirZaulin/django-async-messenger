# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError
# from django.db import IntegrityError
# from datetime import datetime, timedelta
# from .models import User, Subscription, UserSubscription, Video, Payment, SoftDeleteManager
#
import logging
import os

from django.template.context_processors import request
from dotenv import load_dotenv
import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

from users_app.views import chat_message_v1

load_dotenv()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    assert User.objects.count() == 1
    assert user.username == 'testuser'

@pytest.mark.django_db
def chat_test():
    lg = logging.getLogger(__name__)
    factory = RequestFactory()
    request = factory.post('api/chat', {'message': 'Hello! How are you?', 'param2': 'value2'})
    response = chat_message_v1(request)
    lg.warning(f'Hi, i.m really here: {response}')
    assert "response" in response.data



# User = get_user_model()
#
#
# class UserModelTest(TestCase):
#     """Тесты для модели User"""
#
#     def setUp(self):
#         self.user_data = {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'phone': '+79161234567',
#             'password': 'testpass123'
#         }
#
#     def test_create_user(self):
#         """Тест создания обычного пользователя"""
#         user = User.objects.create_user(**self.user_data)
#
#         self.assertEqual(user.username, 'testuser',
#                          "Username пользователя должен соответствовать переданному значению")
#         self.assertEqual(user.email, 'test@example.com',
#                          "Email пользователя должен соответствовать переданному значению")
#         self.assertTrue(user.check_password('testpass123'),
#                         "Пароль пользователя должен корректно проверяться")
#         self.assertTrue(user.is_active,
#                         "Новый пользователь должен быть активным по умолчанию")
#         self.assertFalse(user.is_staff,
#                          "Обычный пользователь не должен иметь прав staff")
#         self.assertFalse(user.is_superuser,
#                          "Обычный пользователь не должен быть суперпользователем")
#
#     def test_create_superuser(self):
#         """Тест создания суперпользователя"""
#         superuser = User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             phone='+79160000000',
#             password='adminpass'
#         )
#
#         self.assertTrue(superuser.is_staff,
#                         "Суперпользователь должен иметь права staff")
#         self.assertTrue(superuser.is_superuser,
#                         "Суперпользователь должен иметь права superuser")
#
#     def test_unique_username_constraint(self):
#         """Тест уникальности username"""
#         User.objects.create_user(**self.user_data)
#
#         with self.assertRaises(IntegrityError) as context:
#             User.objects.create_user(
#                 username='testuser',
#                 email='test2@example.com',
#                 phone='+79161234568',
#                 password='testpass123'
#             )
#
#         self.assertIn('username', str(context.exception).lower(),
#                       "Должна возникать ошибка IntegrityError при попытке создать пользователя с существующим username")
#
#     def test_unique_email_constraint(self):
#         """Тест уникальности email"""
#         User.objects.create_user(**self.user_data)
#
#         with self.assertRaises(IntegrityError) as context:
#             User.objects.create_user(
#                 username='testuser2',
#                 email='test@example.com',
#                 phone='+79161234568',
#                 password='testpass123'
#             )
#
#         self.assertIn('email', str(context.exception).lower(),
#                       "Должна возникать ошибка IntegrityError при попытке создать пользователя с существующим email")
#
#     def test_unique_phone_constraint(self):
#         """Тест уникальности phone"""
#         User.objects.create_user(**self.user_data)
#
#         with self.assertRaises(IntegrityError) as context:
#             User.objects.create_user(
#                 username='testuser2',
#                 email='test2@example.com',
#                 phone='+79161234567',
#                 password='testpass123'
#             )
#
#         self.assertIn('phone', str(context.exception).lower(),
#                       "Должна возникать ошибка IntegrityError при попытке создать пользователя с существующим phone")
#
#     def test_user_str_representation(self):
#         """Тест строкового представления пользователя"""
#         user = User.objects.create_user(**self.user_data)
#
#         expected_str = 'testuser (test@example.com)'
#         actual_str = str(user)
#         self.assertEqual(actual_str, expected_str,
#                          f"Строковое представление пользователя должно быть '{expected_str}', но получено '{actual_str}'")
#
#     def test_user_referral_system(self):
#         """Тест реферальной системы"""
#         referrer = User.objects.create_user(
#             username='referrer',
#             email='referrer@example.com',
#             phone='+79161111111',
#             password='testpass123'
#         )
#
#         referral = User.objects.create_user(
#             username='referral',
#             email='referral@example.com',
#             phone='+79162222222',
#             password='testpass123',
#             referred=referrer
#         )
#
#         self.assertEqual(referral.referred, referrer,
#                          "Реферал должен ссылаться на правильного referrer")
#
#         referrals_count = referrer.referrals.count()
#         self.assertIn(referral, referrer.referrals.all(),
#                       f"Referrer должен иметь {referrals_count} рефералов, и созданный реферал должен быть среди них")
#
#
# class SubscriptionModelTest(TestCase):
#     """Тесты для модели Subscription"""
#
#     def setUp(self):
#         self.subscription_data = {
#             'title': 'Premium',
#             'price': '999.99',
#             'duration_days': 30,
#             'is_active': True
#         }
#
#     def test_create_subscription(self):
#         """Тест создания подписки"""
#         subscription = Subscription.objects.create(**self.subscription_data)
#
#         self.assertEqual(subscription.title, 'Premium',
#                          "Название подписки должно соответствовать переданному значению")
#         self.assertEqual(float(subscription.price), 999.99,
#                          "Цена подписки должна соответствовать переданному значению")
#         self.assertEqual(subscription.duration_days, 30,
#                          "Длительность подписки должна соответствовать переданному значению")
#         self.assertTrue(subscription.is_active,
#                         "Новая подписка должна быть активной по умолчанию")
#         self.assertIsNone(subscription.deleted_at,
#                           "Новая подписка не должна иметь дату удаления")
#
#     def test_unique_title_constraint(self):
#         """Тест уникальности title"""
#         Subscription.objects.create(**self.subscription_data)
#
#         with self.assertRaises(IntegrityError) as context:
#             Subscription.objects.create(
#                 title='Premium',
#                 price='499.99',
#                 duration_days=15,
#                 is_active=True
#             )
#
#         self.assertIn('title', str(context.exception).lower(),
#                       "Должна возникать ошибка IntegrityError при попытке создать подписку с существующим title")
#
#     def test_soft_delete(self):
#         """Тест мягкого удаления"""
#         subscription = Subscription.objects.create(**self.subscription_data)
#         initial_count = Subscription.objects.count()
#
#         subscription.delete()
#         subscription.refresh_from_db()
#
#         self.assertIsNotNone(subscription.deleted_at,
#                              "После мягкого удаления у подписки должна быть установлена дата удаления")
#
#         remaining_count = Subscription.objects.count()
#         self.assertEqual(remaining_count, initial_count - 1,
#                          f"После удаления должно остаться {initial_count - 1} подписок, но осталось {remaining_count}")
#
#         all_subscriptions_count = Subscription._base_manager.count()
#         self.assertEqual(all_subscriptions_count, 1,
#                          "В базовом менеджере должна остаться 1 подписка после мягкого удаления")
#
#
# class UserSubscriptionModelTest(TestCase):
#     """Тесты для модели UserSubscription"""
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             phone='+79161234567',
#             password='testpass123'
#         )
#
#         self.subscription = Subscription.objects.create(
#             title='Basic',
#             price='499.99',
#             duration_days=15,
#             is_active=True
#         )
#
#         start_date = datetime.now()
#         end_date = start_date + timedelta(days=15)
#
#         self.user_subscription_data = {
#             'user': self.user,
#             'subscription': self.subscription,
#             'start_date': start_date,
#             'end_date': end_date,
#             'status': 'active'
#         }
#
#     def test_create_user_subscription(self):
#         """Тест создания пользовательской подписки"""
#         user_subscription = UserSubscription.objects.create(**self.user_subscription_data)
#
#         self.assertEqual(user_subscription.user, self.user,
#                          "Пользовательская подписка должна ссылаться на правильного пользователя")
#         self.assertEqual(user_subscription.subscription, self.subscription,
#                          "Пользовательская подписка должна ссылаться на правильную подписку")
#         self.assertEqual(user_subscription.status, 'active',
#                          "Статус пользовательской подписки должен быть 'active'")
#
#     def test_status_choices(self):
#         """Тест валидных статусов подписки"""
#         valid_statuses = ['active', 'outdated', 'not_paid']
#
#         for status in valid_statuses:
#             with self.subTest(status=status):
#                 data = self.user_subscription_data.copy()
#                 data['status'] = status
#                 user_subscription = UserSubscription.objects.create(**data)
#
#                 self.assertEqual(user_subscription.status, status,
#                                  f"Статус должен быть '{status}', но получен '{user_subscription.status}'")
#
#     def test_invalid_status(self):
#         """Тест невалидного статуса"""
#         user_subscription = UserSubscription(**self.user_subscription_data)
#         user_subscription.status = 'invalid_status'
#
#         with self.assertRaises(ValidationError) as context:
#             user_subscription.full_clean()
#
#         error_messages = str(context.exception)
#         self.assertIn('status', error_messages,
#                       "Валидация должна возвращать ошибку для поля status при недопустимом значении")
#
#     def test_cascade_delete_user(self):
#         """Тест каскадного удаления при удалении пользователя"""
#         UserSubscription.objects.create(**self.user_subscription_data)
#         initial_count = UserSubscription.objects.count()
#
#         self.user.delete()
#         remaining_count = UserSubscription.objects.count()
#
#         self.assertEqual(remaining_count, initial_count - 1,
#                          f"После удаления пользователя должно остаться {initial_count - 1} пользовательских подписок, но осталось {remaining_count}")
#
#     def test_set_null_delete_subscription(self):
#         """Тест SET_NULL при удалении подписки"""
#         user_subscription = UserSubscription.objects.create(**self.user_subscription_data)
#
#         self.subscription.delete()
#         user_subscription.refresh_from_db()
#
#         self.assertIsNone(user_subscription.subscription,
#                           "После удаления подписки ссылка на подписку должна быть установлена в NULL")
#
#
# class VideoModelTest(TestCase):
#     """Тесты для модели Video"""
#
#     def setUp(self):
#         self.video_data = {
#             'title': 'Test Video',
#             'description': 'This is a test video description',
#             'file_path': '/videos/test.mp4',
#             'is_public': True,
#             'duration': '120.50',
#             'thumbnail_path': '/thumbnails/test.jpg'
#         }
#
#     def test_create_video(self):
#         """Тест создания видео"""
#         video = Video.objects.create(**self.video_data)
#
#         self.assertEqual(video.title, 'Test Video',
#                          "Название видео должно соответствовать переданному значению")
#         self.assertEqual(video.description, 'This is a test video description',
#                          "Описание видео должно соответствовать переданному значению")
#         self.assertEqual(video.file_path, '/videos/test.mp4',
#                          "Путь к файлу видео должен соответствовать переданному значению")
#         self.assertTrue(video.is_public,
#                         "Видео должно быть публичным по умолчанию")
#         self.assertEqual(float(video.duration), 120.50,
#                          "Длительность видео должна соответствовать переданному значению")
#         self.assertEqual(video.thumbnail_path, '/thumbnails/test.jpg',
#                          "Путь к thumbnail должен соответствовать переданному значению")
#
#     def test_video_str_representation(self):
#         """Тест строкового представления видео"""
#         video = Video.objects.create(**self.video_data)
#
#         if hasattr(video, '__str__'):
#             self.assertEqual(str(video), 'Test Video',
#                              "Строковое представление видео должно быть равно его названию")
#         else:
#             self.assertIsNotNone(video.id,
#                                  "Видео должно быть создано и иметь ID")
#
#
# class PaymentModelTest(TestCase):
#     """Тесты для модели Payment"""
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             phone='+79161234567',
#             password='testpass123'
#         )
#
#         self.subscription = Subscription.objects.create(
#             title='Premium',
#             price='999.99',
#             duration_days=30,
#             is_active=True
#         )
#
#         self.payment_data = {
#             'user': self.user,
#             'subscription': self.subscription,
#             'amount': '999.99',
#             'payment_date': datetime.now(),
#             'status': 'paid',
#             'payment_gateway_id': 'pg_12345',
#             'type': 'basic',
#             'currency': 'RUB'
#         }
#
#     def test_create_payment(self):
#         """Тест создания платежа"""
#         payment = Payment.objects.create(**self.payment_data)
#
#         self.assertEqual(payment.user, self.user,
#                          "Платеж должен ссылаться на правильного пользователя")
#         self.assertEqual(payment.subscription, self.subscription,
#                          "Платеж должен ссылаться на правильную подписку")
#         self.assertEqual(float(payment.amount), 999.99,
#                          "Сумма платежа должна соответствовать переданному значению")
#         self.assertEqual(payment.status, 'paid',
#                          "Статус платежа должен быть 'paid'")
#         self.assertEqual(payment.payment_gateway_id, 'pg_12345',
#                          "ID платежного шлюза должен соответствовать переданному значению")
#         self.assertEqual(payment.type, 'basic',
#                          "Тип платежа должен быть 'basic'")
#         self.assertEqual(payment.currency, 'RUB',
#                          "Валюта платежа должна быть 'RUB'")
#
#     def test_status_choices(self):
#         """Тест валидных статусов платежа"""
#         valid_statuses = ['paid', 'pending', 'declined', 'ready']
#
#         for status in valid_statuses:
#             with self.subTest(status=status):
#                 data = self.payment_data.copy()
#                 data['status'] = status
#                 payment = Payment.objects.create(**data)
#
#                 self.assertEqual(payment.status, status,
#                                  f"Статус должен быть '{status}', но получен '{payment.status}'")
#
#     def test_currency_choices(self):
#         """Тест валидных валют"""
#         valid_currencies = ['RUB', 'USD', 'EUR']
#
#         for currency in valid_currencies:
#             with self.subTest(currency=currency):
#                 data = self.payment_data.copy()
#                 data['currency'] = currency
#                 payment = Payment.objects.create(**data)
#
#                 self.assertEqual(payment.currency, currency,
#                                  f"Валюта должна быть '{currency}', но получена '{payment.currency}'")
#
#     def test_type_choices(self):
#         """Тест валидных типов подписки"""
#         data = self.payment_data.copy()
#         data['type'] = 'basic'
#         payment = Payment.objects.create(**data)
#
#         self.assertEqual(payment.type, 'basic',
#                          "Тип платежа должен быть 'basic'")
#
#     def test_cascade_delete_user(self):
#         """Тест каскадного удаления при удалении пользователя"""
#         Payment.objects.create(**self.payment_data)
#         initial_count = Payment.objects.count()
#
#         self.user.delete()
#         remaining_count = Payment.objects.count()
#
#         self.assertEqual(remaining_count, initial_count - 1,
#                          f"После удаления пользователя должно остаться {initial_count - 1} платежей, но осталось {remaining_count}")
#
#     def test_do_nothing_delete_subscription(self):
#         """Тест DO_NOTHING при удалении подписки"""
#         Payment.objects.create(**self.payment_data)
#         initial_count = Payment.objects.count()
#
#         try:
#             self.subscription.delete()
#             remaining_count = Payment.objects.count()
#
#             self.assertEqual(remaining_count, initial_count,
#                              f"После удаления подписки должно остаться {initial_count} платежей (DO_NOTHING), но осталось {remaining_count}")
#
#         except IntegrityError:
#             # Это ожидаемое поведение для некоторых БД
#             self.assertTrue(True, "IntegrityError ожидаема при DO_NOTHING с существующими связями")
#
#
# class ModelRelationshipsTest(TestCase):
#     """Тесты связей между моделями"""
#
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             phone='+79161234567',
#             password='testpass123'
#         )
#
#         self.subscription = Subscription.objects.create(
#             title='Premium',
#             price='999.99',
#             duration_days=30,
#             is_active=True
#         )
#
#     def test_user_subscription_relationship(self):
#         """Тест связи User - UserSubscription"""
#         user_subscription = UserSubscription.objects.create(
#             user=self.user,
#             subscription=self.subscription,
#             start_date=datetime.now(),
#             end_date=datetime.now() + timedelta(days=30),
#             status='active'
#         )
#
#         user_subscriptions_count = self.user.usersubscription_set.count()
#         self.assertEqual(user_subscriptions_count, 1,
#                          f"Пользователь должен иметь 1 подписку, но имеет {user_subscriptions_count}")
#
#         self.assertEqual(self.user.usersubscription_set.first(), user_subscription,
#                          "Первая подписка пользователя должна быть созданной подпиской")
#
#     def test_subscription_user_subscription_relationship(self):
#         """Тест связи Subscription - UserSubscription"""
#         user_subscription = UserSubscription.objects.create(
#             user=self.user,
#             subscription=self.subscription,
#             start_date=datetime.now(),
#             end_date=datetime.now() + timedelta(days=30),
#             status='active'
#         )
#
#         subscription_users_count = self.subscription.usersubscription_set.count()
#         self.assertEqual(subscription_users_count, 1,
#                          f"Подписка должна иметь 1 пользователя, но имеет {subscription_users_count}")
#
#         self.assertEqual(self.subscription.usersubscription_set.first(), user_subscription,
#                          "Первый пользователь подписки должен быть созданным пользователем")
#
#     def test_user_payment_relationship(self):
#         """Тест связи User - Payment"""
#         payment = Payment.objects.create(
#             user=self.user,
#             subscription=self.subscription,
#             amount='999.99',
#             payment_date=datetime.now(),
#             status='paid'
#         )
#
#         user_payments_count = self.user.payment_set.count()
#         self.assertEqual(user_payments_count, 1,
#                          f"Пользователь должен иметь 1 платеж, но имеет {user_payments_count}")
#
#         self.assertEqual(self.user.payment_set.first(), payment,
#                          "Первый платеж пользователя должен быть созданным платежом")
#
#     def test_subscription_payment_relationship(self):
#         """Тест связи Subscription - Payment"""
#         payment = Payment.objects.create(
#             user=self.user,
#             subscription=self.subscription,
#             amount='999.99',
#             payment_date=datetime.now(),
#             status='paid'
#         )
#
#         subscription_payments_count = self.subscription.payment_set.count()
#         self.assertEqual(subscription_payments_count, 1,
#                          f"Подписка должна иметь 1 платеж, но имеет {subscription_payments_count}")
#
#         self.assertEqual(self.subscription.payment_set.first(), payment,
#                          "Первый платеж подписки должен быть созданным платежом")
#
#
# class SoftDeleteManagerTest(TestCase):
#     """Тесты для менеджера мягкого удаления"""
#
#     def test_soft_delete_manager(self):
#         """Тест работы менеджера мягкого удаления"""
#         # Создаем активную подписку
#         active_sub = Subscription.objects.create(
#             title='Active',
#             price='100.00',
#             duration_days=30,
#             is_active=True
#         )
#
#         # Создаем удаленную подписку
#         deleted_sub = Subscription.objects.create(
#             title='Deleted',
#             price='200.00',
#             duration_days=30,
#             is_active=True
#         )
#         deleted_sub.delete()
#
#         # Проверяем, что менеджер возвращает только активные записи
#         remaining_count = Subscription.objects.count()
#         self.assertEqual(remaining_count, 1,
#                          f"Менеджер должен возвращать 1 активную подписку, но возвращает {remaining_count}")
#
#         remaining_subscription = Subscription.objects.first()
#         self.assertEqual(remaining_subscription.title, 'Active',
#                          "Оставшаяся подписка должна быть 'Active'")
#
#         # Проверяем, что все записи есть в базовом менеджере
#         all_count = Subscription._base_manager.count()
#         self.assertEqual(all_count, 2,
#                          f"Базовый менеджер должен возвращать 2 подписки, но возвращает {all_count}")