from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostCreateView

app_name = BlogConfig.name

urlpatterns = [
    path('', PostListView.as_view(), name='posts_list'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
