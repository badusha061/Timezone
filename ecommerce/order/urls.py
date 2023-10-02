from django.urls import path
from .import views

apa_name = 'order'

urlpatterns = [
    path('admin_order',views.admin_order, name='admin_order'),
    path('user_order',views.user_order , name='user_order'), 
    path('order_views',views.order_views ,name='order_views'),
    path('order_views_admin/<int:orderviews_id>/',views.order_views_admin , name='order_views_admin'),

    path('change_status',views.change_status , name='change_status'),

]
