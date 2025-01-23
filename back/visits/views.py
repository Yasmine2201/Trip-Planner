from rest_framework.request import Request
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView
from trips.models import Trip
from utils import ForbiddenActionError
from visits.models import Location
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
    def get(request: Request, trip_id: int) -> Response:
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


class LocationView(ProtectableAPIView):

    @staticmethod
    def get(request: Request) -> Response:
        """
        Get locations.
        """

        params = {k: v for k, v in request.query_params.items()}
        page: int = params.get('page', 1)
        if 'page' in params:
            del params['page']

        if len(request.query_params) > 0:
            locations = LocationService.get_filtered_locations(request.query_params, page)
        else:
            locations = LocationService.get_all_locations(page)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=200)
