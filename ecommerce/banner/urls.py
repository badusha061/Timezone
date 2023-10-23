from django.urls import path
from .import views




urlpatterns = [
    path('banner',views.banner , name='banner'),
    path('add_banner',views.add_banner , name='add_banner'),
    path('edit_banner/<int:editbanner_id>/',views.edit_banner , name='edit_banner'),
    path('delete_banner/<int:deletebanner_id>/',views.delete_banner , name='delete_banner'),

]