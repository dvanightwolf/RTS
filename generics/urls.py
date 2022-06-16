from django.urls import path
from . import views
app_name = "generics"

urlpatterns = [
    path('pdf/', views.pdf, name='ppdf')
]
