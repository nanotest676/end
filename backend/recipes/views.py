from rest_framework import viewsets
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticated

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
