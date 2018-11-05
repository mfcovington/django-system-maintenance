from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from .app_settings import SYSTEM_MAINTENANCE_PAGINATE_BY
from .models import (DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceType, Software, SysAdmin, System)


def sysadmin_check(user):
    """
    Check whether user is a sysadmin and has an active account.
    """

    return user.is_active and hasattr(user, 'sysadmin')


class SysAdminRequiredMixin(object):
    """
    Checks whether user is a sysadmin and has an active account.
    """

    @method_decorator(user_passes_test(
        sysadmin_check,
        login_url=reverse_lazy('system_maintenance:authentication')))
    def dispatch(self, *args, **kwargs):
        return super(SysAdminRequiredMixin, self).dispatch(*args, **kwargs)


@user_passes_test(
    sysadmin_check,
    login_url=reverse_lazy('system_maintenance:authentication'))
def raw_view(request, **kwargs):
    if kwargs['type_of_record'] == 'documentation':
        record = DocumentationRecord.objects.get(pk=kwargs['record_pk'])
    elif kwargs['type_of_record'] == 'maintenance':
        record = MaintenanceRecord.objects.get(pk=kwargs['record_pk'])
    else:
        pass

    field = getattr(record, kwargs['type_of_field'])

    context = {
        'type_of_field': kwargs['type_of_field'],
        'raw': field.raw,
        'record': record,
    }
    return render(
        request, 'system_maintenance/raw.html', context)


@user_passes_test(
    sysadmin_check,
    login_url=reverse_lazy('system_maintenance:authentication'))
def system_maintenance_home_view(request):
    context = {
        'documentation_record_count':
            DocumentationRecord.objects.all().count(),
        'hardware_count': Hardware.objects.all().count(),
        'maintenance_record_count': MaintenanceRecord.objects.all().count(),
        'maintenance_type_count': MaintenanceType.objects.all().count(),
        'software_count': Software.objects.all().count(),
        'sys_admin_count': SysAdmin.objects.all().count(),
        'system_count': System.objects.all().count(),
    }
    return render(
        request, 'system_maintenance/system_maintenance_home.html', context)


class DocumentationRecordDetailView(SysAdminRequiredMixin, DetailView):

    model = DocumentationRecord
    template_name = 'system_maintenance/documentation_record_detail.html'


class DocumentationRecordListView(SysAdminRequiredMixin, ListView):

    model = DocumentationRecord
    paginate_by = SYSTEM_MAINTENANCE_PAGINATE_BY
    template_name = 'system_maintenance/documentation_record_list.html'


class MaintenanceRecordDetailView(SysAdminRequiredMixin, DetailView):

    model = MaintenanceRecord
    template_name = 'system_maintenance/maintenance_record_detail.html'


class MaintenanceRecordListView(SysAdminRequiredMixin, ListView):

    model = MaintenanceRecord
    paginate_by = SYSTEM_MAINTENANCE_PAGINATE_BY
    template_name = 'system_maintenance/maintenance_record_list.html'
