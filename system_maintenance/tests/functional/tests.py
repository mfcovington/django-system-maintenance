from selenium import webdriver
import unittest


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_app_home_title(self):
        self.browser.get('http://localhost:8000/system_maintenance')
        self.assertIn('System Maintenance', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
