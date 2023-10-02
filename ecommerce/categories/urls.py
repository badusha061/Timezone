from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

# app_name = 'categories'

urlpatterns = [
    path('categories_list',views.categories , name='categories_list'),
    path('add_categories',views.add_categories, name='add_categories'),
    path('edit_categories/<int:editcategory_id>/',views.edit_categories, name='edit_categories'),
    path('add_brand',views.add_brand, name='add_brand'),
    path('edit_brand/<int:editbrand_id>/',views.edit_brand,name='edit_brand'),
    path('search_categories/',views.search_categories , name='search_categories'),
    path('search_brand/',views.search_brand , name='search_brand'),
    path('delete_categories/<int:deletecategory_id>/',views.delete_categories,name='delete_categories'),
    path('delete_brand/<int:deletebrand_id>/',views.delete_brand, name='delete_brand'),
    path('adminpage',views.adminpage , name='adminpage')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)