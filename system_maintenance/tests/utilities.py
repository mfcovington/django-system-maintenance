from django.contrib.auth.models import User
from django.urls import reverse

from system_maintenance.models import (
    DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceRecordRelationship, MaintenanceType, Software, SysAdmin, System)


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
    Returns a dict of the saved objects.
    """
    User.objects.create_user(username='nonsysadmin', password='nonsysadmin')

    sysadmin_user = User.objects.create_user(
        username='sysadmin', password='sysadmin')
    sysadmin = SysAdmin.objects.create(user=sysadmin_user)

    supersysadmin_user = User.objects.create_superuser(
        username='supersysadmin', password='supersysadmin',
        email='supersysadmin@supersysadmin')
    supersysadmin = SysAdmin.objects.create(user=supersysadmin_user)

    maintenance_type_1 = MaintenanceType.objects.create(
        maintenance_type='Maintenance Type 1')
    maintenance_type_2 = MaintenanceType.objects.create(
        maintenance_type='Maintenance Type 2')

    documentation_record_1 = DocumentationRecord.objects.create(
        title='Documentation 1',
        maintenance_type=maintenance_type_1,
        documentation='',
    )
    documentation_record_2 = DocumentationRecord.objects.create(
        title='Documentation 2',
        maintenance_type=maintenance_type_2,
        documentation='',
    )

    hardware = Hardware.objects.create(name='Hardware 1')
    software = Software.objects.create(name='Software 1')
    system = System.objects.create(name='System 1')

    maintenance_record_1 = MaintenanceRecord.objects.create(
        system=system,
        sys_admin=sysadmin,
        maintenance_type=maintenance_type_1,
        description='',
        procedure='',
        problems='',
    )
    maintenance_record_1.hardware.add(hardware)

    maintenance_record_2 = MaintenanceRecord.objects.create(
        system=system,
        sys_admin=supersysadmin,
        maintenance_type=maintenance_type_2,
        description='',
        procedure='',
        problems='',
        status='Complete',
    )
    maintenance_record_2.software.add(software)
    maintenance_record_2.documentation_records.add(documentation_record_1)
    maintenance_record_2.documentation_records.add(documentation_record_2)

    MaintenanceRecordRelationship.objects.create(
        referenced_record=maintenance_record_1,
        referencing_record=maintenance_record_2,
    )

    maintenance_record_3 = MaintenanceRecord.objects.create(
        system=system,
        sys_admin=sysadmin,
        maintenance_type=maintenance_type_1,
        status='Failed',
    )
    maintenance_record_3.hardware.add(hardware)
    maintenance_record_3.software.add(software)

    db_objects = {
        'documentation_record_1': documentation_record_1,
        'documentation_record_2': documentation_record_2,
        'hardware': hardware,
        'maintenance_record_1': maintenance_record_1,
        'maintenance_record_2': maintenance_record_2,
        'maintenance_record_3': maintenance_record_3,
        'maintenance_type_1': maintenance_type_1,
        'maintenance_type_2': maintenance_type_2,
        'software': software,
        'supersysadmin': supersysadmin,
        'system': system,
        'sysadmin': sysadmin,
    }

    return db_objects


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
