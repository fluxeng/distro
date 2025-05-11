from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, AssetType, Asset, Issue
from .serializers import UserProfileSerializer, AssetTypeSerializer, AssetSerializer, IssueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class AssetTypeViewSet(viewsets.ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAuthenticated]

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

class HealthCheckView(APIView):
    permission_classes = []
    def get(self, request):
        return Response({"status": "healthy"})