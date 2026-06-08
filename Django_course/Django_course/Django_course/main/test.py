from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import News, Comment

class NewsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='123')
        self.news = News.objects.create(
            title='Тестовая новость',
            content='Содержание тестовой новости',
            author=self.user
        )

    def test_news_creation(self):

        self.assertEqual(self.news.title, 'Тестовая новость')
        self.assertEqual(str(self.news), 'Тестовая новость')

    def test_news_ordering(self):

        news2 = News.objects.create(
            title='Вторая новость',
            content='Содержание',
            author=self.user
        )
        news_list = list(News.objects.all())
        self.assertEqual(news_list[0].title, 'Вторая новость')  # новая сверху

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='12345')
        self.news = News.objects.create(
            title='Новость для комментариев',
            content='Контент',
            author=self.user
        )
        self.comment = Comment.objects.create(
            news=self.news,
            user=self.user,
            text='Отличная новость!'
        )

    def test_comment_creation(self):

        self.assertEqual(self.comment.text, 'Отличная новость!')
        self.assertEqual(str(self.comment), 'commenter - Новость для комментариев')

    def test_comment_has_required_fields(self):

        self.assertTrue(hasattr(self.comment, 'news'))
        self.assertTrue(hasattr(self.comment, 'user'))
        self.assertTrue(hasattr(self.comment, 'text'))
        self.assertTrue(hasattr(self.comment, 'created_at'))

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewer', password='testpass')
        self.news = News.objects.create(
            title='Просматриваемая новость',
            content='Текст',
            author=self.user
        )

    def test_home_page_status(self):

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_news_list_page(self):

        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_news_detail_page(self):

        response = self.client.get(reverse('news_detail', args=[self.news.id]))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):

        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())