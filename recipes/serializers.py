from django.forms import ValidationError
from rest_framework import serializers
from .models import Recipe, Rating
from django.contrib.auth import get_user_model


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        if 'username' not in data or not data['username']:
            raise serializers.ValidationError({'username': 'This field is required.' })
        if 'email' not in data or not data['email']:
            raise serializers.ValidationError({'email': 'This field is required.'})
        if 'password' not in data or not data['password']:
            raise serializers.ValidationError({'password': 'This field is required.'})
        return data
        

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user

class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id', 'created_date', 'user']

    def validate(self, data):
        
        required_fields = ['title', 'ingredients', 'instructions']

        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field : 'This field is required.'})
        return data

        # if not data.get('title'):
        #     raise serializers.ValidationError("Title is required")
        # if not data.get('ingredients'):
        #     raise serializers.ValidationError("Ingredients are required")
        # if not data.get('instructions'):
        #     raise serializers.ValidationError("Instructions are required")
        # return data

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['user', 'viewd_at']