from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from trips.models import Trip
from trips.serializers import TripSerializer


# Create your views here.

from rest_framework.viewsets import ModelViewSet
from .models import Trip
from .serializers import TripSerializer

class TripViewSet(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @action(detail=False, methods=['get'], url_path='last', url_name='get_last_trip')
    def get_last_trip(self, request):
        """Retrieve the last trip added to the database."""
        last_trip = Trip.objects.all().order_by('-id').first()

        if not last_trip:
            return Response({"error": "No trips found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(last_trip)
        return Response(serializer.data, status=status.HTTP_200_OK)
