import base64
from rest_framework import viewsets, permissions
from .models import Med
from .serializers import MedSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class MedViewSet(viewsets.ModelViewSet):
    queryset = Med.objects.all()
    serializer_class = MedSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [permissions.AllowAny()]  # Public access
        return [permissions.IsAdminUser()]  # Restrict other methods to admins

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow public access to login API

    def post(self, request, *args, **kwargs):
        # Retrieve Authorization header
        auth = request.headers.get('Authorization')

        if not auth:
            return Response({"detail": "Authorization header is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract the type and credentials
            auth_type, auth_credentials = auth.split(' ', 1)
            if auth_type.lower() != 'basic':
                return Response({"detail": "Invalid authentication type"}, status=status.HTTP_400_BAD_REQUEST)

            # Decode the base64 encoded username and password
            decoded_credentials = base64.b64decode(auth_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
        except (ValueError, TypeError, base64.binascii.Error):
            return Response({"detail": "Invalid Authorization header format"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)