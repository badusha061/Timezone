from django.urls import path
from .import views

app_name = 'userauth'

urlpatterns = [
    path('user_login/',views.user_login, name="user_login"),
    path('register/',views.register_views, name="register"),
    path('logout/',views.user_logout, name='user_logout'),
]