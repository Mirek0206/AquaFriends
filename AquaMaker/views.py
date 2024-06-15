from __future__ import annotations

from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from AquaLife.models import HistoricalFish

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

_HISTORY_LABELS: dict[str, str] = {
    "name": "Nazwa akwarium",
    "x": "Długość",
    "y": "Wysokość",
    "z": "Głębokość",
    "light": "Oświetlenie",
    "filters": "Listę filtrów",
    "pump": "Pompa",
    "heater": "Grzałka",
}


@login_required(login_url="login")
def aquarium_history(request, pk: int):
    aquarium = Aquarium.objects.get(id=pk)
    history: list[str] = []

    change = aquarium.history.first()
    while change.prev_record is not None:
        new_record = change
        old_record = change.prev_record

        delta = new_record.diff_against(old_record, foreign_keys_are_objs=True)
        history.extend(
            [
                f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - {_HISTORY_LABELS.get(event.field, event.field)} zmieniono z '{event.old}' na '{event.new}'"
                for event in delta.changes
            ],
        )
        change = change.prev_record

    # Get the historical records for all fishes associated with the aquarium
    fish_history = []
    for fish_history_record in HistoricalFish.objects.filter(aquarium_id=pk).order_by(
        "-history_date",
    ):
        if fish_history_record.history_type == "+":
            fish_history.append(
                f"{fish_history_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - Dodano rybę '{fish_history_record.name}' ({fish_history_record.species})",
            )
        elif fish_history_record.history_type == "-":
            fish_history.append(
                f"{fish_history_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - Usunięto rybę '{fish_history_record.name}' ({fish_history_record.species})",
            )

    # Combine and sort the history
    combined_history = sorted(
        chain(history, fish_history),
        key=lambda x: x.split(" - ")[0],
        reverse=True,
    )

    combined_history.append(
        f"{aquarium.history.last().history_date.strftime('%Y-%m-%d %H:%M:%S')} - Dodano akwarium",
    )

    return render(
        request,
        "AquaMaker/aquarium_history.html",
        {
            "aquarium": aquarium,
            "history": combined_history,
        },
    )
