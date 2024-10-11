from django.urls import path
from .views import (
    post_list_view,
    create_comment_view,
    create_like_view,
    retrieve_update_and_delete_view,
    registration_view,
    login_view,
    
)

urlpatterns = [
    
    path('users/register', registration_view, name='register' ),
    path('users/login', login_view, name='login' ),



    path('posts/', post_list_view, name='post-list-create'),
    path('posts/<int:pk>/', retrieve_update_and_delete_view, name='post-detail'),
    path('posts/<int:post_id>/like/', create_like_view, name='post-like'),
    path('posts/<int:post_id>/comment/', create_comment_view, name='post-comment'),
]
