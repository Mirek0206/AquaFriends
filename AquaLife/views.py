from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
                return redirect('account')
        
        if 'add_fish' in request.POST:
            if fish_form.is_valid():
                fish = fish_form.save(commit=False)
                fish.aquarium = aquarium
                fish.save()
                return redirect('edit_aquarium', pk=aquarium.pk)
    
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
