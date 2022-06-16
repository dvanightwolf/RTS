from django.contrib import admin
from .models import Profile, Employee, Company


# Register the profile model to the admin site
@admin.register(Profile)
class registerAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "bio", "phone_number", "is_employee", "is_company", "is_staff"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "gender"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["user", "website", "location"]
