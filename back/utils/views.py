# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.serializers import CategorySerializer, LocationSerializer
from utils.services import CategoryService, LocationService


class CategoryView(APIView):

    @staticmethod
    def post(request):
        """
        Create a new category.
        """
        name = request.data['name']
        category = CategoryService.create_category(name)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=200)

    @staticmethod
    def get(request):
        """
        Get all categories.
        """
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)

class LocationView(APIView):
    @staticmethod
    def post(request):
        """
        Create a new location.
        """
        location = LocationService.create_location(request.data)
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=200)


    @staticmethod
    def get(request):
        """
        Get all locations.
        """
        locations = LocationService.get_all_locations()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=200)
