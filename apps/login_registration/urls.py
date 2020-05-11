from django.conf.urls import url
from . import views

app_name = 'login_registration'

urlpatterns = [
    # # registers user info if all info is valid
    url(r'^register$', views.register, name='register'),
    # logs in user if user info is valid and saves info into a session
    url(r'^login$', views.login, name='login'),
    # logs out a user and deletes session containing user info
    url(r'^logout$', views.logout, name='logout')
]
