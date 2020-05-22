from django.db import models


class Contact(models.Model):
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    date_of_birth = models.DateField('Date of birth', blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    skype = models.CharField(max_length=50, blank=True, null=False)
    jabber = models.CharField(max_length=50, blank=True, null=False)
    other_contacts = models.TextField(max_length=200, blank=True, null=False)

    def __str__(self):
        return self.first_name, self.last_name


class HttpRequestLog(models.Model):
    date = models.DateTimeField('Datetime of request', db_index=True)
    request_method = models.CharField(
        'Request method', max_length=6, db_index=True)
    url = models.CharField('URL', max_length=256)
    server_protocol = models.CharField('Server Protocol', max_length=256)

    def __unicode__(self):
        return u'%s %s %s %s' % (
                    self.date.strftime('%Y-%m-%d %H:%M:%S'),
                    self.request_method,
                    self.url,
                    self.server_protocol
                )
