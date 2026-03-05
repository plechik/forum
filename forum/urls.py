from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.homeview, name='home'),
    path('thread/<int:pk>/', views.theme_detail, name='thread_details'),
]