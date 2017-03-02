from django.conf.urls import url

from . import views

app_name = 'cel'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^test/$', views.test, name='test'),
    url(r'^start/$', views.start, name='start'),
    url(r'^(?P<pk>[\w{}-]{1,40})/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<task_id>[\w{}-]{1,40})/progress/$', views.progress, name='progress'),
    url(r'^(?P<task_id>[\w{}-]{1,40})/state/$', views.state, name='state'),
    url(r'^(?P<task_id>[\w{}-]{1,40})/failure/$', views.failure, name='failure'),
    url(r'^(?P<task_id>[\w{}-]{1,40})/result/$', views.result, name='result'),
]
