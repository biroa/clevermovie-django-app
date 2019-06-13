from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
# Importing Google spreadsheets aka Airtable DB on steroids ...
from airtable import Airtable
# Importing os to handle environment variables
import os
from pprint import pprint

# Airtable connection to database
AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query',''));
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER( {Name} ) )")
    # contex dictionary
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    # Picture is a list of dictionary
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{ 'url': request.POST.get('url') or 'https://www.quantabiodesign.com/wp-content/uploads/No-Photo-Available-768x960.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }
        try:
            response = AT.insert(data)
            # --== Notify on Create ==--
            # Dictionaries have a function get ... we can retrive information from
            # the dict without braking the code ... So if the key does not exist in
            # the dict it returns null without it it would break
            # {data in format func will be placed here}
            messages.success(request,'New Movie Added : {}'.format(response['fields'].get('Name')))
        except Exception as e:
            # If something went wrong show me an error without crashing the app
            messages.warning(request, 'Error while trying to create a new movie: {}' . format(e))

    return redirect('/')

def edit(request, movie_id):
    # Picture is a list of dictionary
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://www.quantabiodesign.com/wp-content/uploads/No-Photo-Available-768x960.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }

        # Error Handling ....

        try: # try this
            response = AT.update(movie_id, data);
            # Notify on Edit / Update
            messages.warning(request,'The edited movie is {}'.format(response['fields'].get('Name')))
        except Exception as e:
            # If something went wrong show me an error without crashing the app
            messages.warning(request, 'Error while trying to edit a movie: {}' . format(e))

    return redirect('/')

#app.com/delete/rec0wPWwWIm0FpaJw
def delete(request, movie_id):
    try:
        # Notify on Delete
        messages.error(request,'Deleted Movie : {}'.format(AT.get(movie_id)['fields'].get('Name')), extra_tags='danger')
        AT.delete(movie_id)
    except Exception as e:
        # If something went wrong show me an error without crashing the app
        messages.warning(request, 'Error while trying to delete a movie: {}' . format(e))

    return redirect('/')
