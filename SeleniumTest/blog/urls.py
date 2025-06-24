from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('posts/', views.post_list_view, name='posts'),
    path('posts/create', views.post_create_view, name='post_create'),
    path('posts/<int:pk>/edit_ajax/', views.post_edit_ajax, name='post_edit_ajax'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete')
]