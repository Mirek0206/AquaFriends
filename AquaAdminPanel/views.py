from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Model

from .admin import AquaAdminPanel

# Create your views here.

def admin_login(request):

    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception:
            messages.error(request, 'Nie istnieje użytkownik o podanej nazwie.')
            return redirect("admin_login")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:
                messages.error(request, 'To konto nie nalezy do aministratora.')
                return redirect("admin_login")
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else "admin_panel")
        else:
            messages.error(request, 'Nazwa użytkownika lub hasło jest niepoprawne.')
            return redirect("admin_login")

    return render(request, "AquaAdminPanel/login.htm")


@staff_member_required(login_url="admin_login")
def admin_panel(request, module_name: str = None, pk: str = None):
    context: dict = {
        "modules": [key for key in AquaAdminPanel().registry.keys()]
    }

    if module_name:
        model: Model | None = AquaAdminPanel().registry.get(module_name)
        if model is None:
            messages.error(request, 'Taki model nie istnieje')
            return redirect("admin_panel")

        context["model"] = model.__name__
        context["instances"] = model.objects.all()

    if pk:
        ...

    return render(request, "AquaAdminPanel/panel.htm", context=context)
