
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


    path('sales_report',views.sales_report , name='sales_report'),
    path('export_csv/<str:start_date>/<str:end_date>/', views.export_csv, name='export_csv'),
    path('pdf/<str:start_date>/<str:end_date>/',views.pdf , name='pdf')
]   