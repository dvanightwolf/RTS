from django.contrib import admin
from .models import Skills, Educations, Experiences, Countries, Grades, Category, Templates


# Register your models here.

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ["Skill"]


@admin.register(Educations)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ["education"]


@admin.register(Experiences)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ["experience"]


@admin.register(Grades)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ["grade"]


@admin.register(Countries)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ["country"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ["color"]
