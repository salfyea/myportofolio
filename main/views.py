from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Salwa Alifia Putri",
        "npm": "2506620280",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems Student at Universitas Indonesia with interests in "
            "product management, technology, business strategy, and digital innovation."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Salwa Alifia Putri",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)