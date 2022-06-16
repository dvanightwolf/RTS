from django.shortcuts import redirect, render, get_object_or_404
from .models import CareerAdvice
from .forms import CareerAdviceForm
from django.utils.text import slugify
from django.http import HttpResponse
from django.db.models import Q
from generics.models import Category


def search_advices(request):
    results = []
    categories = Category.objects.all()
    sal_category = Category()
    query = None
    if request.method == "GET":
        query = request.GET.get('search')
        category = request.GET.get("category_id", "talon")
        if category:
            sal_category = Category.objects.filter(pk=category)
        if query != '':
            if CareerAdvice.objects.filter(Q(tags__name__icontains=query)):
                results = CareerAdvice.objects.filter(Q(tags__name=query))

            else:
                results = CareerAdvice.objects.filter(Q(heading__icontains=query) |
                                                      Q(text__icontains=query))

        elif query == "":
            results = CareerAdvice.objects.all()

        if category != "0":
            results = results.filter(Q(category__name=sal_category[0].name))

        if results.count != 0:
            query = "talon"

    return render(request, 'advices.html', {'query': query, 'advices': results, "categories": categories})


def advices(request):
    categories = Category.objects.all()
    advice = CareerAdvice.objects.all()
    context = {'advices': advice, "categories": categories}
    return render(request, 'advices.html', context)


def add_advice(request):
    if request.method == 'POST':
        advice = CareerAdviceForm(request.POST)
        if advice.is_valid():
            new_advice = advice.save(commit=False)
            new_advice.author = request.user
            new_advice.slug = slugify(new_advice.heading)
            new_advice.save()
            advice.save_m2m()
            return redirect('../')
    else:
        advice = CareerAdviceForm()
    context = {'advice': advice}
    return render(request, 'add_advice.html', context)


def advice_details(request, advice_id):
    """Retrieves a advice object by id and slug """
    # Try to get a advice object with the passed id and slug
    advice = get_object_or_404(CareerAdvice, pk=advice_id)
    same_user = False
    if advice.author == request.user:
        same_user = True
    # Data to be sent over to the corresponding html page
    context = {'advice': advice, 'same_user': same_user}
    # Render the details of the advice object
    return render(request, 'advice_details.html', context)


def delete_advice(request, advice_id):
    """ Method to delete jobs"""
    # To get advice id.
    advice_to_delete = get_object_or_404(CareerAdvice, pk=advice_id)
    # Check if the one requesting is the advice's owner.
    if request.user != advice_to_delete.author:
        return HttpResponse("You don't own this job!")
    # Is it a post request ? and checks if its by the owner himself.
    if request.method == "POST":
        # If so delete the job.
        advice_to_delete.delete()
        # Return to advices page
        return redirect('careeradvice:advice_list')
    context = {"advice_to_delete": advice_to_delete}
    return render(request, "delete_advice.html", context)


def edit_advice(request, advice_id):
    """ EDIT THE advice """
    # gets the object with the primary key from job
    advice_to_edit = CareerAdvice.objects.get(id=advice_id)
    # Does  is all data ?
    if request.method == "POST" and request.user == advice_to_edit.author:
        advice_form = CareerAdviceForm(data=request.POST, instance=advice_to_edit)
        #  The data are valid ?
        if advice_form.is_valid():
            advice_form.save(commit=False)
            # save tags
            # advice_form.save_m2m()
            # save form
            advice_form.save()
            # where the thread was updated ...
            return redirect(advice_to_edit.get_absolute_url())
    else:
        advice_form = CareerAdviceForm(instance=advice_to_edit)
    # Everything went well render send the user to the success page
    return render(request, "edit_advice.html", {"form": advice_form})
