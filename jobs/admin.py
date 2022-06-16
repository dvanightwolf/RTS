from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(JobPost)


@admin.register(Locations)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["job"]


admin.site.register(JobApply)
admin.site.register(PhoneNumber)
admin.site.register(RequiredEducation)
admin.site.register(RequiredExperience)
admin.site.register(RequiredSkills)

