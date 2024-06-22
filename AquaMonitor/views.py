from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from AquaMaker.models import Aquarium, AquariumParametrs
from AquaMonitor.forms import ExceptionalSituationForm, WaterParameterForm
from .models import WaterParameter, ExceptionalSituation
from django.utils import timezone

@login_required(login_url='login')
def user_aquariums_and_parameters(request, aquarium_id=None):
    user = request.user
    aquariums = Aquarium.objects.filter(user=user)
    selected_aquarium = None
    parameters_history = None
    exceptional_situations_history = None
    parameter_hints = []

    if aquarium_id:
        selected_aquarium = get_object_or_404(Aquarium, id=aquarium_id, user=request.user)
        parameters_history = WaterParameter.objects.filter(aquarium=selected_aquarium).order_by('-date')
        exceptional_situations_history = ExceptionalSituation.objects.filter(aquarium=selected_aquarium).order_by('-date')

        # Get the latest parameters
        if parameters_history.exists():
            latest_parameters = parameters_history.first()
            # Get the parameter norms
            parameter_norms = AquariumParametrs.objects.first()

            # Check NO2
            if latest_parameters.no2 < parameter_norms.minimum_no2:
                parameter_hints.append(parameter_norms.too_low_no2_hint)
            elif latest_parameters.no2 > parameter_norms.maximum_no2:
                parameter_hints.append(parameter_norms.too_high_no2_hint)

            # Check NO3
            if latest_parameters.no3 < parameter_norms.minimum_no3:
                parameter_hints.append(parameter_norms.too_low_no3_hint)
            elif latest_parameters.no3 > parameter_norms.maximum_no3:
                parameter_hints.append(parameter_norms.too_high_no3_hint)

            # Check GH
            if latest_parameters.gh < parameter_norms.minimum_gh:
                parameter_hints.append(parameter_norms.too_low_gh_hint)
            elif latest_parameters.gh > parameter_norms.maximum_gh:
                parameter_hints.append(parameter_norms.too_high_gh_hint)

            # Check KH
            if latest_parameters.kh < parameter_norms.minimum_kh:
                parameter_hints.append(parameter_norms.too_low_kh_hint)
            elif latest_parameters.kh > parameter_norms.maximum_kh:
                parameter_hints.append(parameter_norms.too_high_kh_hint)

            # Check pH
            if latest_parameters.ph < parameter_norms.minimum_ph:
                parameter_hints.append(parameter_norms.too_low_ph_hint)
            elif latest_parameters.ph > parameter_norms.maximum_ph:
                parameter_hints.append(parameter_norms.too_high_ph_hint)

    context = {
        'aquariums': aquariums,
        'selected_aquarium': selected_aquarium,
        'parameters_history': parameters_history,
        'exceptional_situations_history': exceptional_situations_history,
        'parameter_hints': parameter_hints,
    }
    return render(request, 'AquaMonitor/user_aquariums_and_parameters.html', context)

@login_required(login_url='login')
def add_water_parameter(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id, user=request.user)
    page = "parameters"
    
    if request.method == 'POST':
        form = WaterParameterForm(request.POST)
        if form.is_valid():
            water_parameter = form.save(commit=False)
            water_parameter.aquarium = aquarium
            water_parameter.date = timezone.now()  # Ustawienie bieżącej daty i czasu
            water_parameter.save()
            messages.success(request, 'Pomyślnie zapisano dane!')
            return redirect('AquaMonitor:user_aquariums_and_parameters', aquarium_id=aquarium.id)
    else:
        form = WaterParameterForm()
    
    context = {
        'form': form,
        'aquarium': aquarium,
        'page': page
    }
    
    return render(request, 'AquaMonitor/add_water_parameter.html', context)

@login_required(login_url='login')
def add_exceptional_situation(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id, user=request.user)
    page = "exceptional_situation"

    if request.method == 'POST':
        form = ExceptionalSituationForm(request.POST)
        if form.is_valid():
            exceptional_situation = form.save(commit=False)
            exceptional_situation.aquarium = aquarium
            exceptional_situation.save()
            messages.success(request, 'Pomyślnie dodano sytuację wyjątkową!')
            return redirect('AquaMonitor:user_aquariums_and_parameters', aquarium_id=aquarium.id)
    else:
        form = ExceptionalSituationForm()

    context = {
        'form': form,
        'aquarium': aquarium,
        'page': page
    }

    return render(request, 'AquaMonitor/add_water_parameter.html', context)