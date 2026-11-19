from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """Общедоступная страница просмотра списка товаров"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ContactsView(TemplateView):
    """Общедоступная страница контактов"""

    template_name = "catalog/contacts.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Закрыто для анонимов: просмотр карточки товара"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Закрыто для анонимов: создание товара с автопривязкой владельца"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form: ProductForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование доступно только владельцу или модератору"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def test_func(self) -> bool:
        product = self.get_object()
        user = self.request.user
        return bool(product.owner == user or user.has_perm("catalog.can_unpublish_product"))

    def get_success_url(self) -> str:
        return str(reverse_lazy("product_detail", kwargs={"pk": self.object.pk}))


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление доступно только владельцу или модератору"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self) -> bool:
        product = self.get_object()
        user = self.request.user
        return bool(product.owner == user or user.has_perm("catalog.delete_product"))


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Отмена публикации продукта (только для модераторов с правом can_unpublish_product)"""

    permission_required = "catalog.can_unpublish_product"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])
        return redirect("product_detail", pk=pk)
