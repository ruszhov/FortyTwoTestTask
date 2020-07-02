from django import forms
import re
import datetime
from apps.hello.models import Contact


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check_jabber(jabber):
    """Check if Jabber line looks like email"""
    if jabber is not None and jabber != '':
        if (re.search(regex, jabber)):
            return True
        else:
            return False


def check_years(birth_date):
    """Check if age isn't longer than 100 years"""
    if isinstance(birth_date, datetime.date):
        age = datetime.datetime.today().year - birth_date.year
        if age <= 100:
            return True
        else:
            return False


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['date_of_birth'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.fields['bio'].widget.attrs['placeholder'] = 'Bio'
        self.fields['email'].widget\
            .attrs['placeholder'] = 'contact@example.com'
        self.fields['skype'].widget.attrs['placeholder'] = 'Skype Nickname'
        self.fields['jabber'].widget.attrs['placeholder'] = 'Jabber Account'
        self.fields['other_contacts'].widget\
            .attrs['placeholder'] = 'Other Contacts'

    def clean_jabber(self):
        jabber_data = self.cleaned_data.get('jabber')
        if not check_jabber(jabber_data):
            raise forms.ValidationError(
                'This value can\'t be used as Jabber account')
        return jabber_data

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not check_years(date_of_birth):
            raise forms.ValidationError(
                'Age can\'t be longer than 100 years!!!!')
        return date_of_birth

    class Meta:
        model = Contact
