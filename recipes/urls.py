from django.urls import path
from .views import RecipeListCreateView, RecipeDetailView, UserCreateView, UserDetailView, RecipesByCategoryView, RecipesByIngredientView, RecipeByMultipleIngredientView


urlpatterns = [
    path("user/", UserCreateView.as_view(), name = 'user-create' ),
    path("user/<int:pk>/", UserDetailView.as_view(), name = 'user-detail'),
    path("recipes/", RecipeListCreateView.as_view(), name = 'recipe-list-create'),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name = 'recipe-detail'),
    path('recipes/category/<str:category>/', RecipesByCategoryView.as_view(), name = 'recipe-by-category'),
    path('recipes/ingredient/<str:ingredient>/', RecipesByIngredientView.as_view(), name="recipe-by-ingredient"),
    path('recipes/filter/', RecipeByMultipleIngredientView.as_view(), name='recipe-filter'),

]