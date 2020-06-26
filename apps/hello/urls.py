from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.hello, name='home'),
    url(r'^http_requests/$', views.http_requests, name='http_requests'),
    url(r'^ajax_request/$', views.ajax_request, name='ajax_request'),
    url(r'^edit_form/$', views.edit_form, name='edit_form'),
]
