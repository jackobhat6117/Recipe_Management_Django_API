from django.shortcuts import render
from .serializers import UserSerializer, RecipeSerializer
from rest_framework import generics, permissions, status, response
from django.contrib.auth import get_user_model
from .models import Recipe
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, ValidationError


User = get_user_model()

class RecipeListCreateView(generics.ListCreateAPIView):

    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'ingredients']

    def get_queryset(self):
        return Recipe.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Recipe.objects.filter(user = self.request.user)
    
    def get_object(self):
        try: 
            return Recipe.objects.get(pk = self.kwargs['pk'])
        except:
            raise NotFound(detail="Recipe not found.", code=status.HTTP_400_BAD_REQUEST)
    
    

    
    
