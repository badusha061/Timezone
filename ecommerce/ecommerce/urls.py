
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('user/',include('userauth.urls')),
    path('adminside/',include('adminside.urls')),
    path('categories/',include('categories.urls')),
    path('product/',include('product.urls')),
    path('cart/',include('cart.urls')),
    path('userprofile',include('userprofile.urls')),
    path('order/',include('order.urls')),
    path('checkout/',include('checkout.urls')),
    path('coupon/',include('coupon.urls')),
    path('wishlist/',include('wishlist.urls')),
    path('offer/',include('offer.urls')),
    path('banner/',include('banner.urls')),
   

] +static(settings. MEDIA_URL,document_root=settings.MEDIA_ROOT)
