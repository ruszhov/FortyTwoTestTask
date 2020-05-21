from django.db import models

class Contact(models.Model):
    first_name = models.CharField('First Name',max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    date_of_birth = models.DateField('Date of birth', blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    skype = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
        return '%s %s' % self.first_name, self.last_name