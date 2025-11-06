from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
def product_list(request):
    return HttpResponse("Catalog home — it works!")
