from django.shortcuts import render
from models import Contact

import datetime

# Create your views here.
def hello(request):
    contact = Contact.objects.get(pk=1)
    age = int((datetime.date.today() - contact.date_of_birth).days / 365.25  )
    return render(request, 'hello/index.html', locals())