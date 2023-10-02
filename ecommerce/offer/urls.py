from django.urls import path
from . import views



urlpatterns = [
    path('',views.offer, name='offer'),
    path('add_offer/', views.add_offer , name='add_offer'),
    path('delete_offer/<int:deleteoffer_id>/',views.delete_offer, name='delete_offer'),
    path('edit_offer/<int:editoffer_id>/',views.edit_offer , name='edit_offer'),


]