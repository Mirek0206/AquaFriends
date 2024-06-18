from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from AquaMaker.models import Aquarium
from AquaMonitor.forms import WaterParameterForm
from .models import WaterParameter
from django.utils import timezone

@login_required(login_url='login')
def user_aquariums_and_parameters(request, aquarium_id=None):
    user = request.user
    aquariums = Aquarium.objects.filter(user=user)
    selected_aquarium = None
    parameters_history = None

    if aquarium_id:
        selected_aquarium = get_object_or_404(Aquarium, id=aquarium_id, user=request.user)
        parameters_history = WaterParameter.objects.filter(aquarium=selected_aquarium).order_by('-date')

    context = {
        'aquariums': aquariums,
        'selected_aquarium': selected_aquarium,
        'parameters_history': parameters_history,
    }
    return render(request, 'AquaMonitor/user_aquariums_and_parameters.html', context)

@login_required(login_url='login')
def add_water_parameter(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, id=aquarium_id, user=request.user)
    
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
        'aquarium': aquarium
    }
    
    return render(request, 'AquaMonitor/add_water_parameter.html', context)
