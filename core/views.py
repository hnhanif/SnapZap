from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SingupForm
# Create your views here.


def index(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', context={'categories': categories, 'items': items})


def contact(request):
    return render(request, 'core/contact.html')


def signup(request):
    form = SingupForm()

    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')

    return render(request, 'core/signup.html', context={'form': form})
