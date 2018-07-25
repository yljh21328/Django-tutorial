"""
Definition of urls for DjangoWebProject1.
"""

from django.conf.urls import include, url
from django.contrib import admin
from musics.views import hello_view
from musics.views import index_view
from rest_framework.routers import DefaultRouter
from musics.views import MusicViewSet
from shares.views import ShareViewSet
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
router = DefaultRouter()
router.register(r'music_viewset', MusicViewSet)
router.register(r'share_viewset', ShareViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', DjangoWebProject1.views.home, name='home'),
    # url(r'^DjangoWebProject1/', include('DjangoWebProject1.DjangoWebProject1.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^hello/', hello_view),
    url(r'^index/', index_view),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
