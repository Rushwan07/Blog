from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from blog.models import Post
from .models import Contact


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")


def about(request):
    return render(request, 'home/about.html')


def search(request):
    quary = request.GET['quary']
    if len(quary) == 70:
        Allpost = Post.objects.none()
    else:
        Allposttitle = Post.objects.filter(title__icontains=quary)
        Allpostcontent = Post.objects.filter(content__icontains=quary)
        AllposAutho = Post.objects.filter(author__icontains=quary)
        Allpost = Allposttitle.union(Allpostcontent, AllposAutho)
    if Allpost.count() == 0:
        messages.error(request, 'NO Result Found sorry..')
    params = {'Allpost': Allpost, 'quary': quary}
    return render(request, 'home/search.html', params)


def SingUpHandeling(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, " Passwords does not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder Account created SuccessFully.!  ")
        return redirect('../')

    else:
        return HttpResponse("404 Not Found")


def LoginHandeling(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully locked IN..")
            return redirect("../")

        else:
            messages.error(request, 'Credential Error Please try again..')
            return redirect('/')


def LogoutHandeling(request):
    logout(request)
    messages.success(request, 'LogedOut')
    return redirect('/')
