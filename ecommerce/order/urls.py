from django.urls import path
from .import views


urlpatterns = [
    path('admin_order',views.admin_order, name='admin_order'),
    path('user_order',views.user_order , name='user_order'), 
    path('order_views/<int:orderviews_id>/',views.order_views ,name='order_views'),
    path('order_views_admin/<int:orderviews_id>/',views.order_views_admin , name='order_views_admin'),

    path('change_status',views.change_status , name='change_status'),
    path('cancel_order/<int:ordercancel_id>/',views.cancel_order , name='cancel_order'),
    path('retur_order/<int:orderreturn_id>/',views.return_order , name='return_order'),
    path('order_tracker/<int:ordertracker_id>/',views.order_tracker , name='order_tracker')

]
