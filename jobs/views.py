from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from account.models import Profile
from generics.views import compare_cv
from cv.views import delete_duplicate
from .forms import *
from django.utils.text import slugify
from cv.models import CV, EmpExperience, EmpEducations, EmpSkills, EmpLocations, EmpPhoneNumber
from django.db.models import Q
from generics.models import Category, Countries


# Create your views here.
def search_job(request):
    results = []
    categories = Category.objects.all()
    countries = Countries.objects.all()
    sal_category = Category()
    sal_country = Countries()
    query = None
    if request.method == "GET":
        query = request.GET.get('search')
        category = request.GET.get("category_id")
        country = request.GET.get("country_id")

        if category:
            sal_category = Category.objects.filter(pk=category)

        if country:
            sal_country = Countries.objects.filter(pk=country)

        if query != '':
            if JobPost.objects.filter(Q(tags__name__icontains=query)):
                results = JobPost.objects.filter(Q(tags__name=query))
            else:
                results = JobPost.objects.filter(Q(heading__icontains=query) |
                                                 Q(description__icontains=query))

        elif query == '':
            results = JobPost.objects.all().order_by('-id')

        if category != "0":
            results = results.filter(Q(category__name=sal_category[0].name))

        if country != "0":
            results = results.filter(Q(locations__country__country=sal_country[0].country))

    return render(request, 'job_post.html', {'jobs': results, 'categories': categories, 'countries': countries})


def posts(request):
    user_photo = Profile.objects.all().order_by('-id')
    categories = Category.objects.all()
    countries = Countries.objects.all()
    job = JobPost.objects.all().order_by('-id')

    context = {'jobs': job, "categories": categories, 'countries': countries}
    return render(request, 'job_post.html', context)


def add_job(request):
    if request.method == 'POST':
        job_form = JobPostForm(request.POST)
        experience_formset = ExperienceFormset(request.POST)
        education_formset = EducationFormset(request.POST)
        skill_formset = SkillFormset(request.POST)
        phone_number_formset = PhoneNumberFormset(request.POST)
        locations_formset = LocationsFormset(request.POST)
        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        phone_number_formset.prefix = "phone"
        locations_formset.prefix = "location"

        # The data are valid ?
        if job_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() \
                and skill_formset.is_valid() and locations_formset.is_valid() \
                and phone_number_formset.is_valid():
            new_job_form = job_form.save(commit=False)
            new_job_form.author = request.user
            new_job_form.slug = slugify(new_job_form.heading)

            for experience_form in experience_formset:
                new_experience_form = experience_form.save(commit=False)
                new_experience_form.job = new_job_form

            for education_form in education_formset:
                new_education_form = education_form.save(commit=False)
                new_education_form.job = new_job_form

            for skill_form in skill_formset:
                new_skill_form = skill_form.save(commit=False)
                new_skill_form.job = new_job_form

            for locations_form in locations_formset:
                new_locations_form = locations_form.save(commit=False)
                new_locations_form.job = new_job_form

            for phone_number_form in phone_number_formset:
                new_phone_number_form = phone_number_form.save(commit=False)
                new_phone_number_form.job = new_job_form

            new_job_form.save()
            job_form.save_m2m()

            experience_formset.save()
            education_formset.save()
            skill_formset.save()
            locations_formset.save()
            phone_number_formset.save()

            return redirect('jobs:post_list')

    else:
        job_form = JobPostForm()

        experience_formset = ExperienceFormset(queryset=RequiredExperience.objects.none())
        education_formset = EducationFormset(queryset=RequiredEducation.objects.none())
        skill_formset = SkillFormset(queryset=RequiredSkills.objects.none())
        locations_formset = LocationsFormset(queryset=Locations.objects.none())
        phone_number_formset = PhoneNumberFormset(queryset=PhoneNumber.objects.none())

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        locations_formset.prefix = "location"
        phone_number_formset.prefix = "phone"

    context = {"job_form": job_form, "experience_formset": experience_formset,
               "education_formset": education_formset, "skill_formset": skill_formset,
               "locations_formset": locations_formset, "phone_number_formset": phone_number_formset}

    return render(request, "post_a_job.html", context)


