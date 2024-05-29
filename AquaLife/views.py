from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AquariumForm, FishForm
from .models import Aquarium, Fish

@login_required(login_url='login')
def edit_aquarium(request, pk):
    aquarium = get_object_or_404(Aquarium, pk=pk, user=request.user)
    
    if request.method == 'POST':
        aquarium_form = AquariumForm(request.user, request.POST, instance=aquarium)
        fish_form = FishForm(request.POST)
        
        if 'save_aquarium' in request.POST:
            if aquarium_form.is_valid():
                aquarium_form.save()
                messages.success(request, 'Zapisano zmiany!')
                return redirect('AquaLife:edit_aquarium', pk=aquarium.pk)
        
        if 'add_fish' in request.POST:
            if fish_form.is_valid():
                fish = fish_form.save(commit=False)
                fish.aquarium = aquarium
                fish.save()
                messages.success(request, 'Pomyślnie dodano rybkę!')
                return redirect('AquaLife:edit_aquarium', pk=aquarium.pk)
    
    else:
        aquarium_form = AquariumForm(user=request.user, instance=aquarium)
        fish_form = FishForm()
    
    fishes = Fish.objects.filter(aquarium=aquarium)
    
    context = {
        'aquarium_form': aquarium_form,
        'fish_form': fish_form,
        'fishes': fishes,
        'aquarium': aquarium
    }
    
    return render(request, 'AquaLife/edit_aquarium.html', context)

@login_required(login_url='login')
def delete_fish(request, pk):
    fish = get_object_or_404(Fish, pk=pk, aquarium__user=request.user)
    aquarium_pk = fish.aquarium.pk
    fish.delete()
    messages.success(request, 'Pomyślnie usunięto rybkę!')
    return redirect('AquaLife:edit_aquarium', pk=aquarium_pk)

@login_required(login_url='login')
def delete_aquarium(request, pk):
    aquarium = get_object_or_404(Aquarium, pk=pk, user=request.user)
    aquarium.delete()
    messages.success(request, 'Pomyślnie usunięto rybkę!')
    return redirect('account')
