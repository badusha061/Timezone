from django.urls import path
from .import views



urlpatterns = [
    path('',views.userprofile , name='userprofile'),
    path('add_address',views.add_address, name='add_address'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('changepassword',views.changepassword , name='changepassword'),
    path('edit_address/<int:editaddress_id>/',views.edit_address , name='edit_address'),
    path('delete_address/<int:deleteaddress_id>/',views.delete_address , name='delete_address'),
    path('edit_image',views.edit_image , name='edit_image'),
    

    path('wallet',views.wallet , name='wallet' ),
    path('chatbox',views.chat_box, name='chatbox')

]   