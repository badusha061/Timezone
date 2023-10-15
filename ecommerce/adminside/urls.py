
from django.urls import path 
from .import views

app_name = 'adminside'

urlpatterns = [
    path('',views.dashboard , name= 'dashboard'),
    path('admin_login/',views.admin_login , name= 'admin_login'),
    path('user_mgt/',views.user_mgt , name= 'user_mgt'),
    path('admin_logout',views.admin_logout , name='admin_logout'),
    path('user_block/<int:user_id>/',views.user_block , name='user_block'),
    path('user_search',views.user_search , name='user_search'),
    path('user_block_status',views.user_block_status , name='user_block_status'),
    path('adminpage',views.adminpage, name='adminpage'),

    
]