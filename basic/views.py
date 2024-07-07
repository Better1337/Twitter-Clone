from django.shortcuts import render
from .models import Profile, Tweet
from django.shortcuts import redirect
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-date')
    return render(request, 'home.html', {"tweets": tweets})


def profile_list(request):
    if request.user.is_authenticated:
        profiles= Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        return redirect(home)


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-date')
        if request.method == 'POST':
            current_user = request.user.profile
            action = request.POST['follow']
            if action == 'follow':
                current_user.follows.add(profile)
            elif action == 'unfollow':
                current_user.follows.remove(profile)
            current_user.save()

        return render(request, 'profile.html', {"profile": profile, "tweets": tweets})
    else:
        return redirect(home)