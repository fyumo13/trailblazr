from django.conf.urls import url
from . import views

app_name = 'trailblazr'

urlpatterns = [
    # displays user login and registration page
    url(r'^$', views.index, name='index'),
    # displays user dashboard
    url(r'dashboard$', views.dashboard, name='dashboard'),
    # displays search results and search bar
    url(r'^search_bar$', views.search_bar, name='search_bar'),
    # searches for trails near specific location
    url(r'^search$', views.search, name='search'),
    # adds trail to user's dashboard
    url(r'^add_trail/(?P<id>\d+)$', views.add_trail, name='add_trail'),
    # deletes specific trail
    url(r'del_trail/(?P<id>\d+)$', views.del_trail, name='del_trail'),
    # # displays specific trail page
    url(r'trail/(?P<id>\d+)$', views.show_trail, name='show_trail')
]