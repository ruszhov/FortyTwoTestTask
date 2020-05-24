from django.contrib import admin
from .models import Contact, HttpRequestLog


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]

    class Meta:
        model = Contact
admin.site.register(Contact, ContactAdmin)


class HttpRequestLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HttpRequestLog._meta.fields]

    class Meta:
        model = HttpRequestLog
admin.site.register(HttpRequestLog, HttpRequestLogAdmin)
