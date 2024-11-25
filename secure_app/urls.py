from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='secure_index'),
    # Add paths for each vulnerability demo
]
