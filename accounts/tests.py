from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='1qaz@WSX123')
        assert user.id, 'У пользователя не назначен id. Запись отсутствует в базе данных!'
        assert not user.is_superuser, 'Пользователь не должен иметь прав суперпользователя!'
        assert not user.is_staff, 'Пользователь не должен иметь прав персонала!'

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='test@example.com', password='1qaz@WSX123')
        assert superuser.id, 'У пользователя не назначен id. Запись отсутствует в базе данных!'
        assert superuser.is_superuser, 'Пользователь должен иметь права суперпользователя!'
        assert superuser.is_staff, 'Пользователь должен иметь права персонала!'
