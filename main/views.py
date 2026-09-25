"""Views for the portfolio app.

Covers the profile/experience pages plus the projects CRUD-lite flow
(list with search, JSON API, create, and delete).
"""

import json

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ProjectForm, SkillForm
from main.models import Experience, Project, Skill

PROFILE_NAME = "Salwa Alifia Putri"

CHAT_SYSTEM_INSTRUCTION = (
    "Kamu adalah asisten AI di website portofolio Salwa Alifia Putri. Jawab "
    "pertanyaan pengunjung hanya berdasarkan data berikut, jangan mengarang "
    "informasi di luar ini. Kalau ditanya hal di luar topik ini (misalnya "
    "hal umum yang tidak berhubungan dengan Salwa, atau data yang memang "
    "tidak tersedia di sini), jangan coba jawab pertanyaannya. Sampaikan "
    "dengan nada ceria dan ramah bahwa itu di luar hal yang bisa kamu "
    "bantu, lalu arahkan pengunjung untuk bertanya seputar profil, "
    "pendidikan, pengalaman organisasi, sertifikasi, skill, atau proyek "
    "Salwa saja.\n\n"
    "DATA DIRI:\n"
    "Nama: Salwa Alifia Putri. Domisili: Jakarta, Indonesia. "
    "Kontak: alfyosya@gmail.com, github.com/salfyea, "
    "linkedin.com/in/salwaalfptr.\n\n"
    "PENDIDIKAN:\n"
    "Universitas Indonesia, Depok - S1 Ilmu Komputer, program studi Sistem "
    "Informasi, 2025-2029 (masih berlangsung).\n\n"
    "PENGHARGAAN:\n"
    "Juara 1 Mini Case Competition Billions 2026 sebagai Product Lead, "
    "menyusun strategi dan roadmap produk Livin Momentum dengan proyeksi ROI "
    "127.7% dalam lima tahun. "
    "TOP 50 MAPID WebGIS Competition 2026 sebagai Product Lead, memimpin "
    "TitikTemu, WebGIS berbasis AI yang menghubungkan UMKM lokal dengan "
    "peluang berbasis transit. "
    "Semifinalis Business Case Competition Astranauts 2026 sebagai Product "
    "Lead, mengembangkan roadmap dan business case E-QUAL dengan proyeksi "
    "ROI 70% dan penghematan biaya 13.7%. "
    "TOP 5 WECTION Business Model Canvas Competition 2026 sebagai Product "
    "and Tech Lead, memimpin desain produk dan business model AgriLoom "
    "dengan proyeksi pendapatan Rp8.14 miliar di tahun kelima.\n\n"
    "PENGALAMAN DAN KEPEMIMPINAN:\n"
    "VPIC of Business Development di Open House Fasilkom UI 2026 (Juli 2026 "
    "sampai sekarang), memimpin strategi sponsorship dan partnership. "
    "Co-Founder and Product Lead di OTWPTN (Mei 2026 sampai sekarang), "
    "program mentoring untuk jalur masuk universitas negeri non-tes, sudah "
    "punya 53 peserta berbayar dan menghasilkan Rp5.5 juta pendapatan di "
    "tahun pertama. "
    "Peserta Product Management Academy di COMPFEST 18 (April 2026 sampai "
    "sekarang), memperdalam product discovery, user research, "
    "prioritization, product metrics, dan roadmapping.\n\n"
    "SERTIFIKASI:\n"
    "McKinsey.org Forward Program dari McKinsey and Company. "
    "Advanced Certificate on Global Citizenship for Social Impact dari "
    "University of Pennsylvania. "
    "Artificial Intelligence, Robotic, and Drone Making dari Indian "
    "Institute of Technology, Delhi.\n\n"
    "SKILL PRODUCT MANAGEMENT:\n"
    "Product Strategy and Roadmapping, User Research, Market Analysis, A/B "
    "Testing, Agile Methodologies seperti Scrum dan Kanban, Go-to-Market "
    "Strategy, Experimentation, Stakeholder Management, Data Analysis "
    "dengan Google Analytics, Amplitude, Mixpanel, dan Posthog, serta "
    "Business Development.\n\n"
    "SKILL TEKNIS:\n"
    "Figma, Notion, Jira, Supabase, Python, JavaScript dan TypeScript "
    "termasuk Node.js, React, dan Next.js, Vercel, Git dan GitHub, Docker, "
    "serta perkakas AI seperti Claude Code dan AI Agents.\n\n"
    "ATURAN FORMAT JAWABAN (WAJIB DIIKUTI):\n"
    "Tulis jawaban sebagai teks biasa saja. Jangan pernah memakai tanda "
    "bintang (* atau **) untuk bold, italic, maupun bullet list. Jangan "
    "pernah memakai tanda em dash (—). Kalau butuh tanda pisah, pakai koma "
    "atau titik, atau tanda hubung biasa (-) yang diapit spasi. Kalau perlu "
    "membuat daftar, tulis pakai angka biasa seperti '1.', '2.', atau pakai "
    "baris baru dengan tanda hubung biasa, bukan markdown. Jawab singkat, "
    "ramah, dan dalam Bahasa Indonesia kecuali diminta bahasa lain."
)


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

    if request.method == "POST":
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, project tidak ditambahkan.")
        elif form.is_valid():
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

    if request.method == "POST":
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, project tidak diperbarui.")
        elif form.is_valid():
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


