from django.contrib.auth import logout as user_logout
from django.shortcuts import HttpResponse


def logout(request):
    user_logout(request)
    return HttpResponse('/')
