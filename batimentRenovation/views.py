from django.shortcuts import render


def index(request):
    return render(request, 'batimentRenovation/home.html')
    
def auth(request):
    return render(request, 'batimentRenovation/login.html')

def accueil(request):
    return render(request, 'batimentRenovation/dashboard.html')

def contact(request):
    return render(request, 'batimentRenovation/contact.html')

def admin(request):
    return render(request, 'batimentRenovation/admin_page.html')

def about(request):
    return render(request, 'batimentRenovation/about.html')

def erreur(request):
    return render(request, 'batimentRenovation/404.html')