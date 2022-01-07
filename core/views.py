from django.shortcuts import render
from .models import Todo
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Create your views here.
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def get_todo(filter_todo = None):
    if filter_todo:
        print('DATA FROM DB')

        todos = Todo.objects.filter(name__contains=filter_todo)
    else:
        todos = Todo.objects.all()
    return todos


def home(request):
    filter_todo = request.GET.get('todo')
    if cache.get(filter_todo):
        print('DATA FROM CACHE')
        todo = cache.get(filter_todo)
    else:
        if filter_todo:
            todo = get_todo(filter_todo)
            cache.set(filter_todo, todo)
        else:
            todo = get_todo()

    context = { 'todo': todo }
    return render(request, 'home.html', context)


def show(request, id):
    if cache.get(id):
        print('DATA FROM CACHE')
        todo = cache.get(id)
    else:
        print('DATA FROM DB')

        todo = Todo.objects.get(id=id)
        cache.set(id, todo)

    context = { 'todo': todo }
    return render(request, 'show.html', context)
