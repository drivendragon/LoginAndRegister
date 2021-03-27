from django.urls import include, path     
from . import views
urlpatterns = [
    path('', views.log_and_reg),
    path('login', views.login),
    path('register', views.register),
    path('success', views.success),
    path('logout', views.logout),
]