from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Contacts, Category
from catalog.services import ProductService


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        return ProductService.get_products_list()


class ProductsByCategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'catalog/products_by_category.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.object.id
        context['products_by_category'] = ProductService.get_products_by_category(category_id)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user:
            raise PermissionDenied('У вас не достаточно прав для редактирования данного продукта.')
        return obj


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.owner != self.request.user and not self.request.user.groups.filter(name='Модератор продуктов').exists():
            raise PermissionDenied('У вас не достаточно прав для удаления данного продукта.')
        return obj


class UnpublishProductView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied('У вас не достаточно прав для отмены публикации.')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.is_publication = False
        product.save()
        return redirect('catalog:products_list')


class ContactsTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        contact = Contacts.objects.first()
        context = {
            'contact': contact
        }
        return render(request, 'catalog/contacts.html', context=context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Поступило обращение от {name}, номер телефона:{phone}, следующего содержания: {message}.')
        return HttpResponse(f'Спасибо {name}! Ваше сообщение получено.')
