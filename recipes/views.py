from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer, RecipeSerializer, RatingSerializer
from rest_framework import generics, permissions, status, response
from django.contrib.auth import get_user_model
from .models import Recipe, Rating
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models




class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Get a list of users or create a new user",
        responses={200: UserSerializer(many=True), 201: UserSerializer(), 400: 'Bad Request'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format != 'html':
            return render(request, 'user_list.html', {'users': self.get_queryset()})
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user",
        responses={201: UserSerializer(), 400: 'Bad Request'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve user details",
        responses={200: UserSerializer(), 404: 'User Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if request.accepted_renderer.format == 'html':
            return render(request, 'user_detail.html', {'user': user})
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])


class RecipeListCreateView(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'ingredients']
    search_fields = ['title', 'category', 'ingredients', 'preparation_time']
    ordering_fields = ['cooking_time', 'preparation_time', 'servings']
    ordering = ['created_date']

    @swagger_auto_schema(
        operation_description="Get a list of recipes or create a new recipe",
        responses={200: RecipeSerializer(many=True), 201: RecipeSerializer(), 400: 'Bad Request'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search recipes by title, description, or ingredients",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order recipes by created_at, title, or category",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return render(request, 'recipe_list.html', {'recipes': self.get_queryset()})
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Create a new recipe",
        request_body=RecipeSerializer,
        responses={201: RecipeSerializer(), 400: 'Bad Request'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve a recipe",
        responses={200: RecipeSerializer(), 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        recipe = self.get_object()
        if request.accepted_renderer.format == 'html':
            return render(request, 'recipe_detail.html', {'recipe': recipe})
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])


class RecipesByCategoryView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a recipe by category",
        responses={200: RecipeSerializer(), 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return render(request, 'recipe_category.html', {'recipes': self.get_queryset()})
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        category = self.kwargs['category']
        queryset = Recipe.objects.filter(category=category)
        if not queryset.exists():
            raise NotFound(detail="No recipes found in this category.", code=status.HTTP_404_NOT_FOUND)
        return queryset


class RecipesByIngredientView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a recipe by ingredient",
        responses={200: RecipeSerializer(), 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return render(request, 'recipe_ingredient.html', {'recipes': self.get_queryset()})
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        ingredient = self.kwargs['ingredient']
        queryset = Recipe.objects.filter(ingredients__icontains=ingredient)
        if not queryset.exists():
            raise NotFound(detail="No recipes found with this ingredient.", code=status.HTTP_404_NOT_FOUND)
        return queryset


class RecipeByMultipleIngredientView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ingredients']

    @swagger_auto_schema(
        operation_description="Retrieve a recipe by multiple ingredients",
        responses={200: RecipeSerializer(many=True), 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'ingredients',
                openapi.IN_QUERY,
                description="Comma-separated list of ingredients",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            return render(request, 'recipe_multiple_ingredients.html', {'recipes': self.get_queryset()})
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        ingredients = self.request.query_params.get('ingredients')
        if ingredients:
            ingredient_list = [i.strip() for i in ingredients.split(',')]
            queryset = Recipe.objects.all()
            for ingredient in ingredient_list:
                queryset = queryset.filter(ingredients__icontains=ingredient)
            if not queryset.exists():
                raise NotFound(detail="No recipes found with these ingredients.", code=status.HTTP_404_NOT_FOUND)
            return queryset
        else:
            raise NotFound(detail="Please provide a comma-separated list of ingredients.", code=status.HTTP_400_BAD_REQUEST)


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
class PopularRecipesView(generics.ListAPIView):
    queryset = Recipe.objects.annotate(average_rating=models.Avg('ratings__score')).order_by('-average_rating')
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset[:10]       