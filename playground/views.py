from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from tag.models import TaggedItem
from store.models import Cart, CartItem, Product




def hello_view(request):
    context = {
    }
    return render(request, "playground/hello.html", context)