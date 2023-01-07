from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form':UserCreationForm

    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'signup.html', {
            'form':UserCreationForm,
            'error': 'el usuario ya existe '
    })
            #registrar el usuari\

        return render(request, 'signup.html', {
            'form':UserCreationForm,
            'error': 'contrasena no coinciden '
    })

@login_required
def task(request):
    task = Task.objects.filter(user=request.user, dato_completado__isnull=True)
    return render(request, 'task.html', {'task': task})

@login_required
def task_completada(request):
    task = Task.objects.filter(user=request.user, dato_completado__isnull=False).order_by("-dato_completado")
    return render(request, 'task.html', {'task': task})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El nombre o la contrasena es incorrecta'
            })
        else:
            login(request, user)
            return redirect('task')

@login_required
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html', {
       'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            print(nueva_tarea)
            return redirect('/task')
        except ValueError:
            return render(request, 'crear_tarea.html', {
            'form': TaskForm,
            'error': 'Porfavor ingresa datos validos'
            })

@login_required
def tarea_detalles(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tarea_detalles.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'tarea_detalles.html', {'task': task, 'form': form, 'error': 'error actualizando la tarea'})

@login_required
def completa_task(request, task_id):
    
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.dato_completado = timezone.now()
        task.save()
        return redirect("task")
    
@login_required
def eliminar_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task")



