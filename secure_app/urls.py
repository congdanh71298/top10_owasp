from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='secure_index'),
    path('a1/', views.a1_broken_access_control, name='secure_a1'),
    path('a2/', views.a2_cryptographic_failures, name='secure_a2'),
    path('a3/', views.a3_injection, name='secure_a3'),
    path('a4/', views.a4_insecure_design, name='secure_a4'),
    path('a5/', views.a5_security_misconfiguration, name='secure_a5'),
    path('a6/', views.a6_vulnerable_and_outdated_components, name='secure_a6'),
    path('a7/', views.a7_identification_and_authentication_failures, name='secure_a7'),
    path('a8/', views.a8_software_and_data_integrity_failures, name='secure_a8'),
    path('a9/', views.a9_security_logging_and_monitoring_failures, name='secure_a9'),
    path('a10/', views.a10_server_side_request_forgery, name='secure_a10'),
]
