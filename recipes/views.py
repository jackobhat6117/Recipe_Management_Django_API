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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'ingredients']

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
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

