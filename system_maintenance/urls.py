from django.conf.urls import patterns, url

from .views import (MaintenanceDetailView, MaintenanceListView,
    system_maintenance_home_view)


urlpatterns = patterns('',
    url(r'^$', system_maintenance_home_view, name='system_maintenance_home_view'),
    url(r'^records/$', MaintenanceListView.as_view(), name='maintenance_list'),
    url(r'^records/(?P<pk>\d+)/$', MaintenanceDetailView.as_view(), name='maintenance_detail'),
)
