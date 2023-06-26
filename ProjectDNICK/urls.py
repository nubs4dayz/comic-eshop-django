"""
URL configuration for ProjectDNICK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ComicShop.views import index, comic_detail, add_to_cart, checkout, contact, about, cart, register, \
    remove_from_cart, remove_all_from_cart, order_summary, order_confirmation, edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('comic/<int:comic_id>/', comic_detail, name='comic_detail'),
    path('cart/', cart, name='cart'),
    path('comic/<int:comic_id>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:comic_in_order_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove-all/<int:comic_in_order_id>/', remove_all_from_cart, name='remove_all_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-summary/', order_summary, name='order_summary'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
