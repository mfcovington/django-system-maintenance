from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_app_home_title(self):
        self.browser.get('http://localhost:8000/system_maintenance')
        self.assertIn('System Maintenance', self.browser.title)
