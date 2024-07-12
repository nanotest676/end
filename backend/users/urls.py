from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FollowViewSet, SetPasswordView

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'follows', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('set_password/', SetPasswordView.as_view(), name='set_password'),
]
