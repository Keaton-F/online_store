from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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
    """Закрыто для анонимов: создание товара"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Закрыто для анонимов: редактирование товара"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self) -> str:
        return str(reverse_lazy("product_detail", kwargs={"pk": self.object.pk}))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Закрыто для анонимов: удаление товара"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")
