from django.core.paginator import Paginator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import ProtectableAPIView
from trips.models import Trip
from utils import ForbiddenActionError
from visits.models import Location, Visit
from visits.serializers import LocationSerializer, VisitSerializer
from visits.services import VisitService, LocationService


# Create your views here.
class VisitView(ProtectableAPIView):

    @staticmethod
    def post(request: Request, trip_id: int):
        """
        Create a new visit for a trip.
        """
        visit_data = request.data
        try:
            visit = VisitService.create_visit(request.user, trip_id, visit_data)
            serializer = VisitSerializer(visit)

            return Response(serializer.data, status=200)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=404)

        except ForbiddenActionError as e:
            return Response({"error": str(e)}, status=403)

    @staticmethod
    def __get_visit_by_id(request: Request, trip_id: int, visit_id: int) -> Response:
        try:
            visit = VisitService.get_visit_by_id(request.user, trip_id, visit_id)
            serializer = VisitSerializer(visit)
            return Response(serializer.data, status=200)
        except Visit.DoesNotExist:
            return Response({"error": "Visit not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except ForbiddenActionError as e:
            return Response({"error": str(e)}, status=403)

    @staticmethod
    def __get_all_visits(request: Request, trip_id: int) -> Response:
        try:
            visits = VisitService.get_all_visits(request.user, trip_id)
            if visits is None:
                return Response({"error": "No visits found"}, status=404)

            serializer = VisitSerializer(visits, many=True)
            return Response(serializer.data, status=200)

        except Trip.DoesNotExist:
            return Response({"error": "Trip not found"}, status=404)

        except ForbiddenActionError as e:
            return Response({"error": str(e)}, status=403)

    @staticmethod
    def get(request: Request, trip_id: int, visit_id: int = None) -> Response:
        if visit_id is not None:
            return VisitView.__get_visit_by_id(request, trip_id, visit_id)
        else:
            return VisitView.__get_all_visits(request, trip_id)

    @staticmethod
    def put(request: Request, trip_id: int, visit_id: int) -> Response:
        """
        Update a visit.
        """
        try:
            visit = VisitService.update_visit(request.user, trip_id, visit_id, request.data)
            serializer = VisitSerializer(visit)
            return Response(serializer.data, status=200)

        except Visit.DoesNotExist:
            return Response({"error": "Visit not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except ForbiddenActionError as e:
            return Response({"error": str(e)}, status=403)

    @staticmethod
    def delete(request: Request, trip_id: int, visit_id: int) -> Response:
        """
        Delete a visit.
        """
        try:
            visit = VisitService.delete_visit(request.user, trip_id, visit_id)
            serializer = VisitSerializer(visit)
            return Response(serializer.data, status=200)

        except Visit.DoesNotExist:
            return Response({"error": "Visit not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except ForbiddenActionError as e:
            return Response({"error": str(e)}, status=403)


class LocationView(APIView):
    DEFAULT_PAGE_SIZE = 10

    @staticmethod
    def get(request: Request) -> Response:
        """
        Get locations.
        """

        params = {k: v for k, v in request.query_params.items()}
        page_index: int = params.get('page', 1)
        page_size: int = params.get('pageSize', LocationView.DEFAULT_PAGE_SIZE)
        if 'page' in params:
            del params['page']
        if 'pageSize' in params:
            del params['pageSize']

        if len(request.query_params) > 0:
            locations = LocationService.get_filtered_locations(request.query_params)
        else:
            locations = LocationService.get_all_locations()

        page = Paginator(locations, page_size)

        serializer = LocationSerializer(page.get_page(page_index), many=True)
        response = {
            "data": serializer.data,
            "current_page": page_index,
            "total_pages": page.num_pages,
            "total_elements": page.count,
            "elements_per_page": page_size
        }
        return Response(response, status=200)