@require_POST
def verify_secret_key(request):
    """Check a submitted secret key against PORTFOLIO_EDIT_KEY, without
    saving anything. Used by the create/edit form's password gate so wrong
    codes never even reveal the data fields. The real save views still
    check the key again on submit — this endpoint is just for the gate UX.
    """
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"valid": False}, status=400)

    secret_key = payload.get("secret_key", "")
    is_valid = bool(settings.PORTFOLIO_EDIT_KEY) and secret_key == settings.PORTFOLIO_EDIT_KEY

    return JsonResponse({"valid": is_valid})


@require_POST
def chat_with_ai(request):
    """Relay a visitor's message to Gemini and return its reply as JSON.

    Relies on Django's normal CSRF protection (this view is NOT
    csrf_exempt) — the frontend must send the csrftoken cookie's value
    in the X-CSRFToken header, same as any other same-origin POST.
    """
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Body request harus berupa JSON yang valid."}, status=400)

    message = payload.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return JsonResponse({"error": "Field 'message' wajib diisi."}, status=400)

    if not settings.GEMINI_API_KEY:
        return JsonResponse(
            {"error": "Fitur chat AI belum dikonfigurasi (GEMINI_API_KEY kosong)."},
            status=503,
        )

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            "gemini-3.6-flash",
            system_instruction=CHAT_SYSTEM_INSTRUCTION,
        )
        response = model.generate_content(message.strip())
        reply = (response.text or "").strip()
    except google_exceptions.Unauthenticated:
        return JsonResponse({"error": "GEMINI_API_KEY tidak valid."}, status=502)
    except google_exceptions.GoogleAPIError:
        return JsonResponse(
            {"error": "Gagal menghubungi layanan AI, silakan coba lagi."},
            status=502,
        )
    except Exception:
        return JsonResponse(
            {"error": "Terjadi kesalahan tak terduga saat memproses chat."},
            status=500,
        )

    if not reply:
        return JsonResponse(
            {"error": "AI tidak memberikan jawaban, silakan coba lagi."},
            status=502,
        )

    return JsonResponse({"reply": reply})


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

    if request.method == "POST":
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, skill tidak ditambahkan.")
        elif form.is_valid():
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

    if request.method == "POST":
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, skill tidak diperbarui.")
        elif form.is_valid():
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
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, skill tidak dihapus.")
        else:
            skill.delete()
            messages.success(request, "Skill berhasil dihapus!")

    return redirect("main:show_skills_manage")


def delete_project(request, project_id):
    """Delete a project on POST; any other method just redirects back."""
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if not settings.PORTFOLIO_EDIT_KEY or request.POST.get("secret_key") != settings.PORTFOLIO_EDIT_KEY:
            messages.error(request, "Kode rahasia salah, project tidak dihapus.")
        else:
            project.delete()
            messages.success(request, "Project berhasil dihapus!")

    return redirect("main:show_projects")


def register_user(request):
    """Show and process the registration form for new visitor accounts."""
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect("main:login")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "register.html", context)
