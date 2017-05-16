from django.shortcuts import render, redirect, reverse
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'user_dashboard/index.html')

def signin(request):
    return render(request, 'user_dashboard/signin.html')

def authenticate(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.login(email, password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            return redirect(reverse('dashboard:signin'))
        else:
            request.session["id"] = user["user"].id
            request.session["user_level"] = user["user"].user_level
            return redirect(reverse('dashboard:dashboard'))
    else:
        return redirect(reverse('dashboard:signin'))

def register(request):
    return render(request, 'user_dashboard/register.html')

def register_add(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.add_user(first_name, last_name, email, password, confirm_password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            if request.session["user_level"] == 9:
                return redirect(reverse('dashboard:new'))
            return redirect(reverse('dashboard:register'))
        elif "id" not in request.session:
            request.session["id"] = user["user"].id
            request.session["user_level"] = user["user"].user_level
        return redirect(reverse('dashboard:dashboard'))
    else:
        if request.session["user_level"] == 9:
            return redirect(reverse('dashboard:new'))
        return redirect(reverse('dashboard:register'))

def logout(request):
    del request.session['id']
    del request.session["user_level"]
    return redirect(reverse('dashboard:index'))

def dashboard(request):
    if request.session["user_level"] == 9:
        return redirect(reverse('dashboard:dashboard_admin'))
    users = User.objects.all()
    context = {
            "users":users,
    }
    return render(request, 'user_dashboard/dashboard.html', context)

def dashboard_admin(request):
    if request.session["user_level"] == 1:
        return redirect(reverse('dashboard:dashboard'))
    users = User.objects.all()
    context = {
            "users":users,
    }
    return render(request, 'user_dashboard/dashboard_admin.html', context)

def show(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        redirect(reverse('dashboard:dashboard'))
    context = {
            "user":user
    }
    return render(request, 'user_dashboard/show.html', context)

def edit(request):
    try:
        user = User.objects.get(id=request.session['id'])
    except:
        redirect(reverse('dashboard:dashboard'))
    context = {
            "user":user
    }
    return render(request, 'user_dashboard/edit.html', context)

def update(request, id):
    if request.POST["edit_field"] == "information":
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        if "user_level" in request.POST:
            user_level= request.POST["user_level"]
            user = User.objects.update_name(email, first_name, last_name, id, user_level)
        else:
            user = User.objects.update_name(email, first_name, last_name, id)
    elif request.POST["edit_field"] == "password":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.update_password(password, confirm_password, id)
    else:
        user = User.objects.get(id=request.session['id'])
        user.description = request.POST["description"]
        user.save()
        return redirect(reverse("dashboard:show", kwargs={'id':user.id}))
    if "errors" in user:
        for error in user["errors"]:
            messages.error(request, error)
            if "user_level" in request.POST:
                return redirect(reverse("dashboard:edit_admin", kwargs={'id':id}))
            return redirect(reverse('dashboard:edit'))
    return redirect(reverse("dashboard:show", kwargs={'id':id}))

def edit_admin(request, id):
    try:
        user = User.objects.get(id=id)
        context = {"user":user}
    except:
        redirect(reverse('dashboard:dashboard'))
    return render(request, 'user_dashboard/edit_admin.html', context)

def new(request):
    return render(request, 'user_dashboard/new.html')

def message(request, id):
    if request.method == "POST":
        content = request.POST["message"]
        sender = User.objects.get(id=request.session["id"])
        receiver = User.objects.get(id=id)
        Message.objects.create(content=content, sender=sender, receiver=receiver)
    return redirect(reverse('dashboard:show', kwargs={'id':id}))

def comment(request, user_id, message_id):
    if request.method == "POST":
        content = request.POST["comment"]
        user = User.objects.get(id=request.session["id"])
        message = Message.objects.get(id=message_id)
        Comment.objects.create(content=content, user=user, message=message)
    return redirect(reverse('dashboard:show', kwargs={'id':user_id}))

def delete_message(request, user_id, message_id):
    Message.objects.get(id=message_id).delete()
    return redirect(reverse('dashboard:show', kwargs={'id':user_id}))

def delete_comment(request, user_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect(reverse('dashboard:show', kwargs={'id':user_id}))
