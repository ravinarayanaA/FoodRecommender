from newproject import find_items

from restaurants import find_rest

from django.shortcuts import render

from django.http import HttpResponse

from .forms import NameForm


def get_name(request, path):
	
	
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
    	list1 =[]
    	
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            for item in form.cleaned_data:
                if str(item) == "place":
                    place = form.cleaned_data[str(item)]
                else:
                    list1.append(form.cleaned_data[str(item)])
        	output = find_items(list1)
            places = find_rest(place)

            if str(type(output)) == "<type 'str'>":
        		return render(request, 'response.html', {'error': output})
            else:
                #return HttpResponse(place)
                #, 'restaurants': places
        	return render(request, 'response.html', {'form': output, 'restaurants': places})
    		#return HttpResponse(html)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form.as_ul})
    
    
def static_view(request, path):
    """
    serve pages directly from the templates directories.
    """
    if not path or path.endswith("/"):
        template_name = path + "homepage.html"
    else:
        template_name = path
    return render(request, template_name)


def about_view(request, path):
	return render(request, "about.html")

