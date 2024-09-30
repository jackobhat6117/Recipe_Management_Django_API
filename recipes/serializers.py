from rest_framework import serializers
from .models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'created_date', 'author']

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title is required")
        if not data.get('ingredients'):
            raise serializers.ValidationError("Ingredients are required")
        if not data.get('instructions'):
            raise serializers.ValidationError("Instructions are required")
        return data