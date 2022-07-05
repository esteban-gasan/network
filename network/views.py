import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm
from .models import Post, User


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all()
    })


@login_required
def new_post(request: HttpRequest):
    if request.method != "POST":
        return render(request, "network/post_form.html", {"form": PostForm})

    post_form = PostForm(request.POST)
    if not post_form.is_valid():
        # Send back the form submitted if errors are found
        return render(request, "network/post_form.html", {"form": post_form})

    # Create object but don't save to the database yet
    new_post = post_form.save(commit=False)
    new_post.author = request.user
    new_post.save()

    return redirect("index")


def profile(request: HttpRequest, pk: int):
    user = get_object_or_404(User, id=pk)
    return render(request, "network/profile.html", {"user_viewed": user})


@csrf_exempt
@login_required
def follow(request: HttpRequest, user_id: int):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    if request.user.id == user_id:
        return JsonResponse({"error": "You can only follow other users."}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with id {user_id} does not exist."
        }, status=400)

    if request.user.following.contains(user):
        request.user.following.remove(user)
        msg = "Unfollowed"
    else:
        request.user.following.add(user)
        msg = "Following"

    return JsonResponse({"message": f"{msg} {user.username}"}, status=201)


@login_required
def following(request: HttpRequest):
    return render(request, "network/following.html", {
        "posts": Post.objects.filter(author_id__in=request.user.following.all())
    })


@csrf_exempt
@login_required
def like(request: HttpRequest, post_id: int):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"Post with id {post_id} does not exist."
        }, status=400)

    user = request.user
    if post.likes.contains(user):
        post.likes.remove(user)
        msg = "Unliked"
    else:
        post.likes.add(user)
        msg = "Liked"

    return JsonResponse({"message": f"{msg} post {post.id}"}, status=201)


@csrf_exempt
@login_required
def edit(request: HttpRequest, post_id: int):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({
            "error": f"Post with id {post_id} does not exist."
        }, status=400)

    if request.user != post.author:
        return JsonResponse(
            {"error": "You can only edit your own posts."}, status=400
        )

    if (text := json.loads(request.body).get("text")) is None:
        return JsonResponse({"error": "Text is empty!"}, status=400)

    post.text = text
    post.save()
    msg = f"Edited post with id {post.id}"

    return JsonResponse({"message": msg}, status=201)


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
