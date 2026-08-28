from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Product


def home(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "catalog/home.html", {"products": products})


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, "catalog/contacts.html")


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    product = Product.objects.get(pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})
