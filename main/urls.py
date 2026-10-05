"""URL routes for the portfolio app."""

from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_projects,
    create_project,
    create_project_ajax,
    update_project,
    get_projects_json,
    delete_project,
    toggle_star,
    get_skills_json,
    show_skills_manage,
    create_skill,
    create_skill_ajax,
    update_skill,
    delete_skill,
    toggle_skill_star,
    chat_with_ai,
    register_user,
    login_user,
    logout_user,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/manage/", show_skills_manage, name="show_skills_manage"),
    path("skills/add/", create_skill, name="create_skill"),
    path("skills/add-ajax/", create_skill_ajax, name="create_skill_ajax"),
    path("skills/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("skills/<uuid:skill_id>/star/", toggle_skill_star, name="toggle_skill_star"),
    path("api/chat/", chat_with_ai, name="chat_with_ai"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]