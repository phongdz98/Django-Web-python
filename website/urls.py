from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name='home'),
    # User URLS
    path('users', views.watch_users, name='users'),
    path('users/<int:pk>', views.customer_user, name='user_info'),
    path('delete_user/<int:pk>', views.delete_user, name='delete_user'),
    path('update_user/<int:pk>', views.update_user, name='update_user'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('ad', views.admin, name='ad'),
    path('technician', views.technician, name='technician'),
    path('employee', views.employee, name='employee'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    # Person URLS
    path('person', views.person_read, name='person'),
    path('add_person', views.add_person, name='add_person'),

    # Expert system URLS
    path('frame', views.frame_read, name='frame'),
    path('delete_frame/<int:pk>', views.delete_frame, name='delete_frame'),
    path('frame_info/<int:pk>', views.frame_info, name='frame_info'),
    path('slot', views.slot_read, name='slot'),
    path('delete_slot/<int:pk>', views.delete_slot, name='delete_slot'),
    path('add_slots_to_frame/<int:frame_id>', views.add_slots_to_frame, name='add_slots_to_frame'),
    path('add_slot_values/<int:frame_id>', views.add_slot_values, name='add_slot_values'),
    path('dialog', views.dialog_view, name='dialog'),

]
