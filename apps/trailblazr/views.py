from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Trail
from ..login_registration.models import User
import requests
from django.conf import settings

# displays landing page
def index(request):
    return render(request, 'index.html')

# displays user dashboard, including list of trails saved by current user if there are any
def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    try:
        trails = Trail.objects.filter(user=user).order_by('created_at')
    except Trail.DoesNotExist:
        trails = None
    context = {
        'trails': trails
    }
    return render(request, 'dashboard.html', context)

# displays search page
def search_bar(request):
    return render(request, 'results.html')

# makes api call to Google Maps to retrieve latitude and longitude coordinates
# makes api call to Hiking Project using lat and lon to retrieve list of trails near queried location
def search(request):
    if 'search' in request.GET:
        address = request.GET['search']
        address_list = address.split(' ');
        address = ''
        for i in range(len(address_list)):
            address = address + address_list[i] + "+"
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, settings.GOOGLE_MAPS_API_KEY)) 
        location = response.json()
        lat = location['results'][0]['geometry']['location']['lat']
        lon = location['results'][0]['geometry']['location']['lng']
        response = requests.get('https://www.hikingproject.com/data/get-trails?lat={}&lon={}&key={}'.format(lat, lon, settings.HIKING_PROJECT_API_KEY))
        trails = response.json()
        results = trails['trails']
        user_trails = Trail.objects.filter(user=request.session['user_id'])
        saved_trails = []
        for user_trail in user_trails:
            saved_trails.append(user_trail.trail_id)
        context = {
            'results': results,
            'address': address,
            'saved_trails': saved_trails
        }
        return render(request, 'results.html', context)
    else:
        return redirect('trailblazr:dashboard')

# saves selected trail into user's saved trails list
def add_trail(request, id):
    response = requests.get('https://www.hikingproject.com/data/get-trails-by-id?ids={}&key={}'.format(id, settings.HIKING_PROJECT_API_KEY))
    trail = response.json()
    trail_id = trail['trails'][0]['id']
    trail_name = trail['trails'][0]['name']
    trail_location = trail['trails'][0]['location']
    trail_lat = trail['trails'][0]['latitude']
    trail_lon = trail['trails'][0]['longitude']
    trail_length = trail['trails'][0]['length']
    trail_ascent = trail['trails'][0]['ascent']
    trail_descent = trail['trails'][0]['descent']
    if trail['trails'][0]['difficulty'] == 'green':
        trail_difficulty = 'Beginner'
    elif trail['trails'][0]['difficulty'] == 'blue':
        trail_difficulty = 'Intermediate'
    elif trail['trails'][0]['difficulty'] == 'black':
        trail_difficulty = 'Advanced'
    Trail.objects.add_trail(request.session['user_id'], trail_id, trail_name, trail_location, trail_lat, trail_lon, trail_length, trail_ascent, trail_descent, trail_difficulty)
    return redirect('trailblazr:search')

# deletes selected trail from user's saved trails list
def del_trail(request, id):
    Trail.objects.get(id=id).delete()
    return redirect('trailblazr:dashboard')

# makes api call to Hiking Project to gather additional info about specific trail
# makes api call to Google Maps to embed map of trail location
def show_trail(request, id):
    trail = Trail.objects.get(id=id)
    address = trail.name
    address_list = address.split(' ')
    address = ''
    for i in range(len(address_list)):
        address = address + address_list[i] + "+"
    response = requests.get('https://www.hikingproject.com/data/get-conditions?ids={}&key={}'.format(trail.trail_id, settings.HIKING_PROJECT_API_KEY))
    conditions = response.json()
    context = {
        'trail': trail,
        'address': address,
        'conditions': conditions['0'],
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY 
    }
    return render(request, 'trail.html', context)