from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import Todo
from rest_framework.permissions import AllowAny
from .serializers import TodoSerializer
from django.contrib.auth import get_user_model
from .tasks import send_todo_completion_email

User = get_user_model()

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        todo = self.get_object()
        todo.completed = True
        todo.save()
        send_todo_completion_email.delay(request.user.email, todo.title)
        return Response({'status':'todo completed'})
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not all([username, password, email]):
        return Response({'error': 'Username, password, and email are required'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
