from django.shortcuts import render, HttpResponse, redirect
from models import Contact, HttpRequestLog
from forms import ContactForm
import json

import datetime


def hello(request):
    contact = Contact.objects.get(pk=1)
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    return render(request, 'hello/index.html', locals())


def http_requests(request):
    if request.is_ajax():
        response_data = {}
        response_data['total'] = len(HttpRequestLog.objects.all())
        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")
    else:
        requests = HttpRequestLog.objects.all().order_by('-date')[:10]
        return render(request, 'hello/requests.html', locals())


def edit_form(request):
    return render(request, 'hello/edit_form.html', locals())
