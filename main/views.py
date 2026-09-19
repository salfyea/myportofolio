"""Views for the portfolio app.

Covers the profile/experience pages plus the projects CRUD-lite flow
(list with search, JSON API, create, and delete).
"""

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project

PROFILE_NAME = "Salwa Alifia Putri"

SKILL_LIST = [
    {"name": "Python", "icon_url": "https://cdn.simpleicons.org/python"},
    {"name": "JavaScript", "icon_url": "https://cdn.simpleicons.org/javascript"},
    {"name": "TypeScript", "icon_url": "https://cdn.simpleicons.org/typescript"},
    {"name": "React", "icon_url": "https://cdn.simpleicons.org/react"},
    {"name": "Next.js", "icon_url": "https://cdn.simpleicons.org/nextdotjs"},
    {"name": "Django", "icon_url": "https://cdn.simpleicons.org/django"},
    {"name": "Supabase", "icon_url": "https://cdn.simpleicons.org/supabase"},
    {"name": "Docker", "icon_url": "https://cdn.simpleicons.org/docker"},
    {"name": "Git", "icon_url": "https://cdn.simpleicons.org/git"},
    {"name": "Figma", "icon_url": "https://cdn.simpleicons.org/figma"},
    {"name": "Notion", "icon_url": "https://cdn.simpleicons.org/notion"},
    {"name": "Jira", "icon_url": "https://cdn.simpleicons.org/jira"},
]


def show_main(request):
    """Render the profile/landing page with bio and experience preview."""
    context = {
        "name": PROFILE_NAME,
        "npm": "2506620280",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems Student at Universitas Indonesia with interests in "
            "product management, technology, business strategy, and digital innovation."
        ),
        "experience_list": Experience.objects.order_by("-started_at"),
        "skill_list": SKILL_LIST,
    }
    return render(request, "index.html", context)


def show_experience(request):
    """Render the full list of experiences."""
    context = {
        "name": PROFILE_NAME,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def _get_projects(request):
    """Return (queryset, query) of projects filtered by the ``title`` GET param.

    Shared by ``show_projects`` and ``get_projects_json`` so both views stay
    in sync on how search filtering works without one calling the other.
    """
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return projects, title_query


def get_projects_json(request):
    """Return projects as JSON, optionally filtered by the ``title`` query param."""
    projects, _ = _get_projects(request)
    projects_json = serializers.serialize("json", projects)

    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    """Render the projects list page, with optional search by title."""
    projects, title_query = _get_projects(request)

    context = {
        "name": PROFILE_NAME,
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)


def create_project(request):
    """Show and process the "add project" form."""
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "projects_form.html", context)


def update_project(request, project_id):
    """Show and process the "edit project" form for an existing project."""
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "project": project,
    }
    return render(request, "projects_form.html", context)


def delete_project(request, project_id):
    """Delete a project on POST; any other method just redirects back."""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")

    return redirect("main:show_projects")
