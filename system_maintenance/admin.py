from django import forms
from django.contrib import admin

from .models import (DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceRecordRelationship, MaintenanceType, Software, SysAdmin, System)


class ReferencingRecordInline(admin.TabularInline):
    model = MaintenanceRecordRelationship
    fk_name = 'referencing_record'


class ReferencedRecordInline(admin.TabularInline):
    model = MaintenanceRecordRelationship
    fk_name = 'referenced_record'


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):

    search_fields = ['name']


class DocumentationRecordAdminForm(forms.ModelForm):
    maintenance_records = forms.ModelMultipleChoiceField(
        MaintenanceRecord.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple(
            'MaintenanceRecord', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['maintenance_records'] = \
                self.instance.maintenance_records.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.pk:
            instance.maintenance_records.clear()
            instance.maintenance_records.add(
                *self.cleaned_data['maintenance_records'])
        return instance


@admin.register(DocumentationRecord)
class DocumentationRecordAdmin(admin.ModelAdmin):

    form = DocumentationRecordAdminForm

    fieldset_basic = ('Basic', {
        'fields': [
            'title',
            'maintenance_type'
        ],
    })

    fieldset_description = ('Documentation', {
        'fields': [
            'documentation',
            'documentation_markup_type',
        ],
    })

    fieldset_maintenance_records = ('Related Maintenance Records', {
        'fields': [
            'maintenance_records',
        ],
    })

    fieldset_timestamps = ('Timestamps', {
        'classes': ['collapse'],
        'fields': [
            'created_at',
            'updated_at',
        ],
    })

    fieldsets = [
        fieldset_basic,
        fieldset_description,
        fieldset_maintenance_records,
        fieldset_timestamps,
    ]

    list_display = [
        'title',
        'maintenance_type',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'maintenance_type',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    save_on_top = True

    search_fields = [
        'title',
        'documentation',
    ]


@admin.register(MaintenanceRecordRelationship)
class MaintenanceRecordRelationshipAdmin(admin.ModelAdmin):

    list_display = [
        '__str__',
        'referencing_record',
        'referenced_record',
    ]

    search_fields = [
        'referencing_record__description',
        'referencing_record__procedure',
        'referencing_record__problems',
        'referencing_record__system__name',
        'referencing_record__hardware__name',
        'referencing_record__software__name',
        'referencing_record__maintenance_type__maintenance_type',
        'referenced_record__description',
        'referenced_record__procedure',
        'referenced_record__problems',
        'referenced_record__system__name',
        'referenced_record__hardware__name',
        'referenced_record__software__name',
        'referenced_record__maintenance_type__maintenance_type',
    ]


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):

    fieldset_basic = ('Basic', {
        'fields': [
            'system',
            'sys_admin',
            'maintenance_type',
            'hardware',
            'software',
            'datetime',
            'status',
        ],
    })

    fieldset_description = ('Description', {
        'fields': [
            'description',
            'description_markup_type',
        ],
    })

    fieldset_procedure = ('Procedure', {
        'fields': [
            'procedure',
            'procedure_markup_type',
        ],
    })

    fieldset_problems = ('Problems', {
        'fields': [
            'problems',
            'problems_markup_type',
        ],
    })

    fieldset_documentation = ('Documentation Records', {
        'fields': [
            'documentation_records',
        ],
    })

    fieldsets = [
        fieldset_basic,
        fieldset_description,
        fieldset_procedure,
        fieldset_problems,
        fieldset_documentation,
    ]

    filter_horizontal = [
        'hardware',
        'software',
        'documentation_records',
    ]

    inlines = [
        ReferencingRecordInline,
        ReferencedRecordInline,
    ]

    list_display = [
        '__str__',
        'system',
        'datetime',
        'maintenance_type',
        'sys_admin',
        'status',
    ]

    list_filter = [
        'status',
        'system',
        'maintenance_type',
        'hardware',
        'software',
        'sys_admin',
    ]

    save_on_top = True

    search_fields = [
        'description',
        'procedure',
        'problems',
    ]


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):

    search_fields = [
        'maintenance_type',
        'description',
    ]


@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):

    search_fields = ['name']


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):

    search_fields = [
        'name',
        'description',
    ]


admin.site.register(SysAdmin)
