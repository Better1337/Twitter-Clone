from django.shortcuts import render
from .models import Profile
from django.shortcuts import redirect
# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def profile_list(request):
    if request.user.is_authenticated:
        profiles= Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        return redirect(home)