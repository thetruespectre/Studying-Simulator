from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.method == "POST":
        new_message = request.POST.get("new_message")
        message_classroom = Classroom.objects.get(id=request.POST.get("message_classroom"))
        if new_message and message_classroom:
            Message.objects.create(
                user = request.user,
                body = new_message,
                classroom = message_classroom
            )
            
            return redirect("classroom", message_classroom.id)
    
    q = request.GET.get('q')
    if q == None:
        classrooms = Classroom.objects.all()
        messagesChat = Message.objects.all()
    else:
        classrooms = Classroom.objects.filter(
            Q(name__icontains=q) |
            Q(subject__name__icontains=q) |
            Q(description__icontains=q) |
            Q(host__username__icontains=q)
        )
        
        messagesChat = Message.objects.filter(
            Q(classroom__subject__name__icontains=q)
        )
    
    subjects = Subject.objects.all()

    count = 0
    for classroom in classrooms:
        if request.user.is_authenticated: 
            if request.user in classroom.participants.all() or request.user.id == classroom.host.id or request.user.is_superuser:
                count += 1
    
    not_new = False
    for i in Classroom.objects.all():
        if request.user in i.participants.all():
            not_new = True
    
    context = {"classrooms":classrooms, "subjects":subjects, "messagesChat":messagesChat, "not_new":not_new, "count":count}
    return render(request, "base/home.html", context)

@login_required(login_url="login")
def classroom(request, id):
    profile = False
    classroom = Classroom.objects.get(id=id)
    messagesChat = classroom.message_set.all()
    
    if request.user not in classroom.participants.all():
        if request.user.is_superuser == False and request.user.id != classroom.host.id:
            return render(request, "base/skibidi.html")
    
    if request.method == "POST" and request.POST.get("new_participant") == None:
        if request.user in classroom.participants.all() or request.user.is_superuser or request.user.id == classroom.host.id:
            Message.objects.create(
                user = request.user,
                classroom = classroom,
                body = request.POST.get("message")
            )
            return redirect("classroom", classroom.id)
        else:
            return render(request, "base/skibidi.html")
        
    elif request.method == "POST" and request.POST.get("message") == None:
        if request.user in classroom.participants.all() or request.user.is_superuser or request.user.id == classroom.host.id:
            new_participant = request.POST.get("new_participant")
            if userExists(new_participant):
                usr = User.objects.get(username=new_participant)
                classroom.participants.add(usr)
                return redirect("classroom", classroom.id)
            else:
                return HttpResponse("User does not exist")
        else:
            return render(request, "base/skibidi.html")
    
    context = {"classroom":classroom, "messagesChat":messagesChat, "profile":profile}
    return render(request, "base/classroom.html", context)

@login_required(login_url="login")
def classroomCreate(request):
    if request.method == "POST":
        form  = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.host = request.user
            classroom.save()
            
            return redirect("home")
    
    form = ClassroomForm()
    context = {"form":form}
    return render(request, "base/updateForm.html", context)

@login_required(login_url="login")
def classroomEdit(request, id):
    classroom = Classroom.objects.get(id=id)
    
    if request.method == "POST":
        if request.user.id == classroom.host.id or request.user.is_superuser:
            form  = ClassroomForm(request.POST, instance=classroom)
            if form.is_valid():
                room = form.save(commit=False)
                room.is_updated = True
                room.save()
                
                return redirect("classroom", classroom.id)
        else:
            return render(request, "base/skibidi.html")
    
    form = ClassroomForm(instance=classroom)
    context = {"form":form}
    return render(request, "base/updateForm.html", context)

@login_required(login_url="login")
def messageEdit(request, id):
    messageChat = Message.objects.get(id=id)
    
    if request.method == "POST":
        if request.user.id == messageChat.user.id or request.user.is_superuser:
            form = MessageForm(request.POST, instance=messageChat)
            if form.is_valid:
                mes = form.save(commit=False)
                mes.is_updated = True
                mes.save()
                
                return redirect("classroom", messageChat.classroom.id)
        else:
            return render(request, "base/skibidi.html")
    
    form = MessageForm(instance=messageChat)
    context = {"form": form}
    return render(request, "base/updateForm.html", context)
    
@login_required(login_url="login")
def messageDelete(request, id):
    messageChat = Message.objects.get(id=id)
    if request.method == "POST":
        if request.user.id == messageChat.user.id or request.user.is_superuser:
            messageChat.delete()
            return redirect("classroom", messageChat.classroom.id)

        else:
            return render(request, "base/skibidi.html")
        
    context = {"obj":messageChat.body[:50]}
    return render(request, "base/delete.html", context)

@login_required(login_url="login")
def deleteClassroom(request, id):
    classroom = Classroom.objects.get(id=id)
    if request.method == "POST":
        if request.user.id == classroom.host.id or request.user.is_superuser:
            classroom.delete()
            return redirect("home")
        else:
            return render(request, "base/skibidi.html")
    
    context = {"obj":classroom.name}
    return render(request, "base/delete.html", context)

@login_required(login_url="login")
def subjectCreate(request):
    if request.method == "POST":
        form  = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    form = SubjectForm()
    subject = None
    context = {"form":form, "subject":subject}
    return render(request, "base/updateForm.html", context)

def loginForm(request):
    page = "login"
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if userExists(username):
            user = authenticate(username=username, password=password)
            if user:
                if request.user.is_authenticated:
                    logout(request)
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username or Password is Incorrect")
        else:
            messages.error(request, "User doesn't exist")    
    
    context = {"page":page}
    return render(request, "base/login.html", context)

def logoutForm(request):
    logout(request)
    return redirect("home")

def registerForm(request):
    page = "register"
    form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            if request.user.is_authenticated:
                logout(request)
            login(request, user)
            return redirect("home")
    
    context = {"form":form, "page":page}
    return render(request, "base/login.html", context)

@login_required(login_url="login")
def userEdit(request):
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile-page", request.user.id)
    
    context = {"form":form}
    return render(request, 'base/userEdit.html', context)

@login_required(login_url="login")
def profilePage(request, id):
    profile = True
    
    usr = User.objects.get(id=id)
    classrooms = usr.classroom_set.all()
    
    context = {"profile":profile, "user":usr, "classrooms":classrooms}
    return render(request, "base/profile.html", context)

def userExists(username):
    try:
        user = User.objects.get(username=username)
        if user:
            return True
        else:
            return False
    except:
        return False
    
