from django.urls import path
from . import views
from generics.views import preview

# Namespace for CV app.
app_name = "cv"

# CV urls.
urlpatterns = [
    # Home's urls
    path('', views.have_cv, name="home"),
    # CV's urls.
    path('cv_show/', views.show, name='cv_show'),
    path('cv_make/', views.create, name='create'),
    path('delete/', views.delete, name='delete_cv'),
    path('edit/', views.edit, name='edit'),
    path('preview/<cv_id>/', preview, name='preview'),
]
