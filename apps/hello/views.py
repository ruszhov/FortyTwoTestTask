from django.shortcuts import render
from models import Contact

import datetime


def hello(request):
    contact = Contact.objects.first()
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25)
    return render(request, 'hello/index.html', locals())
