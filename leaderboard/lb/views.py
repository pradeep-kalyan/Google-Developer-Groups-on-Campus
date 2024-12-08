from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from .models import Leaderboard
from datetime import datetime
import random

# Create your views here.
@login_required
def lbb(request):
    quotes = [
        "Why do programmers prefer dark mode? Because the light attracts bugs.",
        "There are only 10 kinds of people in the world: those who understand binary and those who don’t.",
        "Programming is like writing a book... except if you miss out a single comma on page 126 the whole thing makes no sense.",
        "A good programmer is someone who always looks both ways before crossing a one-way street.",
        "I don't always test my code, but when I do, I do it in production.",
        "I have a joke on programming, but it’s still in development.",
        "Debugging: Being the detective in a criminal movie where you are also the murderer.",
        "The best thing about a Boolean is even if you are wrong, you are only off by a bit.",
        "Programmer: A machine that turns coffee into code.",
        "I wish debugging was as easy as deleting my browser history.",
        "Why do Java developers wear glasses? Because they don’t see sharp.",
        "If at first you don’t succeed, call it version 1.0.",
        "Code never lies, comments do.",
        "Programming is the art of telling another human being what one wants the computer to do.",
        "To iterate is human, to recurse divine.",
        "The problem with troubleshooting is that the trouble shoots back.",
        "There are two hard things in computer science: cache invalidation, naming things, and off-by-one errors.",
        "I’m not a magician, but I can make your bugs disappear.",
        "Real programmers count from 0.",
        "Why was the JavaScript developer sad? Because he didn’t 'null' his feelings.",
        "Don't worry if it doesn't work right. If everything did, you'd be out of a job.",
        "A programmer’s wife tells him, ‘While you’re at it, can you fix the sink?’ The programmer replies, ‘I’ll first try re-booting it.’",
        "The best way to predict the future is to invent it... and then debug it.",
        "One man’s bug is another man’s feature.",
        "Every time I write a program, I make the same mistake: I write a program.",
        "Computers are like air conditioners – they stop working when you open windows.",
        "I’m not sure what the problem is, but I’ll try turning it off and on again.",
        "Why don’t programmers like nature? It has too many bugs.",
        "Programmers are tools for building tools.",
        "Software development is like a relationship – when it works, it’s amazing, but when it goes wrong, you’re just debugging for hours.",
        "A code is like a joke: if you have to explain it, it’s not that good.",
        "Java is to JavaScript what car is to carpet.",
        "There's no place like 127.0.0.1.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "The code that you write today will be written by someone else tomorrow and will look like it was written by a person from Mars.",
        "Programming is the only profession where you get paid for making mistakes and then fixing them.",
        "Without requirements or design, programming is the art of adding bugs to an empty text file.",
        "Why do programmers hate nature? It’s full of bugs.",
    ]
    quotes = random.choice(quotes)
    leaderboard = Leaderboard.objects.all().order_by('-points', '-streak')
    return render(request, "leaderboard.html", {"quotes": quotes})
