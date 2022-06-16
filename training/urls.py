from django.urls import path
from . import views


# Create a name space for the training application
app_name = "training"

# Training's urls
urlpatterns = [
    path('', views.trainings_list, name='trainings_list'),
    path('<int:training_id>/', views.training_details, name='training_details'),
    path('add/', views.add_training, name='add_training'),
    path('edit/<training_id>/', views.training_edit, name='edit_training'),
    path('delete/<training_id>/', views.training_delete, name='training_delete'),
    path('payment/', views.payment, name='payment'),
    path('complete/', views.payment_complete, name='complete'),
    path('search_result/', views.search_training, name='search_training')
]

