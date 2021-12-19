from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, LoginForm
from .models import Profile, Post
import time

from .forms import UserRegistrationForm

def index(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    return render(request, 'app/index.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('../' + cd['username'] + '/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    return redirect('../')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            pr = Profile(user=new_user, bio="")
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            pr.save()
    return redirect('../')

def profile(request, username):
    ctx = {
        "user" : User.objects.all().get(username=username),
        "own": False,
        "posts": [],
        "bio": "",
        "friends": [],
        "friends_num": "0"
    }
    ctx["auth"] = request.user.is_authenticated
    ctx["posts"] = list(sorted(ctx["user"].profile.post_set.all(), reverse=True, key=lambda x: x.date))
    
    ctx["friends"] = ctx["user"].profile.friends.all()
    ctx["friends_num"] = str(len(ctx["friends"]))

    ctx["subs"] = ctx["user"].profile.subs.all()
    ctx["subs_num"] = str(len(ctx["subs"]))
    ctx["bio"] = ctx["user"].profile.bio
    
    if request.user.is_authenticated and request.user.username == username:
        ctx["own"] = True
    else:
        ctx["sub"] = False
        for fr in request.user.profile.friends.all():
            if fr.user.username == username:
                ctx["sub"] = True
    return render(request, 'app/profile.html', ctx)


def change_data(request, username):
    ctx = {
        "user" : User.objects.all().get(username=username),
        "own": False
    }
    if request.user.is_authenticated and request.user.username == username:
        ctx["own"] = True
    return render(request, 'app/change_data.html', ctx)


def create_post(requset, username):
    if requset.user.is_authenticated:
        if requset.method == 'POST':
            user_form = CreatePostForm(requset.POST)
            if user_form.is_valid():
                u = User.objects.all().get(username=requset.user.username).profile
                p = u.post_set.create(text=requset.POST["text"], date=time.time())
                u.save()
                p.save()
    return redirect('profile', requset.user.username)

def change_username(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            u = User.objects.all().get(username=request.user.username)
            u.username = request.POST["new_username"]
            u.save()
    return redirect('profile', request.POST["new_username"])

def change_bio(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            u = User.objects.all().get(username=request.user.username)
            u.profile.bio = request.POST["new_bio"]
            u.profile.save()
    return redirect(request.user.username)

def get_profile(request):
    try:
        u = User.objects.all().get(username=request.POST['search_username'])
        return redirect('profile', u.username)
    except:
        return redirect('index')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def profile_subs(request, username):
    u = User.objects.all().get(username=username)
    ctx = {
        "profiles": u.profile.subs.all(),
        "list_title": "Подписчики @" + username
    }

    return render(request, 'app/profiles_list.html', ctx)


def profile_friends(request, username):
    u = User.objects.all().get(username=username)
    ctx = {
        "profiles": u.profile.friends.all(),
        "list_title": "Подписки @" + username
    }

    return render(request, 'app/profiles_list.html', ctx)


def add_friend(request, username):
    if request.user.is_authenticated:
        u = User.objects.all().get(username=username)
        f = User.objects.all().get(username=request.user.username)
        f.profile.friends.add(u.profile)
        f.profile.save()
        u.profile.subs.add(f.profile)
        u.profile.save()
        return redirect('profile', username)
    return redirect('index')

def remove_friend(request, username):
    if request.user.is_authenticated:
        u = User.objects.all().get(username=username)
        f = request.user

        f.profile.friends.remove(u.profile)
        u.profile.subs.remove(f.profile)
        f.profile.save()
        u.profile.save()
    return redirect('profile', username)
    