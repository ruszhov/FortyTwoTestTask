from django.conf.urls import url
import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout')
    ]
