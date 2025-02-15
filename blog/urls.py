from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig


app_name = BlogConfig.name

urlpatterns = [
    path(),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
