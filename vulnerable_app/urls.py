from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='vulnerable_index'),
    # Add paths for each vulnerability demo
]
