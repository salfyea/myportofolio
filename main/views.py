"""Views for the portfolio app.

Covers the profile/experience pages plus the projects CRUD-lite flow
(list with search, JSON API, create, and delete).
"""

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ProjectForm, SkillForm
from main.models import Experience, Project, Skill

PROFILE_NAME = "Salwa Alifia Putri"


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
        "skill_list": Skill.objects.all(),
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


def get_skills_json(request):
    """Return skills as JSON."""
    skills = Skill.objects.all()
    skills_json = serializers.serialize("json", skills)

    return HttpResponse(skills_json, content_type="application/json")


def show_skills_manage(request):
    """Render the skills management page listing every Skill."""
    context = {
        "name": PROFILE_NAME,
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills_manage.html", context)


def create_skill(request):
    """Show and process the "add skill" form."""
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills_manage")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "skills_form.html", context)


def update_skill(request, skill_id):
    """Show and process the "edit skill" form for an existing skill."""
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skills_manage")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "skill": skill,
    }
    return render(request, "skills_form.html", context)


def delete_skill(request, skill_id):
    """Delete a skill on POST; any other method just redirects back."""
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")

    return redirect("main:show_skills_manage")


def delete_project(request, project_id):
    """Delete a project on POST; any other method just redirects back."""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")

    return redirect("main:show_projects")
