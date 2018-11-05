from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (DocumentationRecordListView, DocumentationRecordDetailView,
    MaintenanceRecordDetailView, MaintenanceRecordListView, raw_view,
    system_maintenance_home_view)


app_name = 'system_maintenance'

urlpatterns = [
    url(r'^$', system_maintenance_home_view, name='system_maintenance_home_view'),
    url(r'^authentication/$', auth_views.login, {'template_name': 'system_maintenance/authentication.html'}, name='authentication'),
    url(r'^documentation/$', DocumentationRecordListView.as_view(), name='documentation_record_list'),
    url(r'^documentation/(?P<pk>\d+)/$', DocumentationRecordDetailView.as_view(), name='documentation_record_detail'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/system_maintenance/'}, name='logout'),
    url(r'^raw/(?P<type_of_record>[A-Za-z]+)/(?P<type_of_field>[A-Za-z]+)/(?P<record_pk>\d+)/$', raw_view, name='raw_view'),
    url(r'^records/$', MaintenanceRecordListView.as_view(), name='maintenance_record_list'),
    url(r'^records/(?P<pk>\d+)/$', MaintenanceRecordDetailView.as_view(), name='maintenance_record_detail'),
]
