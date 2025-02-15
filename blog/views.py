from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview', 'publication_at']
    success_url = reverse_lazy('blog:posts_list')
