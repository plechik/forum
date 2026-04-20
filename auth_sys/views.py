from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm


# Create your views here.
def ReqisterView(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum:home')
        else:
            messages.error(request, "Виправте помилку та спробуйте ще раз.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_sys/register.html', {'form': form})

def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomLoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('forum:home')
            else:
                messages.error(request, "Невірний логін або пароль.")
        else:
            form = CustomLoginForm()
        return render(request, 'auth_sys/login.html', {'form': form})
    return redirect('forum:home')

def LogoutView(request):
    logout(request)
    messages.success(request, "Ви вийшли з акаунту.")
    return redirect('forum:home')