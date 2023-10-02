from django.urls import path
from .import views



urlpatterns = [
    path('product_list',views.product_list , name="product_list"),
    path('add_product',views.add_product,name='add_product' ),
    path('search_product',views.search_product , name='search_product'),
    path('product_view/<int:viewproduct_id>',views.product_view , name='product_view'),
    path('delete_product/<int:deleteproduct_id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:editproduct_id>/',views.edit_product , name='edit_product'),
    path('product_details',views.product_details , name='product_details'),  
]