from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, redirect, render

from .forms import ProjectForm, RegistrationForm
from .models import Project

# Create your views here.


@login_required(login_url="/login")
def index(request):
    projects = Project.objects.all()
    # html doesn't support put or delete, so i made two post requests each for deleting and donating (depending on conditions satisified)
    if request.method == "POST":
        project_id = request.POST.get("project-id")
        project = Project.objects.filter(id=project_id).first()
        if project and project.owner == request.user:  # request to delete
            project.delete()
            return redirect('/')
        else:  # request to donate
            amount_donated = request.POST.get("donation_amount")
            project.amount_donated += int(amount_donated)
            project.save()
            return redirect('/')

    # render all projects
    return render(request, 'main.html', {"projects": projects})


@login_required(login_url="/login")
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('/')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})


@login_required(login_url="/login")
def edit_project(request, project_id):
    project = Project.objects.filter(id=project_id, owner=request.user).first()

    if not project:
        return HttpResponseForbidden("You do not have permission to edit this project.")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)  # pass the instance
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})



