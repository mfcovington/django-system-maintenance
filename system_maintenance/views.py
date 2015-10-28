from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import available_attrs, method_decorator
from django.views.generic import DetailView, ListView

from .models import (DocumentationRecord, Hardware, MaintenanceRecord,
    MaintenanceType, Software, SysAdmin, System)


def user_passes_test_or_404(test_func, message='User test failed.'):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the 404 page if the test fails. The test should be a
    callable that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise Http404(message)
        return _wrapped_view
    return decorator


class SysAdminRequiredMixin(object):

    @method_decorator(user_passes_test_or_404(
        lambda u: u in [s.user for s in SysAdmin.objects.all()],
        'Current user is not a system administrator.'
    ))
    def dispatch(self, *args, **kwargs):
        return super(SysAdminRequiredMixin, self).dispatch(*args, **kwargs)


@user_passes_test_or_404(
    lambda u: u in [s.user for s in SysAdmin.objects.all()],
    'Current user is not a system administrator.'
)
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
    paginate_by = 30
    template_name = 'system_maintenance/documentation_record_list.html'


class MaintenanceRecordDetailView(SysAdminRequiredMixin, DetailView):

    model = MaintenanceRecord
    template_name = 'system_maintenance/maintenance_record_detail.html'


class MaintenanceRecordListView(SysAdminRequiredMixin, ListView):

    model = MaintenanceRecord
    paginate_by = 30
    template_name = 'system_maintenance/maintenance_record_list.html'
