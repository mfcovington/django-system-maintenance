from django.views.generic import DetailView

from .models import Maintenance


class MaintenanceDetailView(DetailView):
    model = Maintenance
    template_name = 'system_maintenance/maintenance_detail.html'
