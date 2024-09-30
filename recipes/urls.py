from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, UserCreateView, UserDetailView


urlpatterns = [
    path("recipes/", RecipeListCreateView.as_view(), name = 'recipe-list-create'),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name = 'recipe-detail'),
    path("user/", UserCreateView.as_view(), name = 'user-create' ),
    path("user/<int:pk>/", UserDetailView.as_view(), name = 'user-detail')
]