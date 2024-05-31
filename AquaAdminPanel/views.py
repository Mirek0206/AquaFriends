from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Model
from django import forms
from django.forms import modelform_factory

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

def get_model_form(model):
    FormClass = modelform_factory(model, fields="__all__")

    class ModelFormWithClass(FormClass):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'input'})

    return ModelFormWithClass

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

        if pk:
            instance = get_object_or_404(model, pk=pk)
            ModelForm = get_model_form(model)
            if request.method == "POST":
                form = ModelForm(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Obiekt został zaktualizowany')
                    return redirect("admin_panel_model", module_name=module_name)
            else:
                form = ModelForm(instance=instance)
            context["form"] = form
            context["instance"] = instance
        else:
            context["instances"] = model.objects.all()

    return render(request, "AquaAdminPanel/panel.htm", context=context)
