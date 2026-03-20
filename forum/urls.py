from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_details'),
    path('thread/post/', views.ThreadCreateView.as_view(), name='thread_create')
]