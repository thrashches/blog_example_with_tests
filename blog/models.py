from django.db import models


class Post(models.Model):
    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    title = models.CharField(max_length=255, verbose_name='название поста', unique=True)
    body = models.TextField(verbose_name='текст поста')
    author = models.ForeignKey('accounts.Blogger', on_delete=models.CASCADE, verbose_name='автор')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    published = models.BooleanField(default=False, verbose_name='опубликовано')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='пост')
    body = models.TextField(verbose_name='текст комментария')
    author = models.ForeignKey('accounts.Blogger', on_delete=models.CASCADE, verbose_name='автор')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title}|comment: {self.id}'