def edit_job(request, job_id):
    """EDIT THE job"""
    job = get_object_or_404(JobPost, pk=job_id)
    if request.method == 'POST':
        job_form = JobPostForm(request.POST, instance=job)
        experience_formset = ExperienceFormset(request.POST, queryset=RequiredExperience.objects.filter(job=job))
        education_formset = EducationFormset(request.POST, queryset=RequiredEducation.objects.filter(job=job))
        skill_formset = SkillFormset(request.POST, queryset=RequiredSkills.objects.filter(job=job))
        phone_number_formset = PhoneNumberFormset(request.POST, queryset=PhoneNumber.objects.filter(job=job))
        locations_formset = LocationsFormset(request.POST, queryset=Locations.objects.filter(job=job))
        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        phone_number_formset.prefix = "phone"
        locations_formset.prefix = "location"

        # The data are valid ?
        if job_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid() \
                and skill_formset.is_valid() and locations_formset.is_valid() \
                and phone_number_formset.is_valid():
            new_job_form = job_form.save(commit=False)
            new_job_form.author = request.user
            new_job_form.slug = slugify(new_job_form.heading)

            for experience_form in experience_formset:
                new_experience_form = experience_form.save(commit=False)
                new_experience_form.job = new_job_form

            for education_form in education_formset:
                new_education_form = education_form.save(commit=False)
                new_education_form.job = new_job_form

            for skill_form in skill_formset:
                new_skill_form = skill_form.save(commit=False)
                new_skill_form.job = new_job_form

            for locations_form in locations_formset:
                new_locations_form = locations_form.save(commit=False)
                new_locations_form.job = new_job_form

            for phone_number_form in phone_number_formset:
                new_phone_number_form = phone_number_form.save(commit=False)
                new_phone_number_form.job = new_job_form

            new_job_form.save()
            job_form.save_m2m()

            experience_formset.save()
            education_formset.save()
            skill_formset.save()
            locations_formset.save()
            phone_number_formset.save()

            skills = RequiredSkills.objects.filter(job=new_job_form)
            experiences = RequiredExperience.objects.filter(job=new_job_form)
            educations = RequiredEducation.objects.filter(job=new_job_form)

            delete_duplicate(experiences, educations, skills)

            applies = JobApply.objects.filter(job=new_job_form)

            for apply in applies:
                apply.evaluation = compare_cv(request, apply.job_id, apply.user)
                apply.save()

            return redirect('jobs:post_list')

    else:
        job_form = JobPostForm(instance=job)

        experience_formset = ExperienceFormset(queryset=RequiredExperience.objects.filter(job=job))
        education_formset = EducationFormset(queryset=RequiredEducation.objects.filter(job=job))
        skill_formset = SkillFormset(queryset=RequiredSkills.objects.filter(job=job))
        locations_formset = LocationsFormset(queryset=Locations.objects.filter(job=job))
        phone_number_formset = PhoneNumberFormset(queryset=PhoneNumber.objects.filter(job=job))

        experience_formset.prefix = "experience"
        education_formset.prefix = "education"
        skill_formset.prefix = "skill"
        locations_formset.prefix = "location"
        phone_number_formset.prefix = "phone"

    context = {"job_form": job_form, "experience_formset": experience_formset,
               "education_formset": education_formset, "skill_formset": skill_formset,
               "locations_formset": locations_formset, "phone_number_formset": phone_number_formset}

    return render(request, "edit_job.html", context)


def delete_job(request, job_id):
    """Method to delete jobs"""
    # To get the job's id.
    job_to_delete = get_object_or_404(JobPost, pk=job_id)
    # Check if the one requesting is the job's owner.
    if request.user != job_to_delete.author:
        return HttpResponse("You don't own this job!")
    # Is it a post request ? and checks if its by the owner himself.
    if request.method == "POST" and request.user == job_to_delete.author:
        # If so delete the job.
        job_to_delete.delete()
        # Return to job page.
        return redirect('jobs:post_list')
    context = {"job_to_delete": job_to_delete}
    return render(request, "delete_job.html", context)


def job_details(request, job_id):
    """Retrieves a job object by id and slug """
    # Try to get a job object with the passed id and slug

    job = get_object_or_404(JobPost, pk=job_id)

    experiences = RequiredExperience.objects.filter(job_id=job).order_by('id')
    educations = RequiredEducation.objects.filter(job_id=job).order_by('id')
    skills = RequiredSkills.objects.filter(job_id=job).order_by('id')
    locations = Locations.objects.filter(job_id=job).order_by('id')
    phone_numbers = PhoneNumber.objects.filter(job_id=job).order_by('id')

    same_user = False
    can_apply = False
    is_company = False
    context = {}
    if job.author == request.user:
        same_user = True
        is_company = True
    elif request.user.is_authenticated and request.user.is_employee:
        can_apply = True

    context = {"job": job, "same_user": same_user,
               "experiences": experiences, "skills": skills,
               "educations": educations, "locations": locations, "phone_numbers": phone_numbers, "can_apply": can_apply}
    return render(request, "job_details.html", context)


def add_apply(request, job_id):
    can_apply = False
    if JobApply.objects.filter(user=request.user, job=job_id).count() == 0 and CV.objects.filter(user=request.user):
        can_apply = True
    if can_apply:
        if request.method == 'POST':
            job_post = get_object_or_404(JobPost, id=job_id)
            apply_form = JobApplyForm(request.POST)
            if apply_form.is_valid():
                new_apply_form = apply_form.save(commit=False)
                new_apply_form.user = request.user
                new_apply_form.job = job_post
                new_apply_form.evaluation = compare_cv(request, job_id, request.user)
                new_apply_form.save()

                return redirect('jobs:post_list')
        else:
            apply_form = JobApplyForm()
    else:
        if CV.objects.filter(user=request.user).count() == 0:
            return redirect('cv:create')
        else:
            return HttpResponse("<p>you cant apply to this post more than one time!<p>")
    context = {'apply_form': apply_form}
    return render(request, 'add_apply.html', context)


def show_applies(request, job_id):
    applies = JobApply.objects.filter(job_id=job_id).order_by('-evaluation')
    cvs = []

    for apply in applies:
        cvs.append(get_object_or_404(CV, user=apply.user))

    count = applies.count()
    context = {'cvs': cvs, "count": count, "applies": applies}

    return render(request, 'show_applies.html', context)


def apply_details(request, apply_id):
    apply = JobApply.objects.get(pk=apply_id)
    cv = CV.objects.get(user=apply.user)
    educations = EmpEducations.objects.filter(cv=cv).order_by('id')
    experiences = EmpExperience.objects.filter(cv=cv).order_by('id')
    skills = EmpSkills.objects.filter(cv=cv).order_by('id')
    locations = EmpLocations.objects.filter(cv=cv).order_by('id')
    phone_numbers = EmpPhoneNumber.objects.filter(cv=cv).order_by('id')

    context = {"apply": apply, "cv": cv, "educations": educations, "experiences": experiences,
               "skills": skills, "locations": locations, "phone_numbers": phone_numbers}
    return render(request, 'apply_details.html', context)
