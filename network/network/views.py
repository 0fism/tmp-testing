from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Profile, Like
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import OuterRef, Subquery, Count, Exists
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import NewPost, EditPost

def index(request):
    posts = Post.objects.order_by('-timestamp').all()
    # likes = Like.objects.filter(post=OuterRef('id'), user=request.user)
    # posts = Post.objects.filter().order_by('-timestamp')
    paginator = Paginator(posts, 10)    # Show 10 posts per page.
    page_number = request.GET.get('page') 
    if page_number != None:
        try:
            page_obj = paginator.get_page(page_number)
        except:
            page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(1)

    return render(request, "network/index.html", {
        'posts': page_obj,
        'form': NewPost(),
        'form_edit': EditPost()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# TODO
def following(request):
    if request.user.is_authenticated:
        # request.session['_auth_user_id']
        # Profile.objects.filter(follower=request.user).following.all()
        # SELECT likeModel WHERE user LIKE '%user%';
        followers = Profile.objects.filter(follower=request.user)
        # id
        posts = Post.objects.filter(user_id__in=followers.values('following_id')).order_by(
            '-timestamp')
    else:
        return HttpResponseRedirect(reverse("login"))

    paginator = Paginator(posts, 10)    # Show 10 posts per page.
    page_number = request.GET.get('page') 
    if page_number != None:
        try:
            page_obj = paginator.get_page(page_number)
        except:
            page_obj = paginator.get_page(1)
    else:
        page_obj = paginator.get_page(1)

    return render(request, "network/following.html", {
        'posts': page_obj,
        'form': NewPost()
    })

# TODO
def post_message(request):

    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        form = NewPost(request.POST)
        if form.is_valid():
            post = Post(user=User.objects.get(username=request.user), text=form.cleaned_data["post"])
            post.save()
            return HttpResponseRedirect(reverse("index"))

# TODO
def edit_post(request, id):
    if request.method != "POST":
        return JsonResponse({}, status=400)
    else:
        form = EditPost(request.POST)
        if form.is_valid():
            text = form.cleaned_data["id_form_edit"]
            Post.objects.filter(id=id, user=request.user).update(text=text)
            return JsonResponse({"text": text}, status=201)
        else:
            return JsonResponse({}, status=400)


def follow(request, id):
    
    user = User.objects.get(username=request.user)
    follower = Profile.objects.get_or_create(follower=user, following=User.objects.get(id=id))
    if follower[1] is True:
        status = 'following'
    else:
        Profile.objects.filter(follower=user, following=User.objects.get(id=id)).delete()
        status = 'unfollow'

    total_followers = Profile.objects.filter(following=User.objects.get(id=id)).count()
    return JsonResponse({"status": status, "total_followers": total_followers})

def like(request, id):

    
    like = Like.objects.get_or_create(user=User.objects.get(username=request.user),post=Post.objects.get(id=id)
        )
    if like[1] is True:
        likeIcon = 'fas fa-heart'
    else: 
        likeIcon = 'far fa-heart'
        Like.objects.filter(user=User.objects.get(username=request.user), post=Post.objects.get(id=id)).delete()
    totalLikes = Like.objects.filter(post=Post.objects.get(id=id)).count()
    return JsonResponse({ "id": id, "likeIcon": likeIcon, "totalLikes": totalLikes})

# TODOGOOD
@login_required
def profile(request, username):
   
    #present profile user
    profile_user = User.objects.get(username=username)
    
    if request.user.is_authenticated:
        #all user
        user = request.session['_auth_user_id']
        likes = Like.objects.filter(post=OuterRef('id'), user_id=user)
        '''posts = Post.objects.filter().order_by('-timestamp').annotate(totalLike=Count(likes.values('id')))'''
        posts = Post.objects.filter(user=profile_user).order_by('-timestamp').annotate(totalLike=Count(likes.values('id')))
        sum_posts = Post.objects.filter(user=profile_user).count()
        exist_following = Profile.objects.filter(follower=user, following=profile_user).count()
        
    else:
        posts = Post.objects.filter(user=profile_user).order_by('timestamp').all()
        sum_posts = 0 
        exist_following = 0


    paginator = Paginator(posts, 10)    # Show 10 posts per page.
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    total_following = Profile.objects.filter(follower=profile_user).count()
    total_followers = Profile.objects.filter(following=profile_user).count()
    

    return render(request, "network/profile.html", {
        'posts': page_obj,
        'form': NewPost(),
        'form_edit': EditPost(),

        "sum_posts": sum_posts,
        "profile_user": profile_user, 
        "exist_following": exist_following,
        'total_following': total_following, 
        'total_followers': total_followers 
        
    })
