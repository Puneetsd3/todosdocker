from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title','description','completed','created_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    
    
