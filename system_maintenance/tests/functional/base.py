from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from system_maintenance.tests.utilities import populate_test_db


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        populate_test_db()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        self.username_inputbox = None
        self.password_inputbox = None
        self.login_button = None

    def tearDown(self):
        self.browser.quit()

    def find_authentication_elements(self):
        self.username_inputbox = self.browser.find_element_by_id('id_username')
        self.password_inputbox = self.browser.find_element_by_id('id_password')
        self.login_button = self.browser.find_element_by_tag_name('button')

    def login_as(self, username):
        self.find_authentication_elements()
        self.username_inputbox.send_keys(username)
        self.password_inputbox.send_keys(username)
        self.login_button.click()

    def system_maintenance_url(self, url_stem=''):
        return '{}/system_maintenance/{}'.format(
            self.live_server_url, url_stem)
