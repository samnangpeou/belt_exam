from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'login.html')

def success(request):
    if 'first_name' not in request.session:
        return redirect('/')
    context = {
        'all_wishes': Wish.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'users': User.objects.all(),
        'granted': Wish.objects.filter(grants='Yes')
    }
    return render(request, 'home.html',context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key,values in errors.items():
                messages.error(request,values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash,
        )
        request.session['first_name'] = new_user.first_name
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')
        
def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key,values in errors.items():
                messages.error(request,values)
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['first_name'] = logged_user.first_name
                request.session['user_id'] = logged_user.id
                return redirect('/success')
        messages.error(request, 'Invalid Email/Password')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def addwish(request):
    if request.method == 'POST':
        errors = Wish.objects.validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return render(request, 'addwish.html')
        Wish.objects.create(
            content=request.POST['content'],
            desc=request.POST['desc'],
            poster=User.objects.get(id=request.session['user_id']),
            grants='No'
        )
        return redirect('/success')
    return render(request,'addwish.html')


def grant(request,id):
    to_grant = Wish.objects.get(id=id)
    to_grant.grants='Yes'
    to_grant.save()
    return redirect('/success')

def like(request,id):
    liked_wish = Wish.objects.get(id=id)
    user_liked = User.objects.get(id=request.session['user_id'])
    liked_wish.likes.add(user_liked)
    return redirect('/success')


def edit(request,id):
    context = {
        'one_wish': Wish.objects.get(id=id)
    }
    if request.method =='POST':
        if request.method == 'POST':
            errors = Wish.objects.validator(request.POST)
            if len(errors) > 0:
                for key, values in errors.items():
                    messages.error(request, values)
                return render(request, 'edit.html', context)
        update = Wish.objects.get(id=id)
        update.content= request.POST['content']
        update.desc = request.POST['desc']
        update.save()
        return redirect('/success')
    return render(request, 'edit.html', context)

def delete(request,id):
    Wish.objects.get(id=id).delete()
    return redirect('/success')
    
def stats(request):
    context = {
        'ungranted': Wish.objects.filter(grants__icontains="No"),
        'granted': Wish.objects.filter(grants__icontains="Yes"),
        'user': User.objects.get(id=request.session['user_id']),
        'user_granted': Wish.objects.filter(poster=request.session['user_id'], grants__icontains="Yes"),
        'user_ungranted': Wish.objects.filter(poster=request.session['user_id'], grants__icontains="No")
    }
    return render(request, 'stats.html', context)