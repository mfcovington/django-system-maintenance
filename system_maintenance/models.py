from django.conf import settings
from django.db import models
from django.utils import timezone

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


class Maintenance(models.Model):

    system = models.ForeignKey(
        'System',
        help_text='Select/Create a system.',
    )

    sys_admin = models.ForeignKey(
        'SysAdmin',
        help_text='Select a system administrator.',
    )

    maintenance_type = models.ForeignKey(
        'MaintenanceType',
        help_text='Select/Create a maintenance type.',
    )

    software = models.ManyToManyField(
        'Software',
        blank=True,
        help_text='Select the software(s) involved in the system maintenance.',
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

    success = models.BooleanField(
        default=True,
        help_text='Was the system maintenance successful?',
    )

    datetime = models.DateTimeField(
        'maintenance date/time',
        default=timezone.now,
        help_text='Specify the date/time that the system maintenance was '
                  'performed.',
    )

    class Meta:
        ordering = ['system', '-datetime']
        verbose_name = 'maintenance record'
        verbose_name_plural = 'maintenance records'

    def __str__(self):
        return '{} - {} ({})'.format(
            self.system, self.maintenance_type, self.datetime.date())


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

    def __str__(self):
        return self.name


class SysAdmin(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        help_text='Select a user.',
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
