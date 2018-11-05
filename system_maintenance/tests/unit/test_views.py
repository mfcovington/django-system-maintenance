import re

from django.contrib.auth import views as auth_views
from django.urls import resolve, reverse
from django.template.loader import render_to_string
from django.test import TestCase

from system_maintenance import views
from system_maintenance.models import DocumentationRecord, MaintenanceRecord
from system_maintenance.tests.utilities import (
    CustomAssertions, login_normal_user, login_sysadmin_superuser,
    login_sysadmin_user, populate_test_db)


class CommonViewTests:

    """
    A mixin consisting of a set of tests that are common to multiple views.

    Unless these tests are overridden, a `TestCase` that uses this mixin must
    define a set of view-specific variables in the `setUp()` method similar
    to this:

        def setUp(self):
            populate_test_db()
            login_sysadmin_user(self)

            self.namespace = 'system_maintenance:documentation_record_list'
            self.template = 'system_maintenance/documentation_record_list.html'
            self.title = 'Documentation Records'
            self.url = '/system_maintenance/documentation/'
            self.view = views.DocumentationRecordListView

            self.get_response()
    """

    def get_response(self):
        """
        Get response based on URL.
        """
        self.response = self.client.get(self.url)

    def test_namespace_reverses_to_url(self):
        """
        Test that a given namespace reverses to the correct URL.
        """
        self.assertEqual(reverse(self.namespace), self.url)

    def test_url_resolves_to_view(self):
        """
        Test that a given URL resolves to the correct view.
        """
        found = resolve(self.url)
        found_name = found.func.__name__
        self.assertEqual(found_name, getattr(self.view, '__name__', None))

    def test_view_uses_correct_template(self):
        """
        Test that view's response uses the correct template
        """
        self.assertTemplateUsed(self.response, self.template)

    def test_view_returns_correct_title(self):
        """
        Test that view's response contains the correct page title.
        """
        self.assertContains(
            self.response, '<title>{}</title>'.format(self.title))

    def test_view_returns_static_files_links(self):
        """
        Test that view's response contains links to the correct static files.
        """
        static_files = [
            'bootstrap.min.css',
            'bootstrap.min.js',
            'jquery.min.js',
            '/static/system_maintenance/css/app.css',
            '/static/system_maintenance/js/app.js',
        ]
        for static in static_files:
            self.assertContains(self.response, static)

    def test_view_returns_correct_html(self):
        """
        Test that a view's response contains the correct HTML based on the
        template.
        """
        self.assertEqual(self.response.status_code, 200)

        # CSRF tokens don't get render_to_string'd
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        observed_html = re.sub(csrf_regex, '', self.response.content.decode())

        try:
            context = self.context
        except AttributeError:
            context = {}

        expected_html = render_to_string(self.template, context)

        self.assertEqual(observed_html, expected_html)


class RedirectAnonymousUserToAuthenticationTest(TestCase, CustomAssertions):

    def test_system_maintenance_home_view(self):
        self.assertRedirectUserToAuthentication(
            'system_maintenance:system_maintenance_home_view')

    def test_documentation_record_list(self):
        self.assertRedirectUserToAuthentication(
            'system_maintenance:documentation_record_list')


class RedirectNonSysAdminUserToAuthenticationTest(TestCase, CustomAssertions):

    def setUp(self):
        populate_test_db()
        login_normal_user(self)

    def test_system_maintenance_home_view(self):
        self.assertRedirectUserToAuthentication(
            'system_maintenance:system_maintenance_home_view')

    def test_documentation_record_list(self):
        self.assertRedirectUserToAuthentication(
            'system_maintenance:documentation_record_list')


class AuthenticationViewTest(TestCase, CommonViewTests):

    def setUp(self):
        self.namespace = 'system_maintenance:authentication'
        self.template = 'system_maintenance/authentication.html'
        self.title = 'System Maintenance'
        self.url = '/system_maintenance/authentication/'

        self.get_response()

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(
            found.func.view_class().template_name,
            auth_views.LoginView.as_view().view_class().template_name)


class HomeViewTest(TestCase, CommonViewTests):

    def setUp(self):
        populate_test_db()
        login_sysadmin_user(self)

        self.namespace = 'system_maintenance:system_maintenance_home_view'
        self.template = 'system_maintenance/system_maintenance_home.html'
        self.title = 'System Maintenance'
        self.url = '/system_maintenance/'

        self.get_response()

    def test_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, views.system_maintenance_home_view)

    def test_view_returns_correct_html(self):
        """
        Test that normal system administrators have links to System
        Maintenance pages, but not admin pages.
        """
        self.assertEqual(self.response.status_code, 200)

        app_urls = [
            'records/',
            'documentation/',
        ]
        for url in app_urls:
            self.assertContains(
                self.response, '/system_maintenance/{}'.format(url))

        self.assertContains(
            self.response, 'System maintenance records and other important ' +
            'system administration information is accessible via the ' +
            'buttons below.')

        unexpected_superuser_only_content = [
            'System Maintenance Admin Page',
            '/admin/system_maintenance/',
            'glyphicon-wrench',
        ]
        for content in unexpected_superuser_only_content:
            self.assertNotContains(self.response, content)

    def test_view_returns_correct_html_for_superuser_sysadmin(self):
        """
        Test that superuser system administrators have links to System
        Maintenance admin pages.
        """
        login_sysadmin_superuser(self)
        self.get_response()
        self.assertEqual(self.response.status_code, 200)

        model_names = [
            'documentationrecord',
            'hardware',
            'maintenancerecord',
            'maintenancetype',
            'software',
            'sysadmin',
            'system',
        ]
        for model in model_names:
            self.assertContains(
                self.response, '/admin/system_maintenance/{}/'.format(model))

        self.assertContains(self.response, 'System Maintenance Admin Page')
        self.assertContains(self.response, 'glyphicon-wrench')


class DocumentationRecordListViewTest(TestCase, CommonViewTests):

    def setUp(self):
        populate_test_db()
        login_sysadmin_user(self)

        self.namespace = 'system_maintenance:documentation_record_list'
        self.template = 'system_maintenance/documentation_record_list.html'
        self.title = 'Documentation Records'
        self.url = '/system_maintenance/documentation/'
        self.view = views.DocumentationRecordListView

        self.get_response()

        self.context = {
            'object_list': DocumentationRecord.objects.all(),
        }


class MaintenanceRecordListViewTest(TestCase, CommonViewTests):

    def setUp(self):
        populate_test_db()
        login_sysadmin_user(self)

        self.namespace = 'system_maintenance:maintenance_record_list'
        self.template = 'system_maintenance/maintenance_record_list.html'
        self.title = 'Maintenance Records'
        self.url = '/system_maintenance/records/'
        self.view = views.MaintenanceRecordListView

        self.get_response()

        self.context = {
            'object_list': MaintenanceRecord.objects.all(),
        }
