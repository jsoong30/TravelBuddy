from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.views import LogoutView

def home(request):
    context = {'page_title': 'Welcome to Travel Buddy'}
    return render(request, 'home.html', context)

def itinerary(request):
    return HttpResponse("Itinerary page coming soon!")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the new user to the database
            return redirect('login')  # Redirect after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

