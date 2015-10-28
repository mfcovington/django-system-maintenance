from django.conf.urls import patterns, url

from .views import (DocumentationRecordListView, DocumentationRecordDetailView,
    MaintenanceRecordDetailView, MaintenanceRecordListView,
    system_maintenance_home_view)


urlpatterns = patterns('',
    url(r'^$', system_maintenance_home_view, name='system_maintenance_home_view'),
    url(r'^documentation/$', DocumentationRecordListView.as_view(), name='documentation_record_list'),
    url(r'^documentation/(?P<pk>\d+)/$', DocumentationRecordDetailView.as_view(), name='documentation_record_detail'),
    url(r'^records/$', MaintenanceRecordListView.as_view(), name='maintenance_record_list'),
    url(r'^records/(?P<pk>\d+)/$', MaintenanceRecordDetailView.as_view(), name='maintenance_record_detail'),
)
