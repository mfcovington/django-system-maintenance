from django.views.generic import DetailView, ListView

from .models import Maintenance


class MaintenanceDetailView(DetailView):
    model = Maintenance
    template_name = 'system_maintenance/maintenance_detail.html'


class MaintenanceListView(ListView):
    model = Maintenance
    template_name = 'system_maintenance/maintenance_list.html'
