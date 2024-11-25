from django.shortcuts import render
from django.db import connection

def index(request):
    return render(request, 'vulnerable_app/index.html')

def a1_broken_access_control(request):
    user_id = request.GET.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return render(request, 'vulnerable_app/a1_broken_access_control.html', {'result': result})

def a2_cryptographic_failures(request):
    return render(request, 'vulnerable_app/a2_cryptographic_failures.html')

def a3_injection(request):
    return render(request, 'vulnerable_app/a3_injection.html')

def a4_insecure_design(request):
    return render(request, 'vulnerable_app/a4_insecure_design.html')

def a5_security_misconfiguration(request):
    return render(request, 'vulnerable_app/a5_security_misconfiguration.html')

def a6_vulnerable_and_outdated_components(request):
    return render(request, 'vulnerable_app/a6_vulnerable_and_outdated_components.html')

def a7_identification_and_authentication_failures(request):
    return render(request, 'vulnerable_app/a7_identification_and_authentication_failures.html')

def a8_software_and_data_integrity_failures(request):
    return render(request, 'vulnerable_app/a8_software_and_data_integrity_failures.html')

def a9_security_logging_and_monitoring_failures(request):
    return render(request, 'vulnerable_app/a9_security_logging_and_monitoring_failures.html')

def a10_server_side_request_forgery(request):
    return render(request, 'vulnerable_app/a10_server_side_request_forgery.html')
