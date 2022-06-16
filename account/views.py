from django.shortcuts import render, get_object_or_404, redirect
from training.models import Training
from .forms import *
from django.contrib.auth import login
from .models import *
from jobs.models import JobApply, JobPost


def register(request):
    return render(request, "registration/register.html")


def employee_register(request):
    """Handles user registration to the website."""
    # Is it a post request ?
    if request.method == "POST":
        # Instantiate a UserCreationForm and ProfileForm with the submitted data
        user_form = UserRegistrationForm(request.POST, files=request.FILES)
        employee_form = EmployeeForm(data=request.POST)
        # The data are valid ?
        if user_form.is_valid() and employee_form.is_valid():
            # Create a new user object but don't save it to the database just yet
            new_user = user_form.save(commit=False)
            # Set the provided password as this registration's password
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.is_employee = True
            # Did the user submit a profile picture?
            # If so set it as their picture otherwise it's blank ("gonna add a default pic later)
            if request.FILES:
                new_user.photo = request.FILES["photo"]
            new_user.save()
            # Save the profile in case more data were provided
            new_employee = employee_form.save(commit=False)
            new_employee.user = new_user
            new_employee.save()
            # Log the user in
            login(request, new_user)
            # A dictionary that holds the data to be sent to the corresponding html page
            context = {"new_user": new_user, }
            # Everything went well render send the user to the registration success page
            return render(request, "base.html", context)

    # Not a POST request
    else:
        # Instantiate an empty instance of both UserCreationForm and ProfileForm
        user_form = UserRegistrationForm()
        employee_form = EmployeeForm()
    # A dictionary that holds the data to be sent to the corresponding html page
    context = {"employee_form": employee_form, "user_form": user_form}
    # Registration wasn't successful for some reason so render the registration page with empty forms
    return render(request, "registration/employee_register.html", context)


def company_register(request):
    """Handles user registration to the website."""
    # Is it a post request ?
    if request.method == "POST":
        # Instantiate a UserCreationForm and ProfileForm with the submitted data
        user_form = UserRegistrationForm(request.POST)
        company_form = CompanyForm(data=request.POST)
        # The data are valid ?
        if user_form.is_valid() and company_form.is_valid():
            # Create a new user object but don't save it to the database just yet
            new_user = user_form.save(commit=False)
            # Set the provided password as this registration's password
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.is_company = True
            # Did the user submit a profile picture?
            # If so set it as their picture otherwise it's blank ("gonna add a default pic later)
            if request.FILES:
                new_user.photo = request.FILES["photo"]
            new_user.save()
            # Save the profile in case more data were provided
            new_company = company_form.save(commit=False)
            new_company.user = new_user
            new_company.save()
            # Log the user in
            login(request, new_user)
            # A dictionary that holds the data to be sent to the corresponding html page
            context = {"new_user": new_user}
            # Everything went well render send the user to the registration success page
            return render(request, "base.html", context)

    # Not a POST request
    else:
        # Instantiate an empty instance of both UserCreationForm and ProfileForm
        user_form = UserRegistrationForm()
        company_form = CompanyForm()
    # A dictionary that holds the data to be sent to the corresponding html page
    context = {"company_form": company_form, "user_form": user_form}
    # Registration wasn't successful for some reason so render the registration page with empty forms
    return render(request, "registration/company_register.html", context)


def show_profile(request, user_id):
    # Get the user's profile
    profile = Profile.objects.get(pk=user_id)
    info = None
    have_applies = False
    if profile.is_company:
        info = Company.objects.get(pk=user_id)
    elif profile.is_employee:
        info = Employee.objects.get(pk=profile.id)

    context = {"profile": profile, "info": info, "have_applies": have_applies}
    return render(request, "profile/profile.html", context)


def profile(request):
    # Get the user's profile
    profile = Profile.objects.get(pk=request.user.id)
    info = None
    applies = None
    jobs = None
    have_applies = False
    have_jobs = False
    if request.user.is_company:
        info = Company.objects.get(pk=request.user.id)
        jobs = JobPost.objects.filter(author=request.user)
        if jobs.count() != 0:
            have_jobs = True
    elif request.user.is_employee:
        info = Employee.objects.get(pk=request.user.id)
        applies = JobApply.objects.filter(user=request.user)
        jobs = JobPost.objects.filter(author=request.user)
        if applies.count() != 0:
            have_applies = True
        if jobs.count() != 0:
            have_jobs = True

    context = {"profile": profile, "info": info, "applies": applies, "jobs": jobs, "have_applies": have_applies,
               "have_jobs": have_jobs}
    return render(request, "profile/profile.html", context)


def delete_apply(request, apply_id):
    apply = get_object_or_404(JobApply, pk=apply_id)
    if request.method == 'POST':
        apply.delete()
        return redirect("account:profile")
    return render(request, 'profile/delete_apply.html')


def profile_edit(request):
    detail = None
    detail_form = None
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, files=request.FILES, instance=request.user)
        if request.user.is_employee:
            detail = Employee.objects.get(user=request.user)
            detail_form = EmployeeEditForm(request.POST, instance=detail)
        elif request.user.is_company:
            detail = Company.objects.get(user=request.user)
            detail_form = CompanyEditForm(request.POST, instance=detail)
        if request.user.is_staff:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('account:profile')
        else:
            if detail_form.is_valid() and profile_form.is_valid():
                detail_form.save()
                profile_form.save()
                return redirect('account:profile')
    else:
        profile_form = ProfileEditForm(instance=request.user)
        if request.user.is_employee:
            detail = Employee.objects.get(user=request.user)
            detail_form = EmployeeEditForm(instance=detail)
        elif request.user.is_company:
            detail = Company.objects.get(user=request.user)
            detail_form = CompanyEditForm(instance=detail)

    return render(request, 'profile/profile_edit.html', {'profile_form': profile_form, 'detail_form': detail_form})


def base(request):
    i = 0
    jobs = []
    trainings = []
    for job in JobPost.objects.all().order_by('-created'):
        if i < 3:
            jobs.append(job)
            i = i + 1
        else:
            i = 0
            break
    for training in Training.objects.all().order_by('-created'):
        if i < 3:
            trainings.append(training)
            i = i + 1
        else:
            i = 0
            break
    context = {'jobs': jobs, 'trainings': trainings}
    return render(request, 'RTS.html', context)
