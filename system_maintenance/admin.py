from django.contrib import admin

from .models import Maintenance, MaintenanceType, Software, SysAdmin, System


admin.site.register(Maintenance)
admin.site.register(MaintenanceType)
admin.site.register(Software)
admin.site.register(SysAdmin)
admin.site.register(System)
