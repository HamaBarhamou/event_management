from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, "events/event_list.html", {"events": events})


@login_required
@user_passes_test(is_organizer)
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


@login_required
@user_passes_test(is_organizer)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form})


@login_required
@user_passes_test(is_organizer)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect("event_list")
    return render(request, "events/event_confirm_delete.html", {"event": event})
