from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('admin', views.admin, name='admin'),
    path('technician', views.technician, name='technician'),
    path('employee', views.employee, name='employee'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
]
