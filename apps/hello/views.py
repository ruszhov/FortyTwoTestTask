from django.shortcuts import render, HttpResponse
from models import Contact, HttpRequestLog
import json

import datetime


def hello(request):
    contact = Contact.objects.get(pk=1)
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    return render(request, 'hello/index.html', locals())



def http_requests(request):
    requests = HttpRequestLog.objects.all().order_by('-date')[:10]
    return render(request, 'hello/requests.html', locals())
    pass
