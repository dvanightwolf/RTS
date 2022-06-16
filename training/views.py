from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Profile
from generics.models import Category, Countries
from .models import Training
from .forms import TrainingForm
from django.utils.text import slugify


def trainings_list(request):
    """Lists all the training."""
    # Query all trainings
    trainings = Training.objects.all()
    categories = Category.objects.all()
    countries = Countries.objects.all()
    # A dictionary to send trainings to the HTML
    context = {"trainings": trainings, 'categories': categories, 'countries': countries}
    # Render the trades_list html page
    return render(request, 'trainings_list.html', context)


def add_training(request):
    # Is it a post request ?
    if request.method == 'POST' and request.user.is_trainer:
        # Instantiate a Create Training with the submitted data
        training_form = TrainingForm(request.POST, files=request.FILES)
        # The data are valid ?
        if training_form.is_valid():
            # Create a new training object but don't save it to the database just yet
            new_training_form = training_form.save(commit=False)
            # request username to put it in training
            new_training_form.author = request.user
            # create friendly links
            new_training_form.slug = slugify(new_training_form.title)
            # save training
            new_training_form.save()
            # save tags
            training_form.save_m2m()
            # to go to training page
            return redirect('training:trainings_list')
    else:
        # create empty training
        training_form = TrainingForm()
    context = {'training_form': training_form}
    # to represent add training page
    return render(request, 'add_training.html', context)


def training_details(request, training_id):
    """Retrieves a Training object by id and slug """
    # Try to get a Training object with the passed id and slug
    training_to_display = get_object_or_404(Training, pk=training_id)
    context = {"training_to_display": training_to_display}
    # Render the details of the Training object
    return render(request, 'training_details.html', context)


def training_edit(request, training_id):
    # To search for a specific edit training by id
    training_to_edit = get_object_or_404(Training, id=training_id)
    # To check that the publisher himself
    if request.user != training_to_edit.author:
        return HttpResponse("No Permissions!")
    # Is it a post request ?
    if request.method == "POST" and request.user == training_to_edit.author:
        training_form = TrainingForm(instance=training_to_edit, data=request.POST, files=request.FILES)
        # The data are valid ?
        if training_form.is_valid():
            training_form.save(commit=False)
            # save training
            training_form.save()
            return redirect('training:trainings_list')
    else:
        training_form = TrainingForm(instance=training_to_edit)

    return render(request, "training_edit.html", {"form": training_form})


def training_delete(request, training_id):
    # to get the training id
    training = get_object_or_404(Training, id=training_id)
    # check if the one requesting is the training owner
    if request.user != training.author:
        return HttpResponse("No Permissions!")
    # Is it a post request ? and checks if its by the owner himself
    if request.method == "POST" and request.user == training.author:
        # if so delete the training
        training.delete()
        return redirect('training:trainings_list')
    return render(request, "training_delete.html")


def search_training(request):
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
            if Training.objects.filter(Q(tags__name__icontains=query)):
                results = Training.objects.filter(Q(tags__name=query))
            else:
                results = Training.objects.filter(Q(title__icontains=query) |
                                                  Q(description__icontains=query))

        elif query == '':
            results = Training.objects.all()

        if category != "0":
            results = results.filter(Q(category__name=sal_category[0].name))

        if country != "0":
            results = results.filter(Q(country__country=sal_country[0].country))

    return render(request, 'trainings_list.html', {"trainings": results, 'categories': categories, 'countries': countries})


def payment(request):
    return render(request, "paypal.html")


def payment_complete(request):
    profile = Profile.objects.get(pk=request.user.id)
    profile.is_trainer = True
    profile.save()
    return render(request, "complete.html")
