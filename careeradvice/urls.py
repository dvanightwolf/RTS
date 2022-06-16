from django.urls import path
from . import views
app_name = "careeradvice"

urlpatterns = [
    path('', views.advices, name="advice_list"),
    path('search_advices/', views.search_advices, name="search_advices"),
    path('add_advice/', views.add_advice, name="add_advice"),
    path('details/<int:advice_id>/', views.advice_details, name="advice_details"),
    path('edit/<int:advice_id>/', views.edit_advice, name='advice_edit'),
    path('delete_advice/<int:advice_id>/', views.delete_advice, name="advice_delete")
]
