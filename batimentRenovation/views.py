from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
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

"""@cache_page(60 * 15)  # 15min cache
def stats_batiments(request):
    data = [
  {
    "name": "1er",
    "total": 41000,
    "renovated": 15400,
    "private_renovated": 10000,
    "social_renovated": 5400
  },
  {
    "name": "2e",
    "total": 49000,
    "renovated": 19500,
    "private_renovated": 12000,
    "social_renovated": 7500
  },
  {
    "name": "3e",
    "total": 26000,
    "renovated": 8000,
    "private_renovated": 5000,
    "social_renovated": 3000
  },
  {
    "name": "4e",
    "total": 49000,
    "renovated": 19500,
    "private_renovated": 12500,
    "social_renovated": 7000
  },
  {
    "name": "5e",
    "total": 42500,
    "renovated": 16000,
    "private_renovated": 10000,
    "social_renovated": 6000
  },
  {
    "name": "6e",
    "total": 45000,
    "renovated": 17500,
    "private_renovated": 11000,
    "social_renovated": 6500
  },
  {
    "name": "7e",
    "total": 45800,
    "renovated": 18000,
    "private_renovated": 11500,
    "social_renovated": 6500
  },
  {
    "name": "8e",
    "total": 37500,
    "renovated": 16800,
    "private_renovated": 10800,
    "social_renovated": 6000
  },
  {
    "name": "9e",
    "total": 25500,
    "renovated": 7800,
    "private_renovated": 5000,
    "social_renovated": 2800
  },
  {
    "name": "10e",
    "total": 43500,
    "renovated": 16800,
    "private_renovated": 10000,
    "social_renovated": 6800
  },
  {
    "name": "11e",
    "total": 22800,
    "renovated": 6500,
    "private_renovated": 4000,
    "social_renovated": 2500
  },
  {
    "name": "12e",
    "total": 28000,
    "renovated": 9000,
    "private_renovated": 6000,
    "social_renovated": 3000
  },
  {
    "name": "13e",
    "total": 40000,
    "renovated": 15000,
    "private_renovated": 9500,
    "social_renovated": 5500
  },
  {
    "name": "14e",
    "total": 22000,
    "renovated": 6000,
    "private_renovated": 3500,
    "social_renovated": 2500
  },
  {
    "name": "15e",
    "total": 46000,
    "renovated": 18000,
    "private_renovated": 11000,
    "social_renovated": 7000
  },
  {
    "name": "16e",
    "total": 20500,
    "renovated": 5500,
    "private_renovated": 3000,
    "social_renovated": 2500
  },
  {
    "name": "17e",
    "total": 49000,
    "renovated": 19500,
    "private_renovated": 12500,
    "social_renovated": 7000
  },
  {
    "name": "18e",
    "total": 23600,
    "renovated": 7000,
    "private_renovated": 4500,
    "social_renovated": 2500
  },
  {
    "name": "19e",
    "total": 43000,
    "renovated": 16500,
    "private_renovated": 10500,
    "social_renovated": 6000
  },
  {
    "name": "20e",
    "total": 33400,
    "renovated": 11500,
    "private_renovated": 7500,
    "social_renovated": 4000
  }
]
    return JsonResponse(data)

@cache_page(60 * 15)
def stats_dpe(request):
    data = [
  { "class": "A", "count": 1500, "color": "#10B981" },
  { "class": "B", "count": 3200, "color": "#34D399" },
  { "class": "C", "count": 5600, "color": "#A7F3D0" },
  { "class": "D", "count": 8900, "color": "#FCD34D" },
  { "class": "E", "count": 7500, "color": "#F59E0B" },
  { "class": "F", "count": 4200, "color": "#EF4444" },
  { "class": "G", "count": 2100, "color": "#7F1D1D" }
]
    return JsonResponse(data)

@cache_page(60 * 15)
def stats_types(request):
    data = [
        { "type": "Isolation Thermique", "count": 12500, "percentage": 35 },
        { "type": "Chauffage / EnR", "count": 8900, "percentage": 25 },
        { "type": "Ventilation", "count": 5400, "percentage": 15 },
        { "type": "Menuiseries", "count": 7100, "percentage": 20 },
        { "type": "Audit Énergétique", "count": 1800, "percentage": 5 }
    ]
    return JsonResponse(data)"""