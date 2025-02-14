from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>/', product_detail, name='product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
