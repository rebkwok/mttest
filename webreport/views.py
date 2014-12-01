
from django.shortcuts import render
from webreport.forms import WebreportForm
from webreport.utils import process_url


def get_url(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WebreportForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            url = form.cleaned_data['url']
            #import ipdb; ipdb.set_trace()
            context = process_url(url)
            return render(request, 'webreport/report.xhtml', context)

    # if a GET (or any other method) create a blank form
    else:
        form = WebreportForm()

    return render(request, 'webreport/home.html', {'form': form})

