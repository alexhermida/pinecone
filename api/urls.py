from django.conf.urls import include, url

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
