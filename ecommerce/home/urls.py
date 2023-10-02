from django.urls import path
from .import views

app_name = 'home'

urlpatterns = [
    path('',views.index , name="home"),
    path('home',views.index , name="home"),
    path('about',views.about , name = "about"),
    path('shop',views.shop , name="shop"),
    path('product_details',views.product_details , name="product_details"),
    path('blog', views.blog , name= "blog"),
    path('contact', views.contact , name="contact")
]