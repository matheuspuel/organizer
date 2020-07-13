from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class TestFunctionalFirst(StaticLiveServerTestCase):
    def setUp(self):
        if settings.LOCAL_TEST:
            self.browser = webdriver.Chrome('test_functional/chromedriver.exe')
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.browser = webdriver.Chrome('/home/travis/virtualenv/python3.6/bin/chromedriver',
                                            chrome_options=chrome_options)

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
