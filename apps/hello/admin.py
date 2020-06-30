from django.contrib import admin
from apps.hello.models import Contact, HttpRequestLog, ModelActionLog


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


class ModelActionLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ModelActionLog._meta.fields]

    class Meta:
        model = ModelActionLog
admin.site.register(ModelActionLog, ModelActionLogAdmin)
