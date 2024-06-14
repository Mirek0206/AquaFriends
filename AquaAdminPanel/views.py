from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Model
from django.forms import modelform_factory
from django.db.models import ProtectedError, OneToOneField

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

        if pk == "new":
            ModelForm = get_model_form(model)
            if request.method == "POST":
                form = ModelForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Nowy obiekt został utworzony')
                    return redirect("admin_panel_model", module_name=module_name)
            else:
                form = ModelForm()
            context["form"] = form
        elif pk:
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

staff_member_required(login_url="admin_login")
def delete_instance(request, module_name: str, pk: str):
    model = AquaAdminPanel().registry.get(module_name)
    if model is None:
        messages.error(request, 'Taki model nie istnieje')
        return redirect("admin_panel")

    instance = get_object_or_404(model, pk=pk)
    context = {
        "page": "delete",
        "modules": [key for key in AquaAdminPanel().registry.keys()],
        "model": model.__name__,
        "instance": instance,
        "related_objects": get_related_objects(instance)
    }

    if request.method == "POST":
        try:
            instance.delete()
            messages.success(request, f'{model.__name__} został usunięty.')
            return redirect("admin_panel_model", module_name=module_name)
        except ProtectedError:
            messages.error(request, f'{model.__name__} nie może być usunięty, ponieważ jest powiązany z innymi obiektami.')

    return render(request, "AquaAdminPanel/panel.htm", context)

def get_related_objects(instance):
    related_objects = []
    for rel in instance._meta.get_fields():
        if rel.one_to_many or rel.one_to_one:
            if isinstance(rel, OneToOneField):
                accessor_name = rel.name
            else:
                accessor_name = rel.get_accessor_name()
            related_manager = getattr(instance, accessor_name, None)
            if related_manager:
                if hasattr(related_manager, 'all'):
                    related_objects.extend(related_manager.all())
                else:
                    related_objects.append(related_manager)
        elif rel.many_to_many:
            related_manager = getattr(instance, rel.name, None)
            if related_manager:
                related_objects.extend(related_manager.all())
    return related_objects