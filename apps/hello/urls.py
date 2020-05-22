from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.hello, name='home'),
    url(r'^http_requests/$', views.http_requests, name='http_requests')
]
