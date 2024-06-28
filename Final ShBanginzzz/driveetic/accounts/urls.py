from django.urls import path
from . import views

urlpatterns = [ 
    path('login', views.login, name='login'),
    path('signup', views.SignupView.as_view() , name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard_view, name='staff_dashboard'),
    path('file/<pk>', views.file_detail_view, name='file_detail'),
    path('file/<pk>/delete', views.file_delete_view, name='file_delete'),
]