from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
# Create your views here.
def home(request):
    return render(request, "home.html")

def tasks(request):
    tasks = Task.objects.filter(user=request.user, 
                                datecompleted__isnull=True)
    return render(request, "tasks.html"
                  ,{"tasks":tasks})

def create_task(request):
    if request.method == "GET":
        return render (request, 
                       "create_task.html", 
                       {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            print(form)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, 
                      "create_task.html",
                      "form",TaskForm,)
def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request,
                      "signin.html",
                      {"form":AuthenticationForm()})
    else:
        user = authenticate(request,
                            username=request.POST["username"],
                            password =request.POST["password"])
        if user is None:
            return render(request,
                          "",
                          {"form":AuthenticationForm(),
                           "error":"Usuario o contraseña incorrecta"})
        else:
            login(request, user)
            return redirect("tasks")


def signup(request):
    if request.method == "GET":
        return render(request, 
                  "signup.html",
                  {"form":UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("tasks")

            except IntegrityError:
                return render(request,
                              'signup.html',
                              {"form": UserCreationForm(),
                               "error":"Error al crear el usuario"})
                
        else:
                 return render(request,
                              'signup.html',
                              {"form": UserCreationForm(),
                               "error":"Error, Las contraseñas no coinciden"})

def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')  
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form, 'task': task})

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')  
    return render(request, 'task_confirm_delete.html', {'task': task})