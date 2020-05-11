from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User
import types
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# registers user infor if all info is valid
def register(request):
    if request.method != 'POST':
        return redirect(reverse('trailblazr:index'))
    else: 
        user = User.objects.register(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.error(request, error)
            return redirect(reverse('trailblazr:index'))
        else:
            request.session['user_id'] = user.id 
            return redirect(reverse('trailblazr:dashboard'))

# logs in user if user info is valid and saves info into a session
def login(request):
    if request.method != 'POST':
        return redirect(reverse('gym_rat:index'))
    else:
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid email or password!")
            return redirect(reverse('trailblazr:index'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect(reverse('trailblazr:dashboard'))

# logs out a user and deletes session containing user info
def logout(request):
    if 'workout' in request.session:
        del request.session['workout']
    User.objects.logout(request.session['user_id'])
    return redirect(reverse('trailblazr:index'))