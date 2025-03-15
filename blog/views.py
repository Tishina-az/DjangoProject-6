from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Post
from config.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(publication_at=True)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'preview', 'publication_at']
    success_url = reverse_lazy('blog:posts_list')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.number_of_views += 1
        obj.save()
        if obj.number_of_views == 100:
            subject = f"100 просмотров {obj.title}!"
            massage = f"Поздравляем! Статья: '{obj.title}' - достигла 100 просмотров."
            from_email = DEFAULT_FROM_EMAIL
            to_email = [EMAIL_HOST_USER,]
            send_mail(subject, massage, from_email, to_email)
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'preview', 'publication_at']

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:posts_list')
