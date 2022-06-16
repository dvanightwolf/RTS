from django.urls import path, reverse_lazy
from account import views
from django.contrib.auth import views as auth_views


# Create a name space for the account application
app_name = "account"

# Account's URLs
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                               success_url=reverse_lazy('account:password_change_done')),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                              success_url=reverse_lazy('account:password_reset_done')),
         name='registration/password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('company_register/', views.company_register, name='company_register'),
    path('employee_register/', views.employee_register, name='employee_register'),
    path('profile/', views.profile, name="profile"),
    path('profile/<user_id>/', views.show_profile, name="show_profile"),
    path('edit/', views.profile_edit, name="profile_edit"),
    path('delete_apply/<int:apply_id>/', views.delete_apply, name='delete_apply'),
]
