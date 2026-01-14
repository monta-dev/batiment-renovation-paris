from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, LoginForm, SignupForm

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

@require_http_methods(["GET", "POST"])
def login(request):
    print("🔍 VUE login appelée - Method:", request.method)
    mode = request.GET.get('mode', 'login')
    print(f"🔍 Mode détecté: {mode}")
    
    if request.method == "POST":
        print("📤 POST détecté")
        
        if mode == 'register':
            print("📝 Traitement INSCRIPTION")
            form = SignupForm(request.POST)
            if form.is_valid():
                print("✅ Form Signup valide")
                user = form.save()
                print(f"✅ User créé: {user} (ID: {user.id}, email: {user.email})")
                
                # Vérif user actif
                if user and user.is_active:
                    auth_login(request, user)
                    print("✅ Auto-login OK")
                    messages.success(request, f"Compte créé ! Bienvenue {user.email}")
                    return redirect('dashboard')
                else:
                    print(f"❌ User inactif: {user.is_active if user else 'None'}")
                    messages.error(request, "Erreur création compte.")
            else:
                print("❌ Form Signup invalide:", form.errors)
        
        else:  # login
            print("🔑 Traitement CONNEXION")
            form = LoginForm(request.POST)
            if form.is_valid():
                print("✅ Form Login valide")
                print(f"🔍 Tentative login: {form.cleaned_data['email']}")
                
                user = authenticate(
                    request=request,
                    username=form.cleaned_data["email"],  # username=email
                    password=form.cleaned_data["password"],
                )
                print(f"🔍 Authenticate retourne: {user}")
                
                if user and user.is_active:
                    auth_login(request, user)
                    print("✅ Login OK")
                    messages.success(request, f'Bonjour, {user.email} !')
                    return redirect('dashboard')
                else:
                    print("❌ Login échoué - user inactif ou None")
                    messages.error(request, "Identifiants invalides.")
            else:
                print("❌ Form Login invalide:", form.errors)
    
    # Affichage forms
    login_form = LoginForm()
    signup_form = SignupForm()
    
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
        'mode': mode,
    }
    print("📄 Render template avec context")
    return render(request, 'batimentRenovation/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('login')

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