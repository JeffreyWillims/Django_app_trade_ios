"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from importlib.metadata import requires

from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- Импортируем settings
from django.conf.urls.static import static  # <-- Импортируем static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('pages.urls', namespace='pages')),

    path('products/', include('products.urls', namespace='products')),

    path('users/', include('users.urls', namespace='users')),

    path('carts/', include('carts.urls', namespace='carts')),

    path('orders/', include('orders.urls', namespace='orders')),
]

# --- Маршрут для раздачи медиафайлов в режиме разработки ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)