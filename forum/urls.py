from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/threads', views.ThreadsView.as_view(), name='threads_list'),
    path('threads/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_details'),
    path('<int:pk>/threads/post/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('account/', views.profile_view, name='profile'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search-api/', views.search_api, name='search_api'),
]