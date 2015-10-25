from django.conf.urls import patterns, url

from .views import MaintenanceDetailView, MaintenanceListView


urlpatterns = patterns('',
    url(r'^records/$', MaintenanceListView.as_view(), name='maintenance_list'),
    url(r'^records/(?P<pk>\d+)/$', MaintenanceDetailView.as_view(), name='maintenance_detail'),
)
