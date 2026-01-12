from django.shortcuts import render, redirect
from .forms import ContactForm

def index(request):
    return render(request, 'batimentRenovation/home.html')

def dashboard(request):
    return render(request, 'batimentRenovation/dashboard.html')

def about(request):
    return render(request, 'batimentRenovation/about.html')

def contact(request):
    return render(request, 'batimentRenovation/contact.html')

def login(request):
    return render(request, 'batimentRenovation/login.html')

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