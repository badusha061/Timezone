from django.urls import path
from .import views

app_name = 'userauth'

urlpatterns = [
    path('user_login/',views.user_login, name="user_login"),
    path('register/',views.register_views, name="register"),
    path('logout/',views.user_logout, name='user_logout'),

    path('forget_password',views.forget_password , name='forget_password'),
    path('change_password/<str:token>',views.change_password, name='change_password')
]