from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'groups', views.GroupViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'events-statuses', views.EventStatusViewSet,
                basename='statuses')
router.register(r'events-closests', views.ClosetsEventViewSet,
                basename='closests-events')
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^token-auth/', views.obtain_auth_token),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
