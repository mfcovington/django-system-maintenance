from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.html import escape, linebreaks, urlize

import markdown2
from docutils.core import publish_parts
from markupfield.fields import MarkupField


def render_md(markup):
    return markdown2.markdown(markup, extras=[
        'code-friendly',
        'cuddled-lists',
        'fenced-code-blocks',
        'footnotes',
        'tables',
    ])


def render_rest(markup):
    parts = publish_parts(source=markup, writer_name="html4css1")
    return parts["fragment"]


MARKUP_FIELD_TYPES = [
    ('Markdown', render_md),
    ('Markdown Basic', markdown2.markdown),
    ('Plain Text', lambda markup: urlize(linebreaks(escape(markup)))),
    ('reStructuredText', render_rest),
]

STATUS_CHOICES = [
    ('Complete', 'Complete'),
    ('In Progress', 'In Progress'),
    ('Failed', 'Failed'),
]


class Hardware(models.Model):

    name = models.CharField(
        max_length=255,
        help_text="Enter the type of hardware.",
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'hardware'

    def __str__(self):
        return self.name


class DocumentationRecord(models.Model):

    title = models.CharField(
        max_length=255,
        help_text="Enter a brief, descriptive title for this documentation.",
        unique=True,
    )

    maintenance_type = models.ForeignKey(
        'MaintenanceType',
        help_text='Select/Create a maintenance type.',
        on_delete=models.PROTECT,
    )

    documentation = MarkupField(
        blank=True,
        default_markup_type='Markdown',
        help_text='Document how to perform a task.',
        markup_choices=MARKUP_FIELD_TYPES,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title



class MaintenanceRecord(models.Model):
    system = models.ForeignKey(
        'System',
        help_text='Select/Create a system.',
        on_delete=models.PROTECT,
    )

    sys_admin = models.ForeignKey(
        'SysAdmin',
        help_text='Select a system administrator.',
        on_delete=models.PROTECT,
    )

    maintenance_type = models.ForeignKey(
        'MaintenanceType',
        help_text='Select/Create a maintenance type.',
        on_delete=models.PROTECT,
    )

    hardware = models.ManyToManyField(
        'Hardware',
        blank=True,
        help_text='Select the hardware involved in the system maintenance.',
    )

    software = models.ManyToManyField(
        'Software',
        blank=True,
        help_text='Select the software involved in the system maintenance.',
    )

    description = MarkupField(
        blank=True,
        default_markup_type='Markdown',
        help_text='Enter a description of the system maintenance performed.',
        markup_choices=MARKUP_FIELD_TYPES,
        null=True,
    )

    procedure = MarkupField(
        blank=True,
        default_markup_type='Markdown',
        help_text='Enter details of how the system maintenance was performed.',
        markup_choices=MARKUP_FIELD_TYPES,
        null=True,
    )

    problems = MarkupField(
        blank=True,
        default_markup_type='Markdown',
        help_text='Describe problems that arose during system maintenance.',
        markup_choices=MARKUP_FIELD_TYPES,
        null=True,
    )

    referenced_records = models.ManyToManyField(
        'self',
        related_name='referencing_records',
        symmetrical=False,
        through='MaintenanceRecordRelationship',
    )

    documentation_records = models.ManyToManyField(
        'DocumentationRecord',
        blank=True,
        help_text='Select documentation relevant to this system maintenance.<br>',
        related_name='maintenance_records',
    )

    status = models.CharField(
        choices = STATUS_CHOICES,
        default='In Progress',
        help_text='What is the current status of the system maintenance?',
        max_length=15,
    )

    datetime = models.DateTimeField(
        'maintenance date/time',
        default=timezone.now,
        help_text='Specify the date/time that the system maintenance was '
                  'performed.',
    )

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'maintenance record'
        verbose_name_plural = 'maintenance records'

    def __str__(self):
        return '{} - {} ({})'.format(
            self.system, self.maintenance_type, self.datetime.date())


class MaintenanceRecordRelationship(models.Model):

    referencing_record = models.ForeignKey(
        'MaintenanceRecord',
        related_name='referencing_record',
        on_delete=models.CASCADE,
    )

    referenced_record = models.ForeignKey(
        'MaintenanceRecord',
        related_name='referenced_record',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['referencing_record']
        unique_together = ('referencing_record', 'referenced_record')

    def clean(self):
        if self.referencing_record == self.referenced_record:
            raise ValidationError('A record cannot by related to itself.')

    def __str__(self):
        return '{} ➤ {}'.format(
            self.referencing_record, self.referenced_record)


class MaintenanceType(models.Model):

    maintenance_type = models.CharField(
        help_text="Enter a type of maintenance "
                  "(e.g., 'Software Installation').",
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Enter a description of the maintenance type.',
    )

    class Meta:
        ordering = ['maintenance_type']

    def __str__(self):
        return self.maintenance_type


class Software(models.Model):

    name = models.CharField(
        max_length=255,
        help_text="Enter the software's name.",
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'software package'
        verbose_name_plural = 'software packages'

    def __str__(self):
        return self.name


class SysAdmin(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        help_text='Select a user.',
        on_delete=models.PROTECT,
        unique=True,
    )

    class Meta:
        verbose_name = 'system administrator'
        verbose_name_plural = 'system administrators'

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return '{} ({})'.format(
                ' '.join([self.user.first_name, self.user.last_name]),
                self.user.username)
        else:
            return self.user.username


class System(models.Model):

    name = models.CharField(
        'system name',
        help_text='Enter a brief, unique identifier for the system.',
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        blank=True,
        help_text='Enter a description of the system.',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
