from selenium.webdriver.support.color import Color

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_authentication(self):
        # Go to the authentication page
        self.browser.get(self.system_maintenance_url('authentication'))
        window_width = 768
        self.browser.set_window_size(window_width, window_width / 2)

        # Username and password input boxes are centered
        self.find_authentication_elements()
        center_username = self.username_inputbox.location['x'] + \
            self.username_inputbox.size['width'] / 2
        center_password = self.password_inputbox.location['x'] + \
            self.password_inputbox.size['width'] / 2
        self.assertAlmostEqual(center_username, window_width / 2, delta=5)
        self.assertAlmostEqual(center_password, window_width / 2, delta=5)

    def test_maintenance_record_list(self):
        # Sign in as sysadmin and go to Maintenance Records
        self.browser.get(self.system_maintenance_url('records'))
        self.login_as('sysadmin')

        # See, based on the color-coded backgrounds, that the status of the
        # first record is 'Failed', the second is 'Complete', and the third is
        # 'In Progress'
        list_group_items = self.browser.find_elements_by_class_name(
            'list-group-item')
        background_colors = ['#f2dede', '#ffffff', '#fcf8e3']

        self.assertEqual(len(list_group_items), 3)
        for item, color in zip(list_group_items, background_colors):
            self.assertEqual(Color.from_string(
                item.value_of_css_property('background-color')).hex, color)
