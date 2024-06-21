from __future__ import annotations
from datetime import datetime
from itertools import chain
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from AquaLife.models import HistoricalFish
from AquaMonitor.models import ExceptionalSituation

from .forms import AquariumForm, HistoryForm
from .models import Aquarium, Heater, Light, Pump


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

def filter_history_by_date(history, start_date_str, end_date_str):
    start_date = datetime.strptime(str(start_date_str), "%Y-%m-%d")
    end_date = datetime.strptime(str(end_date_str), "%Y-%m-%d").replace(
        hour=23,
        minute=59,
        second=59,
    )

    filtered_history = []
    for entry in history:
        date_str = entry.split(" - ")[0]
        entry_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        if start_date <= entry_date <= end_date:
            filtered_history.append(entry)

    return filtered_history


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

    form = HistoryForm()
    history: list[str] = []

    change = aquarium.history.first()
    while change.prev_record is not None:
        new_record = change
        old_record = change.prev_record

        delta = new_record.diff_against(old_record, foreign_keys_are_objs=True)
        for event in delta.changes:
            if event.field == "filters":
                old_filters = format_filter_list(old_record.filters.all())
                old_filters = old_filters if old_filters else "BRAK"
                new_filters = format_filter_list(new_record.filters.all())
                history.append(
                    f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - { _HISTORY_LABELS.get(event.field, event.field)} zmieniono z '{old_filters}' na '{new_filters}'",
                )
            else:
                history.append(
                    f"{new_record.history_date.strftime('%Y-%m-%d %H:%M:%S')} - {_HISTORY_LABELS.get(event.field, event.field)} zmieniono z '{event.old}' na '{event.new}'",
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

    # Get ExceptionalSituations
    es_history = [
        f"{situation.date.strftime('%Y-%m-%d %H:%M:%S')} - {situation.situation_type}"
        for situation in ExceptionalSituation.objects.filter(aquarium=aquarium)
    ]

    # Combine and sort the history
    combined_history = sorted(
        chain(history, fish_history, es_history),
        key=lambda x: x.split(" - ")[0],
        reverse=True,
    )

    combined_history.append(
        f"{aquarium.history.last().history_date.strftime('%Y-%m-%d %H:%M:%S')} - Dodano akwarium",
    )

    if request.method == "POST":
        form = HistoryForm(request.POST)
        if form.is_valid():
            combined_history = filter_history_by_date(
                combined_history,
                form.cleaned_data["start_date"],
                form.cleaned_data["end_date"],
            )

    return render(
        request,
        "AquaMaker/aquarium_history.html",
        {
            "aquariums": Aquarium.objects.filter(user=request.user),
            "selected_aquarium": aquarium,
            "history": {
                datetime.strptime(  # noqa: DTZ007
                    item.split(" - ")[0],
                    "%Y-%m-%d %H:%M:%S",
                ): " ".join(
                    item.split(
                        " - ",
                        1,
                    )[1:],
                )
                for item in combined_history
            },
            "form": form,
        },
    )

@login_required(login_url="login")
def get_min_power_devices(request):
    x = float(request.GET.get('x', 0))
    y = float(request.GET.get('y', 0))
    z = float(request.GET.get('z', 0))
    volume = x * y * z / 1000  # Oblicz objętość w litrach

    min_pump = Pump.objects.filter(min_volume__lte=volume, max_volume__gte=volume).order_by('power').first()
    min_heater = Heater.objects.filter(min_volume__lte=volume, max_volume__gte=volume).order_by('power').first()
    min_light = Light.objects.filter(min_volume__lte=volume, max_volume__gte=volume).order_by('power').first()

    response_data = {
        'min_pump_power': f'{min_pump.power} W' if min_pump else 'Brak odpowiednich pomp',
        'min_heater_power': f'{min_heater.power} W' if min_heater else 'Brak odpowiednich grzałek',
        'min_light_power': f'{min_light.power} W' if min_light else 'Brak odpowiednich świateł',
    }

    return JsonResponse(response_data)