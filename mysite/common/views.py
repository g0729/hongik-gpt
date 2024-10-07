from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from common.forms import UserForm

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect("common:login")


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/dialog")
    else:
        form = UserForm()
    return render(request, "common/signup.html", {"form": form})


def page_not_found(request, exception):
    return render(request, "common/404.html", {})
