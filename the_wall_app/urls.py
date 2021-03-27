from django.urls import include, path     
from . import views
urlpatterns = [
    path('', views.log_and_reg),
    path('login', views.login),
    path('register', views.register),
    path('wall', views.wall),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment/<int:wall_message_id>', views.post_comment),
    path('delete_message/<int:wall_message_id>', views.delete_message),
 #   path('delete_comment', views.delete_comment),
]