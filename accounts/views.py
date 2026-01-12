from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

# Create your views here.

def register(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Password do not match")
            return redirect("register")
        
        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "user is already exist")
            return redirect("register")
        
        user = User.objects.create_user(mobile=mobile, password=password)
        messages.success(request, "Account created Successfully.")
        return redirect("login")
    return render(request, "accounts/register.html")



def mobile_login(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        # 🔐 authenticate uses USERNAME_FIELD = "mobile"
        user = authenticate(request, mobile=mobile, password=password)

        if user:
            login(request, user)
            return redirect("product_list")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid Mobile Number or Password"}
        )
    
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")


def create_company(request):
    if request.method == "POST":
        name = request.POST.get("name")

        company = company.objects.create(
            name=name,
            onwer=request.user
        )

        request.user.profile.company = company
        request.user.profile.role = "admin"
        request.user.profile.role = "admin"
        request.user.profile.save()

        return redirect("task_list")
    return render(request, "acounts/create_company.html")


        