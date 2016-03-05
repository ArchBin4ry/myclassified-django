from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view()),
]

handler404 = views.page404
handler403 = views.page403
handler500 = views.page500
