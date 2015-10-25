from django.contrib import admin

from .models import Maintenance, MaintenanceType, Software, SysAdmin, System


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):

    fieldset_basic = ('Basic', {
        'fields': [
            'system',
            'sys_admin',
            'maintenance_type',
            'software',
            'datetime',
            'success',
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

    filter_horizontal = ['software']

    list_display = [
        'id',
        'system',
        'datetime',
        'maintenance_type',
        'sys_admin',
        'success',
    ]

    list_filter = [
        'system',
        'maintenance_type',
        'software',
        'success',
        'sys_admin',
    ]

    search_fields = [
        'description',
        'procedure',
        'problems',
    ]


admin.site.register(MaintenanceType)
admin.site.register(Software)
admin.site.register(SysAdmin)
admin.site.register(System)
