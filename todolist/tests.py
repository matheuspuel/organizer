from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from . import models


class TestViewsAnonymous(TestCase):

    def test_render(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200, 'Login page should be accessible')
        self.assertTemplateUsed(response, 'login.html', 'Should render template login.html')

    def test_404(self):
        response = self.client.get('/lsdfjkdskfjsdklfj')
        self.assertEquals(response.status_code, 404, 'Incorrect URL should return 404 error')

    def test_redirect(self):
        response = self.client.get(reverse('task_list'))
        self.assertNotEquals(response.status_code, 200, 'Task List page should not be accessible')
        self.assertEquals(response.status_code, 302, 'Should redirect')

        response = self.client.get(response.url)
        self.assertEquals(response.status_code, 200, 'Should be accessible')
        self.assertTemplateUsed(response, 'login.html', 'Should render template login.html')


class TestViewsUser(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='123456')
        self.client.login(username='user1', password='123456')

    def test_list(self):
        response = self.client.get(reverse('task_list'))
        self.assertEquals(response.status_code, 200, 'Task List page should be accessible')
        self.assertTemplateUsed(response, 'todolist/task_list.html', 'Should render template')

    def test_detail(self):
        task1 = models.Task.objects.create(title='task1', user=self.user1)
        response = self.client.get(reverse('task_detail', kwargs=dict(pk=task1.id)))
        self.assertEquals(response.status_code, 200, 'Task List page should be accessible')
        self.assertTemplateUsed(response, 'todolist/task_detail.html', 'Should render template')

    def test_detail_404(self):
        response = self.client.get(reverse('task_detail', kwargs=dict(pk=1)))
        self.assertEquals(response.status_code, 404, 'Should not be found')

    def test_detail_block(self):
        user2 = User.objects.create_user(username='user2', password='123456')
        task1 = models.Task.objects.create(title='task1', user=user2)
        response = self.client.get(reverse('task_detail', kwargs=dict(pk=task1.id)))
        self.assertEquals(response.status_code, 404, 'Should be blocked')






