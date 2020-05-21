from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]

    class Meta:
        model = Contact
admin.site.register(Contact, ContactAdmin)
