from django.shortcuts import render
from .serializers import UserSerializer, RecipeSerializer
from rest_framework import generics, permissions, status, response
from django.contrib.auth import get_user_model
from .models import Recipe
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter



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

    # For GET (retrieve user)
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
        return super().get(request, *args, **kwargs)

    # For PUT (update user)
    @swagger_auto_schema(
        operation_description="Update user details",
        request_body=UserSerializer,
        responses={200: UserSerializer(), 400: 'Bad Request', 404: 'User Not Found'},
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
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    # For DELETE (delete user)
    @swagger_auto_schema(
        operation_description="Delete user account",
        responses={204: 'No Content', 404: 'User Not Found'},
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
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs['pk'])
        except User.DoesNotExist:
            raise NotFound(detail="User not found.", code=status.HTTP_400_BAD_REQUEST)

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
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

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

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a recipe",
        request_body=RecipeSerializer,
        responses={200: RecipeSerializer(), 400: 'Bad Request', 404: 'Not Found'},
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
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a recipe",
        responses={204: 'No Content', 404: 'Not Found'},
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
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def get_object(self):
        try:
            return Recipe.objects.get(pk=self.kwargs['pk'])
        except Recipe.DoesNotExist:
            raise NotFound(detail="Recipe not found.", code=status.HTTP_400_BAD_REQUEST)

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
    filterset_fields = ['category', 'preparation_time']

    @swagger_auto_schema(
        operation_description="Search for recipes by title, category, ingredients, or preparation time. "
                              "Filter by multiple ingredients with comma-separated values.",
        manual_parameters=[
             openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter('title', openapi.IN_QUERY, description="Title search", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Category filter", type=openapi.TYPE_STRING),
            openapi.Parameter('ingredients', openapi.IN_QUERY, description="Comma-separated list of ingredients", type=openapi.TYPE_STRING),
            openapi.Parameter('preparation_time', openapi.IN_QUERY, description="Preparation time filter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('cooking_time', openapi.IN_QUERY, description="Cooking time filter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('servings', openapi.IN_QUERY, description="Number of servings", type=openapi.TYPE_INTEGER),
        ],
        responses={200: RecipeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Recipe.objects.filter(user=self.request.user)

        # Filter by title (optional)
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Filter by category (optional)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__icontains=category)

        # Filter by preparation time (optional)
        preparation_time = self.request.query_params.get('preparation_time')
        if preparation_time:
            queryset = queryset.filter(preparation_time__lte=preparation_time)

        # Filter by cooking time (optional)
        cooking_time = self.request.query_params.get('cooking_time')
        if cooking_time:
            queryset = queryset.filter(cooking_time__lte=cooking_time)

        # Filter by servings (optional)
        servings = self.request.query_params.get('servings')
        if servings:
            queryset = queryset.filter(servings__gte=servings)

        # Filter by multiple ingredients (optional)
        ingredients = self.request.query_params.get('ingredients')
        if ingredients:
            ingredient_list = ingredients.split(',')
            # Filter by each ingredient in the list
            for ingredient in ingredient_list:
                queryset = queryset.filter(ingredients__icontains=ingredient.strip())

        return queryset
    

  