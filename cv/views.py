from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from generics.views import save, delete_duplicate
from .models import CV, EmpExperience, EmpEducations, EmpSkills, \
    EmpLocations, EmpPhoneNumber
from .forms import CvForm, SkillFormset, EducationsFormset, \
    ExperienceFormset, LocationsFormset, PhoneNumberFormset
from jobs.models import JobApply
from generics.views import compare_cv


def have_cv(request):
    if request.user.is_employee:
        # get all CVs in the model.
        cv = CV.objects.filter(user=request.user)
        if cv:
            return redirect('cv:cv_show')
        else:
            return redirect('cv:create')


#####################################################################################


def show(request):
    """Show user's CV """
    # Make query to user's CV.
    cv = get_object_or_404(CV, user=request.user)
    experiences = EmpExperience.objects.filter(cv=cv).order_by('id')
    skills = EmpSkills.objects.filter(cv=cv).order_by('id')
    educations = EmpEducations.objects.filter(cv=cv).order_by('id')
    locations = EmpLocations.objects.filter(cv=cv).order_by('id')
    phone_number = EmpPhoneNumber.objects.filter(cv=cv).order_by('id')

    context = {}
    same_user = False
    if cv.user == request.user:
        same_user = True
        # Save user picture in variable.
        image = cv.picture

        # A dictionary to send CV and user's picture to the HTML.
        context = {"cv": cv, "image": image, "same_user": same_user,
                   "experiences": experiences, "skills": skills,
                   "educations": educations, "locations": locations,
                   "phone_number": phone_number,
                   }
    # Everything went well render send the user to the posted reviews page.
    return render(request, "show.html", context)


def create(request):
    """A view to make new CV."""
    # Is it a post request ?
    if request.method == 'POST':
        # make instance of CV.
        make_cv_form = CvForm(request.POST, files=request.FILES)
        experience_formset = ExperienceFormset(request.POST)
        education_formset = EducationsFormset(request.POST)
        skill_formset = SkillFormset(request.POST)
        location_formset = LocationsFormset(request.POST)
        phone_number_formset = PhoneNumberFormset(request.POST)

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        location_formset.prefix = "location"
        phone_number_formset.prefix = "phone-number"

        # The data are valid ?
        if make_cv_form.is_valid() and experience_formset.is_valid() \
                and skill_formset.is_valid() and education_formset.is_valid() \
                and location_formset.is_valid() and phone_number_formset.is_valid():
            # Create a new CV object but don't save it to the database just yet.
            new_cv_form = make_cv_form.save(commit=False)
            # request user ID to put it in CV.
            new_cv_form.user = request.user
            # is image included.
            if request.FILES:
                # add the image to CV.
                new_cv_form.image = request.FILES["picture"]

            save(
                request, new_cv_form, skill_formset,
                experience_formset, education_formset,
                location_formset, phone_number_formset
            )

            skills = EmpSkills.objects.filter(cv=new_cv_form)
            experiences = EmpExperience.objects.filter(cv=new_cv_form)
            educations = EmpEducations.objects.filter(cv=new_cv_form)

            delete_duplicate(experiences, educations, skills)

            return redirect('cv:home')
    else:
        # create empty CV.
        make_cv_form = CvForm()
        experience_formset = ExperienceFormset(queryset=EmpExperience.objects.none())
        education_formset = EducationsFormset(queryset=EmpEducations.objects.none())
        skill_formset = SkillFormset(queryset=EmpSkills.objects.none())
        location_formset = LocationsFormset(queryset=EmpLocations.objects.none())
        phone_number_formset = PhoneNumberFormset(queryset=EmpPhoneNumber.objects.none())

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        location_formset.prefix = "location"
        phone_number_formset.prefix = "phone-number"

    # a dictionary that hold form of CV.
    context = {"make_cv_form": make_cv_form, "experience_formset": experience_formset,
               "education_formset": education_formset, "skill_formset": skill_formset,
               "location_formset": location_formset, "phone_number_formset": phone_number_formset}
    # to represent make_cv page.
    return render(request, "create.html", context)


def delete(request):
    """Method to delete CV"""
    # To get the CV's id.
    cv_to_delete = get_object_or_404(CV, user=request.user)
    applies_to_delete = None
    have_applies = False
    # Check if the one requesting is the CV's owner.
    if request.user != cv_to_delete.user:
        return HttpResponse("You don't own this CV!")
    if JobApply.objects.filter(user=request.user).count() != 0:
        have_applies = True
    # Is it a post request ? and checks if its by the owner himself.
    if request.method == "POST":
        for apply in JobApply.objects.filter(user=request.user):
            apply.delete()
        # If so delete the CV.
        cv_to_delete.delete()
        # Return to CV page.
        return redirect('account:profile')
    context = {"have_applies": have_applies}
    return render(request, "delete.html", context)


def edit(request):
    cv = get_object_or_404(CV, user=request.user)
    # Is it a post request ?
    if request.method == 'POST':
        # make instance of CV.
        make_cv_form = CvForm(data=request.POST, files=request.FILES, instance=cv)
        experience_formset = ExperienceFormset(request.POST, queryset=EmpExperience.objects.filter(cv=cv))
        education_formset = EducationsFormset(request.POST, queryset=EmpEducations.objects.filter(cv=cv))
        skill_formset = SkillFormset(request.POST, queryset=EmpSkills.objects.filter(cv=cv))
        location_formset = LocationsFormset(request.POST, queryset=EmpLocations.objects.filter(cv=cv))
        phone_number_formset = PhoneNumberFormset(request.POST, queryset=EmpPhoneNumber.objects.filter(cv=cv))

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        location_formset.prefix = "location"
        phone_number_formset.prefix = "phone-number"

        # The data are valid ?
        if make_cv_form.is_valid() and skill_formset.is_valid() \
                and location_formset.is_valid() and phone_number_formset.is_valid() \
                and education_formset.is_valid() and experience_formset.is_valid():
            # Create a new CV object but don't save it to the database just yet.
            new_cv_form = make_cv_form.save(commit=False)

            save(
                request, new_cv_form, skill_formset,
                experience_formset, education_formset,
                location_formset, phone_number_formset,
            )

            skills = EmpSkills.objects.filter(cv=new_cv_form)
            experiences = EmpExperience.objects.filter(cv=new_cv_form)
            educations = EmpEducations.objects.filter(cv=new_cv_form)

            delete_duplicate(experiences, educations, skills)

            applies = JobApply.objects.filter(user=cv.user)

            for apply in applies:
                apply.evaluation = compare_cv(request, apply.job_id, apply.user)
                apply.save()

            return redirect('cv:cv_show')
    else:
        # create empty CV.
        make_cv_form = CvForm(instance=cv)
        experience_formset = ExperienceFormset(queryset=EmpExperience.objects.filter(cv=cv))
        education_formset = EducationsFormset(queryset=EmpEducations.objects.filter(cv=cv))
        skill_formset = SkillFormset(queryset=EmpSkills.objects.filter(cv=cv))
        location_formset = LocationsFormset(queryset=EmpLocations.objects.filter(cv=cv))
        phone_number_formset = PhoneNumberFormset(queryset=EmpPhoneNumber.objects.filter(cv=cv))

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        location_formset.prefix = "location"
        phone_number_formset.prefix = "phone-number"

    # a dictionary that hold form of CV.
    context = {"make_cv_form": make_cv_form, "experience_formset": experience_formset,
               "education_formset": education_formset, "skill_formset": skill_formset,
               "location_formset": location_formset, "phone_number_formset": phone_number_formset}
    # to represent make_cv page.
    return render(request, "edit.html", context)
