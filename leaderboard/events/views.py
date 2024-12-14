# events/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from events.models import Event
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required


# View to display event details
def events(request, event_id):
    # Get the event by event_id
    event = get_object_or_404(Event, event_id=event_id)

    # Render the event details template
    return render(request, "event_detail.html", {"event": event})


# View to add participant by em


# View to add participant b
