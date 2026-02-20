from django.urls import path
from auth_sys import views

app_name = 'auth_sys'

urlpatterns = [
    path('register/', views.ReqisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
]