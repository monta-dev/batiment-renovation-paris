"""from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # 🔴 SANS ÇA → 0 CONTACT
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'accounts/contact.html', {'form': form})
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def contact(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        
        # Sauvegarder dans la base de données
        Contact.objects.create(
            nom=nom,
            email=email,
            message=message_text
        )
        
        # Afficher un message de succès
        messages.success(request, 'Votre message a été envoyé avec succès !')
        return redirect('contact')  # Redirige vers la même page
    
    return render(request, 'accounts/contact.html')


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Doit correspondre au 'name' dans le template register.html
        confirm_password = request.POST.get("confirm_password") 

        # 1. Vérification des mots de passe
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, "accounts/register.html")

        # 2. Vérification si l'utilisateur existe déjà
        if User.objects.filter(username=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "accounts/register.html")

        # 3. Création de l'utilisateur
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        messages.success(request, "Inscription réussie ! Connectez-vous.")
        return redirect("login") # Redirige vers la vue login

    # Afficher le template d'inscription pour un GET
    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Assurez-vous que 'home' existe dans urls.py
        else:
            messages.error(request, "Email ou mot de passe invalide")

    # Afficher le template de connexion pour un GET
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")