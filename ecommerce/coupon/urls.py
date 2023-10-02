from django.urls import path
from .import views



urlpatterns = [
    path('',views.coupon , name='coupon'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('edit_coupon/<int:editcoupon_id>/',views.edit_coupon , name='edit_coupon'),
    path('delete_coupon/<int:deletecoupon_id>/',views.delete_coupon , name='delete_coupon'),
    path('search_coupon',views.search_coupon, name='search_coupon'), 

   
]