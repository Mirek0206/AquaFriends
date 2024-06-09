from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AquariumForm
from .models import Aquarium


@login_required(login_url='login')
def create_aquarium(request):
    if request.method == 'POST':
        form = AquariumForm(request.user, request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            form.save_m2m()  # To save the many-to-many relationship
            return redirect('account')  # Załóżmy, że masz widok listy akwariów
    else:
        form = AquariumForm(user=request.user)
    return render(request, 'AquaMaker/create_aquarium.html', {'form': form})

@login_required(login_url="login")
def aquarium_history(request, pk: int):
    aquarium = Aquarium.objects.get(id=pk)
    change = aquarium.history.first()
    history: list[str] = []

    while change.prev_record is not None:
        new_record = change
        old_record = change.prev_record

        delta = new_record.diff_against(old_record, foreign_keys_are_objs=True)
        history.extend(
            [
                f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - '{event.field}' zmieniono z '{event.old}' na '{event.new}'"
                for event in delta.changes
            ],
        )
        change = change.prev_record

    return render(
        request,
        "AquaMaker/aquarium_history.html",
        {
            "aquarium": aquarium,
            "history": history,
        },
    )
