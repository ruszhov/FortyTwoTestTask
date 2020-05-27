from django import forms

from .models import Contact


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

    class Meta:
        model = Contact
