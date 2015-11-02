# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, help_text='Enter a brief, descriptive title for this documentation.')),
                ('documentation', markupfield.fields.MarkupField(null=True, help_text='Document how to perform a task.', blank=True, rendered_field=True)),
                ('documentation_markup_type', models.CharField(blank=True, max_length=30, default='Markdown', choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('_documentation_rendered', models.TextField(null=True, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, help_text='Enter the type of hardware.')),
            ],
            options={
                'verbose_name_plural': 'hardware',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('description', markupfield.fields.MarkupField(null=True, help_text='Enter a description of the system maintenance performed.', blank=True, rendered_field=True)),
                ('description_markup_type', models.CharField(blank=True, max_length=30, default='Markdown', choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')])),
                ('procedure', markupfield.fields.MarkupField(null=True, help_text='Enter details of how the system maintenance was performed.', blank=True, rendered_field=True)),
                ('_description_rendered', models.TextField(null=True, editable=False)),
                ('procedure_markup_type', models.CharField(blank=True, max_length=30, default='Markdown', choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')])),
                ('problems', markupfield.fields.MarkupField(null=True, help_text='Describe problems that arose during system maintenance.', blank=True, rendered_field=True)),
                ('_procedure_rendered', models.TextField(null=True, editable=False)),
                ('problems_markup_type', models.CharField(blank=True, max_length=30, default='Markdown', choices=[('', '--'), ('Markdown', 'Markdown'), ('Markdown Basic', 'Markdown Basic'), ('Plain Text', 'Plain Text'), ('reStructuredText', 'reStructuredText')])),
                ('_problems_rendered', models.TextField(null=True, editable=False)),
                ('status', models.CharField(max_length=15, default='in_progress', help_text='What is the current status of the system maintenance?', choices=[('Complete', 'Complete'), ('In Progress', 'In Progress'), ('Failed', 'Failed')])),
                ('datetime', models.DateTimeField(help_text='Specify the date/time that the system maintenance was performed.', default=django.utils.timezone.now, verbose_name='maintenance date/time')),
                ('documentation_records', models.ManyToManyField(help_text='Select documentation relevant to this system maintenance.<br>', blank=True, related_name='maintenance_records', to='system_maintenance.DocumentationRecord')),
                ('hardware', models.ManyToManyField(help_text='Select the hardware involved in the system maintenance.', blank=True, to='system_maintenance.Hardware')),
            ],
            options={
                'verbose_name_plural': 'maintenance records',
                'verbose_name': 'maintenance record',
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceRecordRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('referenced_record', models.ForeignKey(to='system_maintenance.MaintenanceRecord', related_name='referenced_record')),
                ('referencing_record', models.ForeignKey(to='system_maintenance.MaintenanceRecord', related_name='referencing_record')),
            ],
            options={
                'ordering': ['referencing_record'],
            },
        ),
        migrations.CreateModel(
            name='MaintenanceType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('maintenance_type', models.CharField(unique=True, max_length=255, help_text="Enter a type of maintenance (e.g., 'Software Installation').")),
                ('description', models.TextField(help_text='Enter a description of the maintenance type.', blank=True)),
            ],
            options={
                'ordering': ['maintenance_type'],
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, help_text="Enter the software's name.")),
            ],
            options={
                'verbose_name_plural': 'software packages',
                'verbose_name': 'software package',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SysAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('user', models.OneToOneField(help_text='Select a user.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'system administrators',
                'verbose_name': 'system administrator',
            },
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, help_text='Enter a brief, unique identifier for the system.', verbose_name='system name')),
                ('description', models.TextField(help_text='Enter a description of the system.', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='maintenance_type',
            field=models.ForeignKey(help_text='Select/Create a maintenance type.', to='system_maintenance.MaintenanceType'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='referenced_records',
            field=models.ManyToManyField(through='system_maintenance.MaintenanceRecordRelationship', to='system_maintenance.MaintenanceRecord', related_name='referencing_records'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='software',
            field=models.ManyToManyField(help_text='Select the software involved in the system maintenance.', blank=True, to='system_maintenance.Software'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='sys_admin',
            field=models.ForeignKey(help_text='Select a system administrator.', to='system_maintenance.SysAdmin'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='system',
            field=models.ForeignKey(help_text='Select/Create a system.', to='system_maintenance.System'),
        ),
        migrations.AddField(
            model_name='documentationrecord',
            name='maintenance_type',
            field=models.ForeignKey(help_text='Select/Create a maintenance type.', to='system_maintenance.MaintenanceType'),
        ),
        migrations.AlterUniqueTogether(
            name='maintenancerecordrelationship',
            unique_together=set([('referencing_record', 'referenced_record')]),
        ),
    ]
