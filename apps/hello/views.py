from django.shortcuts import render, HttpResponse
from models import Contact, HttpRequestLog
import json

import datetime


def hello(request):
    contact = Contact.objects.all().first()
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    return render(request, 'hello/index.html',
                  {'contact': contact, 'age': age})


def http_requests(request):
    requests = HttpRequestLog.objects.all().order_by('-date')[:10]
    request.session['viewed_nmb'] = HttpRequestLog.objects.count()
    return render(request, 'hello/requests.html',
                  {'requests': requests})


def ajax_request(request):
    response_data = {}
    response_data['total'] = \
        HttpRequestLog.objects.count() - request.session['viewed_nmb'] \
        if 'viewed_nmb' in request.session \
        else HttpRequestLog.objects.count()
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
