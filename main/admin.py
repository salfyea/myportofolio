from django.contrib import admin

# Register your models here.
from .models import Experience, Project


admin.site.register(Experience)
admin.site.register(Project)