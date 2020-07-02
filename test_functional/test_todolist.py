from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

from django.contrib.auth.models import User
from todolist import models


class TestFunctionalFirst(StaticLiveServerTestCase):
    def setUp(self):
        # self.browser = webdriver.Chrome('test_functional/chromedriver_windows.exe')
        self.browser = webdriver.Chrome('test_functional/chromedriver_linux')

    # def tearDown(self):
    #     self.browser.close()

    def test_login_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('login', self.browser.current_url, 'Should have "login" in url')

        User.objects.create_user(username='user1', password='123456')
        self.browser.find_element_by_name('username').send_keys('user1')
        self.browser.find_element_by_name('password').send_keys('123456')
        self.browser.find_element_by_tag_name('form').submit()
        self.assertIn(reverse('task_list'), self.browser.current_url, 'Should be in task_list')
        self.assertNotIn('?next', self.browser.current_url, 'Should not have "?next" in url')

