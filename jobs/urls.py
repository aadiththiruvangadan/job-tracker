from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/bookmark/', views.job_bookmark_toggle, name='job_bookmark_toggle'),
]
