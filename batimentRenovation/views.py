from django.shortcuts import render


def index(request):
    return render(request, 'batimentRenovation/home.html')
    
def login(request):
   return render(request, 'batimentRenovation/login.html')

def Accueil(request):
    return render(request, 'batimentRenovation/dashboard.html')

def dash_bat(request):
    return render(request, 'batimentRenovation/dashboard_batiment.html')

def dash_dpe(request):
    return render(request, 'batimentRenovation/dashboard_dpe.html')

def dash_types(request):
    return render(request, 'batimentRenovation/dashboard_types.html')

def contact(request):
    return render(request, 'batimentRenovation/contact.html')

def admin1(request):
    return render(request, 'batimentRenovation/admin_page.html')

def about(request):
    return render(request, 'batimentRenovation/about.html')

def erreur(request):
    return render(request, 'batimentRenovation/404.html')