from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import UserSerializer, FollowSerializer, SetPasswordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        print ("perform_create FollowViewSet")
        serializer.save(follower=self.request.user)

class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print ("post SetPasswordView")
        serializer = SetPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

urlpatterns = [
    path('auth/', obtain_auth_token, name='api_token_auth'),
]