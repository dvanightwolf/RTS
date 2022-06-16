from django.urls import path
from . import views
app_name = "jobs"
urlpatterns = [
    path('', views.posts, name='post_list'),
    path('add_job/', views.add_job, name='add_job'),
    path('search_job/', views.search_job, name='search_job'),
    path('<job_id>/', views.job_details, name="job_details"),
    path('edit/<int:job_id>/', views.edit_job, name='job_edit'),
    path('add_apply/<job_id>/', views.add_apply, name='add_apply'),
    path('delete/<int:job_id>/', views.delete_job, name="job_delete"),
    path('show_applies/<job_id>/', views.show_applies, name='show_applies'),
    path('apply_details/<int:apply_id>/', views.apply_details, name='apply_details')

]
