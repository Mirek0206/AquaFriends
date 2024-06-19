from __future__ import annotations
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from itertools import chain

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
            messages.success(request, 'Pomyślnie utworzono akwarium!')
            return redirect('account')
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

def format_filter_list(filters):
    return ", ".join([str(f.filter) for f in filters])


@login_required(login_url="login")
def aquarium_history(request, pk: int):
    try:
        aquarium = Aquarium.objects.get(id=pk)
    except Aquarium.DoesNotExist:
        messages.error(request, "Historia dla tego akwarium nie istnieje !")
        return redirect("account")

    if aquarium.user != request.user:
        messages.error(request, "To akwarium nie naley do Ciebie !")
        return redirect("account")

    history: list[str] = []

    change = aquarium.history.first()
    while change.prev_record is not None:
        new_record = change
        old_record = change.prev_record

        delta = new_record.diff_against(old_record, foreign_keys_are_objs=True)
        for event in delta.changes:
            if event.field == "filters":
                old_filters = format_filter_list(old_record.filters.all())
                new_filters = format_filter_list(new_record.filters.all())
                history.append(
                    f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - { _HISTORY_LABELS.get(event.field, event.field)} zmieniono z '{old_filters}' na '{new_filters}'"
                )
            else:
                history.append(
                    f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - {_HISTORY_LABELS.get(event.field, event.field)} zmieniono z '{event.old}' na '{event.new}'"
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
