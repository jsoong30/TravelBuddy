from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    context = {'page_title': 'Welcome to Travel Buddy'}
    return render(request, 'home.html', context)

def itinerary(request):
    return HttpResponse("Itinerary page coming soon!")


