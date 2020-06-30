from django.test import TestCase, SimpleTestCase
from django.urls import reverse


# class TestTest(SimpleTestCase):
#     def test_first_test(self):
#         assert 2 == 2, 'My first test'
#         assert 1 == 1, 'My sec test'
#
#     def test_second_test(self):
#         assert 1 == 1
#
#
# class TestSecType(TestCase):
#     def setUp(self):
#         self.a = 1
#
#     def test_one(self):
#         self.assertEquals(self.a, 1, 'Should be right')


class TestViews(TestCase):

    def test_response(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200, 'Login page should be accessible')

    def test_404(self):
        response = self.client.get('/lsdfjkdskfjsdklfj')
        self.assertEquals(response.status_code, 404, 'Incorrect URL should return 404 error')

    def test_ci_cd(self):
        self.assertTrue(False, 'Testing Heroku CI/CD')



