from training.models import Training
from django.contrib import admin


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ["author", "email", "title", "description", "price", "phone_number", "created"]
