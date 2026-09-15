from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Salwa Alifia Putri",
        "npm": "2506620280",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems Student at Universitas Indonesia with interests in "
            "product management, technology, business strategy, and digital innovation."
        ),
        
        "experience_list": Experience.objects.order_by("-started_at"),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Salwa Alifia Putri",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    projects = [
        project.object
        for project in projects
    ]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Salwa Alifia Putri",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Salwa Alifia Putri",
        "form": form,
    }

    return render(request, "projects_form.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id
    )

    if request.method == "POST":
        project.delete()

        messages.success(
            request,
            "Project berhasil dihapus!"
        )

        return redirect(
            "main:show_projects"
        )

    return redirect(
        "main:show_projects"
    )