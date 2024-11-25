from django.shortcuts import render
from django.db import connection

def index(request):
    return render(request, 'vulnerable_app/index.html')

def sql_injection(request):
    user_id = request.GET.get('id')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return render(request, 'vulnerable_app/sql_injection.html', {'result': result})
