from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from .forms import LoginForm

# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("all good, should authentificate and redirect")
            login(request, user)
            # Redirect to a success page.
            return redirect("home")
        else:
            print("user NONE")
            # Return an 'invalid login' error message.
            messages = []
            # if User.objects.filter(username=username).exists():
                # messages.append("Password is wrong.")
            # else:
                # messages.append("Username does not exist.")
            
            return render(request, "login.html", {"form": LoginForm(request.POST), "messages" : messages})
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "login.html", {"form": LoginForm()})

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect(reverse('home'))
