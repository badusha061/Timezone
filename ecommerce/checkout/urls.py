from django.urls import path
from .import views


# app_name = 'categories'

urlpatterns = [
    path('',views.checkout,name='checkout'),
    path('add_address_check',views.add_address_check , name='add_address_check'),
    path('edit_address_check/<int:editaddress_id>/',views.edit_address_check , name='edit_address_check'),


    path('apply_coupon',views.apply_coupon , name='apply_coupon'),

    path('placeorder',views.placeorder, name='placeorder'),
    path('proceed-to-pay',views.rezorpaycheck , name='proceed-to-pay'),

]