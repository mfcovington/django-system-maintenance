from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'system_maintenance'

urlpatterns = [
    path('', views.system_maintenance_home_view, name='system_maintenance_home_view'),
    path('authentication/', auth_views.LoginView.as_view(template_name='system_maintenance/authentication.html'), name='authentication'),
    path('documentation/', views.DocumentationRecordListView.as_view(), name='documentation_record_list'),
    path('documentation/<int:pk>/', views.DocumentationRecordDetailView.as_view(), name='documentation_record_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/system_maintenance/'), name='logout'),
    path('raw/<type_of_record>/<type_of_field>/<int:record_pk>/', views.raw_view, name='raw_view'),
    path('records/', views.MaintenanceRecordListView.as_view(), name='maintenance_record_list'),
    path('records/<int:pk>/', views.MaintenanceRecordDetailView.as_view(), name='maintenance_record_detail'),
]
