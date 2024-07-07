from django.shortcuts import render
from .models import Profile, Tweet
from django.shortcuts import redirect
from .forms import TweetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout 


def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                return redirect('home')

        tweets = Tweet.objects.all().order_by('-date')
        return render(request, 'home.html', {"tweets": tweets, "form": form})
    else:
        tweets = Tweet.objects.all().order_by('-date')
        return render(request, 'home.html')

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Welcome ' + username)
            return redirect('home')
        else:
            messages.error(request, 'Error wrong username/password')
            return redirect('login')

    else:    
        return render(request, 'login.html', {})

def user_logout(request):
    logout(request)
    return redirect('home')