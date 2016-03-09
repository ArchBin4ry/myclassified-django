from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from . import views


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.IndexPageView.as_view()),
    url(r'^new/$', views.PostCreateView.as_view(), name='post-new'),
    url(r'^edit/(?P<pk>\d+)/$', views.PostUpdateView.as_view(), name='post-edit'),

    # listings
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post'),
    url(r'^group/(?P<pk>\d+)-(?P<slug>[-\w]+)/$', views.GroupDetail.as_view(), name='group'),

    url(r'^search/', views.SearchView.as_view(), name='search'),
    url(r'^robots\.txt$', views.RobotsView.as_view(), name='robots'),

    url(r'^user/$', views.MyPostsView.as_view(), name='my'),
    url(r'^user/profile/$', views.view_profile, name='profile'),
    url(r'^user/my/delete/(?P<pk>\d+)/$', views.PostDeleteView.as_view(), name='my-delete'),

    # authorization
    url(r'user/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^user/login/', 'django.contrib.auth.views.login', name='login'),
    url(r'^user/logout/$', 'django.contrib.auth.views.logout', name='logout'),
]

handler404 = views.page404
handler403 = views.page403
handler500 = views.page500

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
