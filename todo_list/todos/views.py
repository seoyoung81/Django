from django.shortcuts import render, redirect
from .models import TODO
from .forms import TodoForm, TodoForm

# Create your views here.

def index(request):
    todos = TODO.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)

def detail(request, pk):
    todo = TODO.objects.get(pk=pk)
    context = {
        'todo': todo,
    }
    return render(request, 'todos/detail.html', context)

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save()
            return redirect('todos:detail', pk=todo.pk)
    else:
        form = TodoForm()

    context = {'form': form}
    return render(request, 'todos/create.html', context)
    
def update(request, pk):
    todo = TODO.objects.get(pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect('todos:detail', todo.pk)
    else:
        form = TodoForm(instance=todo)

    context = {'form': form, 'todo': todo}
    return render(request, 'todos/update.html', context)


def delete(request, pk):
    todo = TODO.objects.get(pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todos:index')
    else:
        redirect('todos:detail', todo.pk)