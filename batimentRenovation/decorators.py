from django.shortcuts import redirect
from functools import wraps

def anonymous_required(view_func, redirect_url='dashboard'):
    """
    Décorateur qui redirige les utilisateurs authentifiés.
    Inverse de @login_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_url)
        return view_func(request, *args, **kwargs)
    return wrapper