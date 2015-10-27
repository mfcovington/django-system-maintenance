from django.contrib import admin

from .models import (Hardware, Maintenance, MaintenanceRecordRelationship,
    MaintenanceType, Software, SysAdmin, System)


class ReferencingRecordInline(admin.TabularInline):
    model = MaintenanceRecordRelationship
    fk_name = 'referencing_record'


class ReferencedRecordInline(admin.TabularInline):
    model = MaintenanceRecordRelationship
    fk_name = 'referenced_record'


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):

    search_fields = ['name']


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


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):

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

    fieldsets = [
        fieldset_basic,
        fieldset_description,
        fieldset_procedure,
        fieldset_problems,
    ]

    filter_horizontal = [
        'hardware',
        'software',
    ]

    inlines = [
        ReferencingRecordInline,
        ReferencedRecordInline,
    ]

    list_display = [
        'id',
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
