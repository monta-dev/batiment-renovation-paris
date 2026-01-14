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
from django.contrib.auth import authenticate

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





'''def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')
    
    return render(request, 'accounts/login.html')'''


"""def logout_view(request):
    logout(request)
    return redirect('/')"""


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect('login')

    return render(request, 'accounts/login.html')