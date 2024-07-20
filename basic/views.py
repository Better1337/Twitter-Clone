from django.shortcuts import render
from .models import Profile, Tweet
from django.shortcuts import redirect, get_object_or_404
from .forms import TweetForm, SignUpForm, ProfileImageForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
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
        return render(request, 'login.html')

def profile_list(request):
    if request.user.is_authenticated:
        profiles= Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        return redirect('home')


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
        return redirect('home')

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

def user_register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {'form': form})    

def user_update(request):
    if request.user.is_authenticated:
        form = SignUpForm(request.POST or None, instance=request.user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, 'user_update.html', {'form': form})
    else:
        return redirect('home')

def update_profile_image(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        form = ProfileImageForm(request.POST or None, request.FILES or None, instance=profile)
    
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('home')
        return render(request, 'update_profile_image.html', {'form': form})
    else:
        return redirect('login')

def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        user = request.user
        if user in tweet.likes.all():
            tweet.likes.remove(user)
        else:
            tweet.likes.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')

def tweet_delete(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            tweet.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')

def tweet_update(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user == tweet.user:
            form = TweetForm(request.POST or None, instance=tweet)
            if request.method == 'POST':
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, 'Tweet updated')
                    next_url = request.POST.get('next', 'home')
                    return redirect(next_url)
            next_url = request.GET.get('next', '')
            return render(request, 'tweet_update.html', {'form': form, 'tweet': tweet, 'next': next_url})
        else:
            messages.error(request, 'You are not allowed to update this tweet')
            return redirect('home')
    else:
        return redirect('login')

def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search = request.POST['search']
            searched_tweets = Tweet.objects.filter(text__icontains=search)
            return render(request, 'search.html', {'search': search, 'searched_tweets': searched_tweets})
        else:
            return render(request, 'search.html')
    else:
        return redirect('login')

