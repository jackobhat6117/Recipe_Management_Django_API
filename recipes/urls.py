from django.urls import path
from .views import HighestRatedRecipesView, MostPopularRecipesView, RecipeListCreateView, RecipeDetailView, UserCreateView, UserDetailView, RecipesByCategoryView, RecipesByIngredientView,RatingCreateView, RecipeFilter, RatingCreateView

urlpatterns = [
    path("user/", UserCreateView.as_view(), name = 'user-create' ),
    path("user/<int:pk>/", UserDetailView.as_view(), name = 'user-detail'),
    path("recipes/", RecipeListCreateView.as_view(), name = 'recipe-list-create'),
    path("recipes/<int:pk>/", RecipeDetailView.as_view(), name = 'recipe-detail'),
    path('recipes/category/<str:category>/', RecipesByCategoryView.as_view(), name='recipe-by-category'),
    path('recipes/ingredient/<str:ingredient>/', RecipesByIngredientView.as_view(), name="recipe-by-ingredient"),
    path('recipes/filter/', RecipeFilter.as_view(), name='recipe-filter'),
    path('recipes/<int:recipe_id>/rate/', RatingCreateView.as_view(), name='rate-recipe'),
    path('recipes/highest-rated/', HighestRatedRecipesView.as_view(), name='highest-rated-recipes'),
    path('recipes/most-popular/', MostPopularRecipesView.as_view(), name='most-popular-recipes'),
]