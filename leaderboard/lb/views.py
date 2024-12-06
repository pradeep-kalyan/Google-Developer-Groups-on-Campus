from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def lbb(request):
    return render(request, "lb/leaderboard.html")
