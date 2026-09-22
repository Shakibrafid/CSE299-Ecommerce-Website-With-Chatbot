from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from backend.permissions import IsOwnerOrStaff
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import ProfileSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    '''ModelViewSet: By using this, Django automatically 
    creates 5 endpoints for you: listing profiles, viewing a 
    single profile, creating one, updating one, and deleting one.'''
    queryset = Profile.objects.all()
    '''queryset = Profile.objects.all(): This tells the view: 
    "When you need to look at the database, use the Profile table."
    '''
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrStaff()]


class RegisterAPIView(APIView):
    '''Simple registration endpoint for frontend use.

    Expects JSON: { username, email, password, phone }
    Returns 201 with basic user info on success.
    '''
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username') or data.get('email')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        if not username or not email or not password:
            return Response({'detail': 'username, email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'detail': 'User with that username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        if phone:
            user.phone = phone
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'access': access_token,
                'refresh': refresh_token,
            },
            status=status.HTTP_201_CREATED,
        )