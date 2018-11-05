from .base import FunctionalTest


class AuthenticationTest(FunctionalTest):

    def test_anon_user_redirected_to_authentication(self):
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

    def test_username_and_password_required(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))

        # Accidentally click 'Login' button without entering credentials
        self.find_authentication_elements()
        self.login_button.click()

        # See two error messages about required fields
        form_errors = self.browser.find_elements_by_class_name('has-error')
        self.assertEqual(len(form_errors), 2)
        for error in form_errors:
            self.assertIn('This field is required.', error.text)

    def test_incorrect_credentials_raise_error(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))

        # Enter incorrect credentials
        self.login_as('nobody')

        # See error message about entering correct username and password
        self.assertIn(
            'Please enter a correct username and password. Note that both ' +
            'fields may be case-sensitive.',
            self.browser.find_element_by_class_name('alert-danger').text)

    def test_nonsysadmin_is_denied_access_and_can_logout(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))

        # Enter non-sysadmin credentials
        self.login_as('nonsysadmin')

        # See 'Access denied.' message about not being a sys admin
        self.assertIn(
            'Access denied.', self.browser.find_element_by_tag_name('h1').text)
        self.assertIn(
            'Hello nonsysadmin. You are not a system administrator.',
            self.browser.find_element_by_tag_name('p').text)

        # Click 'Logout' button and get redirected to authentication page.
        self.logout_button = self.browser.find_element_by_tag_name('a')
        self.logout_button.click()

    def test_can_login_as_sysadmin_and_can_logout(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))

        # Enter sysadmin credentials
        self.login_as('sysadmin')

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

        # Logout and get redirected to SysAdmin Authentication page
        self.browser.get(self.system_maintenance_url('logout'))
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('SysAdmin Authentication', header_text)

    def test_can_login_as_super_sysadmin(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))

        # Enter superuser sysadmin credentials
        self.login_as('supersysadmin')

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
