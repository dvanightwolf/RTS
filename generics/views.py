import os
import pdfkit
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import requests
from django.template.loader import get_template
from xhtml2pdf import pisa

from account.models import Profile

from cv.models import *
from jobs.models import *
from .models import Grades


# Create your views here.


def compare_cv(request, job_id, apply_user):
    evaluate = int()
    job = JobPost.objects.get(id=job_id)
    cv = CV.objects.get(user=apply_user)
    job_experiences = RequiredExperience.objects.filter(job_id=job)
    job_skills = RequiredSkills.objects.filter(job_id=job)
    job_educations = RequiredEducation.objects.filter(job_id=job)
    cv_experiences = EmpExperience.objects.filter(cv=cv)
    cv_skills = EmpSkills.objects.filter(cv=cv)
    cv_educations = EmpEducations.objects.filter(cv=cv)

    for cv_experience in cv_experiences:
        year = cv_experience.end.year - cv_experience.start.year
        for job_experience in job_experiences:
            if cv_experience.experience.experience == job_experience.experience.experience:
                if year >= 1:
                    evaluate = evaluate + 100
                    for i in range(year - 1):
                        evaluate = evaluate + 50
                elif year < 1:
                    continue

    for cv_skill in cv_skills:
        for job_skill in job_skills:
            if cv_skill.skill.Skill == job_skill.skill.Skill:
                if cv_skill.grade.grade == Grades.objects.get(pk=1).grade:
                    evaluate = evaluate + 10
                elif cv_skill.grade.grade == Grades.objects.get(pk=2).grade:
                    evaluate = evaluate + 7
                elif cv_skill.grade.grade == Grades.objects.get(pk=3).grade:
                    evaluate = evaluate + 4

    for cv_education in cv_educations:
        if cv_educations.count() <= 15:
            for job_education in job_educations:
                if cv_education.education.education == job_education.education.education:
                    evaluate = evaluate + 55

    return evaluate


#####################################################################################


def delete_duplicate(experiences, educations, skills):
    for skill in skills:
        for sk in skills:
            if skill.skill == sk.skill \
                    and sk.id is not None and skill.id is not None:
                if sk.id != skill.id:
                    sk.delete()

    for experience in experiences:
        for exp in experiences:
            if experience.experience == exp.experience \
                    and exp.id is not None and experience.id is not None:
                if exp.id != experience.id:
                    exp.delete()

    for education in educations:
        for ed in educations:
            if education.education == ed.education \
                    and ed.id is not None and education.id is not None:
                if ed.id != education.id:
                    ed.delete()


#####################################################################################


def save(request, new_cv_form, skill_formset,
         experience_formset, education_formset,
         location_formset, phone_number_formset):
    for skill_form in skill_formset:
        if skill_form.is_valid():
            new_skill_form = skill_form.save(commit=False)
            new_skill_form.cv = new_cv_form

    for location_form in location_formset:
        new_location_form = location_form.save(commit=False)
        new_location_form.cv = new_cv_form

    for phone_number_form in phone_number_formset:
        new_phone_number_form = phone_number_form.save(commit=False)
        new_phone_number_form.cv = new_cv_form

    for experience_form in experience_formset:
        if experience_form.is_valid():
            new_experience_form = experience_form.save(commit=False)
            new_experience_form.cv = new_cv_form

    for education_form in education_formset:
        if education_form.is_valid():
            new_education_form = education_form.save(commit=False)
            new_education_form.cv = new_cv_form

    # save CV.
    new_cv_form.save()
    experience_formset.save()
    education_formset.save()
    skill_formset.save()
    location_formset.save()
    phone_number_formset.save()


####################################################################################


def preview(request, cv_id):
    cv = get_object_or_404(CV, pk=cv_id)
    color = request.GET.get('color', 'blue')
    my_color = Templates.objects.get(pk=1)
    my_color.color = color
    my_color.save()
    template = "default " + color
    # Default Template Values
    template_name = 'cv/default.html'

    if not template is None:
        if not template == "":
            template_name = 'cv/' + template.split(" ")[0].lower() + '.html'
            color = template.split(" ")[1]
    image = cv.picture
    context = {
        'cv': cv,
        'image': image,
        'experiences': EmpExperience.objects.filter(cv=cv).order_by('id'),
        'skills': EmpSkills.objects.filter(cv=cv).order_by('id'),
        'educations': EmpEducations.objects.filter(cv=cv).order_by('id'),
        'locations': EmpLocations.objects.filter(cv=cv).order_by('id'),
        'phonenumbers': EmpPhoneNumber.objects.filter(cv=cv).order_by('id'),
        'color': color.lower(),
    }
    return render(request, template_name, context)


def pdf(request):
    cv = get_object_or_404(CV, user=request.user)
    my_color = Templates.objects.get(pk=1)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    cv_pdf = pdfkit.from_url(f"http://127.0.0.1:8000/cv/preview/{cv.id}/?color={my_color}", configuration=config)
    response = HttpResponse(cv_pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Cv.pdf"'
    return response



