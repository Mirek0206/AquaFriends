from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AquariumForm

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
