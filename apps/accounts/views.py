from django.contrib.auth import logout as user_logout
from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                    login(request, user)
                    if 'next' in request.session:
                        return redirect(request.session['next'])
                    return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, 'Username or password not correct')
                return redirect('login')
    else:
        form = LoginForm()
        if 'next' in request.GET:
            request.session['next'] = request.GET.get('next', '/')
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    user_logout(request)
    return HttpResponse('/')
