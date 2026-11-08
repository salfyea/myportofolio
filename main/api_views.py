"""REST API views for projects (Tutorial 07) and skills (Individual Assignment 6)."""

from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, throttle_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Skill
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.serializers import (
    ProjectSerializer, SkillBulkDeleteSerializer, SkillSerializer,
)
from main.throttles import ApiStarThrottle, ApiWriteThrottle


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
@throttle_classes([ApiWriteThrottle])
def project_list(request):
    """List projects (``?title=`` searches) or create one as the owner."""
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
@throttle_classes([ApiWriteThrottle])
def project_detail(request, project_id):
    """Read, replace, partially update or delete one project."""
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([ApiStarThrottle])
def project_star(request, project_id):
    """Toggle the logged-in user's star; the account always comes from the session."""
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)

# Accepted values for ``?ordering=`` on the skill list ("stars" = most starred first).
SKILL_ORDERINGS = ("name", "stars")


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
@throttle_classes([ApiWriteThrottle])
def skill_list(request):
    """List skills or create one as the owner.

    Query parameters: ``name`` (contains), ``category`` (exact, ignoring case) and
    ``ordering`` (``name`` or ``stars``). Two queries serve any number of skills.
    """
    if request.method in ("GET", "HEAD"):
        skills = Skill.objects.prefetch_related("starred_by").order_by("name", "id")
        name = request.query_params.get("name", "").strip()
        if name:
            skills = skills.filter(name__icontains=name)
        category = request.query_params.get("category", "").strip()
        if category:
            skills = skills.filter(category__iexact=category)
        ordering = request.query_params.get("ordering", "name")
        if ordering not in SKILL_ORDERINGS:
            return Response(
                {"ordering": [f"Pilih salah satu dari: {', '.join(SKILL_ORDERINGS)}."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if ordering == "stars":
            skills = skills.annotate(num_stars=Count("starred_by")).order_by(
                "-num_stars", "name", "id",
            )
        serializer = SkillSerializer(skills, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = SkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
@throttle_classes([ApiWriteThrottle])
def skill_detail(request, skill_id):
    """Read a skill, or update (Editor, owner) or delete (owner) it."""
    skill = get_object_or_404(Skill.objects.prefetch_related("starred_by"), pk=skill_id)
    if request.method in ("GET", "HEAD"):
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = SkillSerializer(
        skill, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
@throttle_classes([ApiStarThrottle])
def skill_star(request, skill_id):
    """Toggle the logged-in user's star on a skill and return the fresh counts."""
    skill = get_object_or_404(Skill, pk=skill_id)
    # The starring account always comes from the session, never from the body.
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)
    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
@throttle_classes([ApiWriteThrottle])
def skill_bulk_delete(request):
    """Delete several skills in one request (owner only) and report how many went.

    Unknown and repeated ids are ignored instead of failing the whole request,
    and the delete runs in one transaction so it either happens fully or not at all.
    """
    serializer = SkillBulkDeleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        _, per_model = Skill.objects.filter(pk__in=set(serializer.validated_data["ids"])).delete()

    return Response({"deleted": per_model.get(Skill._meta.label, 0)})
