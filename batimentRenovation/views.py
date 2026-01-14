from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, LoginForm

def index(request):
    return render(request, 'batimentRenovation/home.html')

@login_required
def dashboard(request):
    return render(request, 'batimentRenovation/dashboard.html')

@login_required
def dashboard_batiment(request):
    return render(request, 'batimentRenovation/dashboard_batiment.html')

@login_required
def dashboard_dpe(request):
    return render(request, 'batimentRenovation/dashboard_dpe.html')

@login_required
def dashboard_types(request):
    return render(request, 'batimentRenovation/dashboard_types.html')

def about(request):
    return render(request, 'batimentRenovation/about.html')

def contact(request):
    return render(request, 'batimentRenovation/contact.html')

def login(request):
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                message = "Identifiants invalides."
    else:
        form = LoginForm()

    return render(
        request,
        "batimentRenovation/login.html",
        {"form": form, "message": message},
    )

def admin_page(request):
    return render(request, 'batimentRenovation/admin_page.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # 1) on sauve le message dans la base
            instance = form.save()
            # 2) on envoie l'email
            form.send_email(instance)
            # 3) redirection (évite le resoumission du formulaire)
            return redirect("contact")  # ou une page 'merci'
    else:
        form = ContactForm()

    return render(request, "batimentRenovation/contact.html", {"form": form})