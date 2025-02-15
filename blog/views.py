from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview', 'publication_at']
    success_url = reverse_lazy('blog:posts_list')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.number_of_views += 1
        return obj


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'preview', 'publication_at']
    success_url = reverse_lazy('blog:posts_list')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:posts_list')
