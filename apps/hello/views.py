from django.shortcuts import render, HttpResponse
from apps.hello.models import Contact, HttpRequestLog
from apps.hello.forms import ContactForm
from django.contrib.auth.decorators import login_required
import json

import datetime

login_url = '/login/'


def hello(request):
    contact = Contact.objects.all()[0]
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    return render(request, 'hello/index.html',
                  {'contact': contact, 'age': age})


def http_requests(request):
    requests = HttpRequestLog.objects.all().order_by('-date')[:10]
    request.session['viewed_nmb'] = HttpRequestLog.objects.count()
    return render(request, 'hello/requests.html',
                  {'requests': requests})


def ajax_request(request):
    response_data = {'total': HttpRequestLog.objects.count()}
    if 'viewed_nmb' in request.session:
        response_data['total'] -= request.session['viewed_nmb']
    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


@login_required(login_url=login_url)
def edit_form(request):
    current_entry = Contact.objects.all()[0]
    if request.method == 'POST' and request.is_ajax():
        form = ContactForm(request.POST, request.FILES, instance=current_entry)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'success': 'success'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error': form.errors}))
    else:
        form = ContactForm(instance=current_entry)
    return render(request, 'hello/edit_form.html',
                  {'form': form, 'entry': current_entry})
