from django.db import models
from django.conf import settings


class Recipe(models.Model):
    CATEGORY_CHOICES = [
       ('Desert', 'Desert'),
        ('Main Course', 'Main Course'),
        ('Breakfast', 'Breakfast'),
        ('vegertrian', 'vegetrian'),
        ('appetizer', 'Appetizer'),
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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipe')

    def __str__(self):
        return self.title
