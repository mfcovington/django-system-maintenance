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

    def system_maintenance_url(self, url_stem=''):
        return '{}/system_maintenance/{}'.format(
            self.live_server_url, url_stem)

    def test_can_login_as_sysadmin(self):
        # Try to go to the System Maintenance homepage
        self.browser.get(self.system_maintenance_url())


        # Not logged in, so get redirected to the SysAdmin Authentication page
        self.assertIn('System Maintenance', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('SysAdmin Authentication', header_text)


        # See input boxes for username & password
        self.find_authentication_elements()

        self.assertEqual(
            self.username_inputbox.get_attribute('placeholder'),
            'Enter username')

        self.assertEqual(
            self.password_inputbox.get_attribute('placeholder'),
            'Enter password')

        self.assertEqual(self.login_button.text, 'Login')


        # Accidentally click 'Login' button without entering credentials
        self.login_button.click()


        # See two error messages about required fields
        field_errors = self.browser.find_elements_by_class_name('field-error')
        self.assertEqual(len(field_errors), 2)
        for error in field_errors:
            self.assertEqual(error.text, 'This field is required.')


        # Enter incorrect credentials
        self.find_authentication_elements()

        self.username_inputbox.send_keys('nobody')
        self.password_inputbox.send_keys('nobody')


        # Hit 'Enter' key to submit
        self.password_inputbox.send_keys(Keys.ENTER)


        # See error message about entering correct username and password
        self.assertIn(
            'Please enter a correct username and password. Note that both ' +
            'fields may be case-sensitive.',
            self.browser.find_element_by_class_name('alert-danger').text)


        # Enter non-sysadmin credentials
        self.find_authentication_elements()

        self.username_inputbox.send_keys('nonsysadmin')
        self.password_inputbox.send_keys('nonsysadmin' + Keys.ENTER)


        # See 'Access denied.' message about not being a sys admin
        self.assertIn(
            'Access denied.', self.browser.find_element_by_tag_name('h1').text)
        self.assertIn(
            'Hello nonsysadmin. You are not a system administrator.',
            self.browser.find_element_by_tag_name('p').text)

        # 'Previous Page' button.

        # Click 'Logout' button and get redirected to authentication page.
        self.logout_button = self.browser.find_element_by_tag_name('a')
        self.logout_button.click()


        # Enter sysadmin credentials
        self.find_authentication_elements()

        self.username_inputbox.send_keys('sysadmin')
        self.password_inputbox.send_keys('sysadmin' + Keys.ENTER)

        # Check that redirected to System Maintenance home page
        self.assertIn('System Maintenance', self.browser.title)
        self.assertEqual(
            self.browser.find_element_by_tag_name('p').text,
            'System maintenance records and other important system '
            'administration information is accessible via the buttons below.')

        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(
                '.btn.full-width-on-mobile')), 7)
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(
                '.btn-group.hide-on-mobile > .btn')), 7)


        # Logout
        self.browser.get(self.system_maintenance_url('logout'))


        # Enter superuser sysadmin credentials
        self.find_authentication_elements()

        self.username_inputbox.send_keys('supersysadmin')
        self.password_inputbox.send_keys('supersysadmin' + Keys.ENTER)


        # Check that redirected to System Maintenance home page w/ admin access
        self.assertIn('System Maintenance', self.browser.title)
        paragraphs = self.browser.find_elements_by_tag_name('p')
        self.assertIn('System maintenance records and ', paragraphs[0].text)
        self.assertIn('To add or change system ', paragraphs[1].text)

        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(
                '.btn.full-width-on-mobile')), 7)
        self.assertEqual(
            len(self.browser.find_elements_by_css_selector(
                '.btn-group.hide-on-mobile > .btn')), 14)