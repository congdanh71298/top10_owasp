from django.shortcuts import render
from django.db import connection

def index(request):
    return render(request, 'secure_app/index.html')

def sql_injection(request):
    user_id = request.GET.get('id')
    query = "SELECT * FROM users WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, [user_id])
    result = cursor.fetchall()
    return render(request, 'secure_app/sql_injection.html', {'result': result})
