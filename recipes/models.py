from django.db import models
from django.conf import settings


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Dessert', 'Dessert'),
        ('Main Course', 'Main Course'),
        ('Breakfast', 'Breakfast'),
        ('vegertrian', 'vegetrian'),
        ('appetizer', 'Appetizer'),
        ('salad', 'salad'),
        ('drink', 'Drink'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField(help_text="Enter ingredients separated by commas.")
    instructions = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipe')

    def __str__(self):
        return self.title

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user') 

    def __str__(self):
        return f'{self.user.username} rated {self.recipe.title} - {self.rating}/5'