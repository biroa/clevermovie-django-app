from django.shortcuts import render, redirect
from django.contrib import messages
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
    #print(str(request.GET.get('query','')))
    user_query = str(request.GET.get('query',''));
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER( {Name} ) )")
    # contex dictionary
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):

    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{ 'url': request.POST.get('url')}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }
        AT.insert(data)

    return redirect('/')

