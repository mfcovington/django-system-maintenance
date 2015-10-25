from django.conf.urls import patterns, url

from .views import MaintenanceDetailView


urlpatterns = patterns('',
    url(r'^records/(?P<pk>\d+)/$', MaintenanceDetailView.as_view(), name='maintenance_detail'),
)
