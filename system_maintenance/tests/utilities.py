from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from system_maintenance.models import SysAdmin


class CustomAssertions:

    """
    A mixin consisting of custom assertions.

    Use with a `TestCase` like this:

        from system_maintenance.tests.utilities import CustomAssertions

        class SomeTest(TestCase, CustomAssertions):
            ...
    """

    def assertRedirectUserToAuthentication(self, namespace):
        """
        Take a namespace, get the corresponding URL, and test whether
        it redirects to the System Maintenance authentication page
        (with the original URL as the 'next' page).
        """
        auth_url = reverse('system_maintenance:authentication')
        url = reverse(namespace)
        response = self.client.get(url)
        self.assertRedirects(response, '{}?next={}'.format(auth_url, url))


def populate_test_db():
    """
    Add records to an empty test database.
    """
    User.objects.create_user(username='nonsysadmin', password='nonsysadmin')

    sysadmin = User.objects.create_user(
        username='sysadmin', password='sysadmin')
    SysAdmin.objects.create(user=sysadmin)

    supersysadmin = User.objects.create_superuser(
        username='supersysadmin', password='supersysadmin',
        email='supersysadmin@supersysadmin')
    SysAdmin.objects.create(user=supersysadmin)


def login_normal_user(self):
    """
    Login as a normal user.
    """
    self.client.login(username='nonsysadmin', password='nonsysadmin')
    return self


def login_sysadmin_user(self):
    """
    Login as a sysadmin user.
    """
    self.client.login(username='sysadmin', password='sysadmin')
    return self


def login_sysadmin_superuser(self):
    """
    Login as a sysadmin superuser.
    """
    self.client.login(username='supersysadmin', password='supersysadmin')
    return self
