from django.contrib import admin
from .models import CV, EmpExperience, EmpSkills, EmpEducations, EmpLocations, EmpPhoneNumber


# Register your models here.
@admin.register(CV)
class CvAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "email", "picture", "interests"]


@admin.register(EmpExperience)
class EmpExperienceAdmin(admin.ModelAdmin):
    list_display = ["cv", "experience", "start", "end"]


@admin.register(EmpSkills)
class EmpSkillsAdmin(admin.ModelAdmin):
    list_display = ["cv", "skill", "grade"]


@admin.register(EmpEducations)
class EmpEducationAdmin(admin.ModelAdmin):
    list_display = ["cv", "education", "date"]


@admin.register(EmpLocations)
class EmpLocationAdmin(admin.ModelAdmin):
    list_display = ["cv", "country"]


@admin.register(EmpPhoneNumber)
class EmpEducationAdmin(admin.ModelAdmin):
    list_display = ["cv", "phone_number"]


