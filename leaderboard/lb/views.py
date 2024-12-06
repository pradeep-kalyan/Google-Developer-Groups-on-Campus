from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def lbb(request):
    return render(request, "leaderboard.html")

@login_required
def events(request):
    return render(request, "event/events.html")