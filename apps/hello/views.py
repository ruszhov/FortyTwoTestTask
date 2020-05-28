from django.shortcuts import render, HttpResponse
from models import Contact, HttpRequestLog
from forms import ContactForm
from django.contrib.auth.decorators import login_required
import json

import datetime

login_url = '/login/'


def hello(request):
    contact = Contact.objects.all().first()
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    if 'test' in request.session:
        test = request.session['test']
        print(test)
    return render(request, 'hello/index.html', locals())


def http_requests(request):
    requests = HttpRequestLog.objects.all().order_by('-date')[:10]
    return render(request, 'hello/requests.html', locals())


def ajax_request(request):
    response_data = {}
    response_data['total'] = len(HttpRequestLog.objects.all())
    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")


@login_required(login_url=login_url)
def edit_form(request):
    entry = Contact.objects.all().first()
    form = ContactForm(instance=entry)
    return render(request, 'hello/edit_form.html', locals())


@login_required(login_url=login_url)
def ajax_submit(request):
    current_entry = Contact.objects.all().first()
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=current_entry)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'success': 'success'}),
                                content_type="application/json")
    return HttpResponse("form not valid")
