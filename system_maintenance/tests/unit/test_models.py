from django.core.exceptions import ValidationError
from django.test import TestCase

from system_maintenance.models import (
    DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceRecordRelationship, MaintenanceType, Software, SysAdmin, System)
from system_maintenance.tests.utilities import populate_test_db


class MaintenanceRecordRelationshipTest(TestCase):

    def setUp(self):
        self.db_objects = populate_test_db()

    def test_cannot_save_relationship_to_self(self):
        record = self.db_objects['maintenance_record_1']
        relationship = MaintenanceRecordRelationship(
            referenced_record=record,
            referencing_record=record,
        )

        with self.assertRaises(ValidationError):
            relationship.save()
            relationship.full_clean()


class SaveAndRetrieveTests(TestCase):

    """
    Test that objects created by `populate_test_db()` can be retrieved from
    the database.
    """

    def setUp(self):
        self.db_objects = populate_test_db()

    def test_save_and_retrieve_documentation_records(self):
        records = DocumentationRecord.objects.all()

        self.assertEqual(records.count(), 2)
        self.assertEqual(records[0], self.db_objects['documentation_record_1'])
        self.assertEqual(records[1], self.db_objects['documentation_record_2'])

    def test_save_and_retrieve_hardwares(self):
        hardwares = Hardware.objects.all()

        self.assertEqual(hardwares.count(), 1)
        self.assertEqual(hardwares[0], self.db_objects['hardware'])

    def test_save_and_retrieve_maintenance_records(self):
        # Maintenance Records are in reverse chronological order
        records = MaintenanceRecord.objects.all()

        self.assertEqual(records.count(), 3)
        self.assertEqual(records[0], self.db_objects['maintenance_record_3'])
        self.assertEqual(records[1], self.db_objects['maintenance_record_2'])
        self.assertEqual(records[2], self.db_objects['maintenance_record_1'])

    def test_save_and_retrieve_maintenance_record_relationships(self):
        relationships = MaintenanceRecordRelationship.objects.all()

        self.assertEqual(relationships.count(), 1)
        self.assertEqual(
            relationships[0].referenced_record,
            self.db_objects['maintenance_record_1'])
        self.assertEqual(
            relationships[0].referencing_record,
            self.db_objects['maintenance_record_2'])

    def test_save_and_retrieve_maintenance_types(self):
        maintenance_types = MaintenanceType.objects.all()

        self.assertEqual(maintenance_types.count(), 2)
        self.assertEqual(
            maintenance_types[0], self.db_objects['maintenance_type_1'])
        self.assertEqual(
            maintenance_types[1], self.db_objects['maintenance_type_2'])

    def test_save_and_retrieve_softwares(self):
        softwares = Software.objects.all()

        self.assertEqual(softwares.count(), 1)
        self.assertEqual(softwares[0], self.db_objects['software'])

    def test_save_and_retrieve_sysadmins(self):
        sysadmins = SysAdmin.objects.all()

        self.assertEqual(sysadmins.count(), 2)
        self.assertEqual(sysadmins[0], self.db_objects['sysadmin'])
        self.assertEqual(sysadmins[1], self.db_objects['supersysadmin'])

    def test_save_and_retrieve_systems(self):
        systems = System.objects.all()

        self.assertEqual(systems.count(), 1)
        self.assertEqual(systems[0], self.db_objects['system'])
