from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.db.utils import IntegrityError
from django.shortcuts import reverse
from django.utils import lorem_ipsum

User = get_user_model()


class TestModels(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(email='test@example.com', password='1qaz@WSX')

    def test_post_model_unique_title(self):
        post_1 = Post.objects.create(
            title='test_title',
            author=self.author,
            body='test'
        )
        try:
            post_2 = Post.objects.create(
                title='test_title',
                author=self.author,
                body='test'
            )
            assert not post_2.id, 'Второй пост создался с таким же title!'
        except Exception as e:
            assert isinstance(e, IntegrityError), 'Ошибка не IntegrityError!'

        assert post_1.id, 'Первый пост не создался!'

    def test_comment_model(self):
        post = Post.objects.create(
            title='test_title',
            author=self.author,
            body='test'
        )
        assert post.id, 'Пост не создался!'
        comment = Comment.objects.create(
            post=post,
            author=self.author,
            body='test 12345'
        )
        assert comment.id, 'Комментарий не создан!'
        assert post.comments.all().count(), 'Комментарий не привязался к посту!'


class TestUserPermissions(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_1 = User.objects.create_user(email='test_1@example.com', password='1qaz@WSX')
        cls.author_2 = User.objects.create_user(email='test_2@example.com', password='1qaz@WSX')
        cls.client = Client()

    def test_post_create(self):
        response = self.client.get(reverse('blog:create'))
        assert response.status_code == 302, 'Неавторизованный пользователь не был перенаправлен на страницу логина!'
        self.client.force_login(self.author_1)
        authorized_response = self.client.get(reverse('blog:create'))
        assert authorized_response.status_code == 200, 'Авторизованному пользователю недоступна ' \
                                                       'страница создания поста!'
        test_body = lorem_ipsum.paragraph()
        create_response = self.client.post(
            reverse('blog:create'),
            data={
                'title': 'test_title',
                'body': test_body
            }
        )
        assert create_response.status_code == 302, 'Пользователь не перенаправлен на главную страницу!'
        post = Post.objects.last()
        assert post.title == 'test_title', 'Заголовок поста не совпадает!'
        assert post.body == test_body, 'Содержимое поста не совпадает!'
        assert not post.published, 'Пост опубликован несмотря на значение по умолчанию!'

    def test_post_edit(self):
        test_body = lorem_ipsum.paragraph()
        test_post = Post.objects.create(
            title='test_title',
            body=test_body,
            author=self.author_1
        )
        author_1_client = Client()
        author_1_client.force_login(self.author_1)

        author_1_get_response = author_1_client.get(reverse('blog:update', kwargs={'pk': test_post.id}))
        assert author_1_get_response.status_code == 200, 'Код ответа не 200!'
        author_1_post_response = author_1_client.post(
            reverse('blog:update', kwargs={'pk': test_post.id}),
            data={
                'title': 'new_title',
                'body': test_body,
                'published': True
            }
        )
        assert author_1_post_response.status_code == 302, 'Пользователь не перенаправлен после обновления поста!'
        test_post.refresh_from_db()

        assert test_post.title == 'new_title', f'Заголовок не поменялся! Текущее значение: {test_post.title}'
        assert test_post.body == test_body, 'Содержимое поста изменилось!'
        assert test_post.published, 'Пост не опубликовался!'

        author_2_client = Client()
        author_2_client.force_login(self.author_2)

        author_2_get_response = author_2_client.get(reverse('blog:update', kwargs={'pk': test_post.id}))
        get_status_code = author_2_get_response.status_code
        assert get_status_code == 302, f'Пользователь не был перенаправлен! Код ответа: {get_status_code}'
        author_2_post_response = author_2_client.post(
            reverse('blog:update', kwargs={'pk': test_post.id}),
            data={
                'title': 'new_title',
                'body': 'wipe_body',
                'published': True
            }
        )
        post_status_code = author_2_post_response.status_code
        assert post_status_code == 302, f'Пользователь не был перенаправлен! Код ответа: {post_status_code}'

    def test_post_list(self):
        Post.objects.bulk_create([
            Post(title='test1', author=self.author_1, body=lorem_ipsum.paragraph(), published=True),
            Post(title='test2', author=self.author_2, body=lorem_ipsum.paragraph(), published=True),
            Post(title='test3', author=self.author_1, body=lorem_ipsum.paragraph(), published=False)
        ])
        published_posts = Post.objects.filter(published=True)
        response = self.client.get(reverse('blog:list'))
        assert response.status_code == 200, 'Код ответа не 200!'
        assert len(response.context['page_obj']) == published_posts.count(), 'Количество отображаемых постов ' \
                                                                             'неправильно!'

    def test_post_detail(self):
        post = Post.objects.create(title='test1', author=self.author_1, body=lorem_ipsum.paragraph(), published=True)
        response = self.client.get(reverse('blog:detail', kwargs={'pk': post.id}))
        assert response.status_code == 200, 'Код ответа не 200!'
        assert response.context['post'] == post, 'Неверный объект в контексте!'
