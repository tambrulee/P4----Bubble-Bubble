from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
def view_cart(request):
    return HttpResponse("Cart page — it works!")

