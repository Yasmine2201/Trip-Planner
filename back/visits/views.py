from rest_framework.response import Response

from authentication.utils import ProtectableAPIView, TokenAuthentication
from visits.serializers import VisitSerializerInput
from visits.services import VisitService


# Create your views here.
class VisitView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, trip_id):
        """
        Create a new visit for a trip.
        """
        user_id = request.user.user_id
        visit_data = request.data
        try :
            visit = VisitService.create_visit(user_id, trip_id, visit_data)
            serializer = VisitSerializerInput(visit)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": f"An error occurred while processing the visit, Here are the details: '{e}'"}, status=400)

    @staticmethod
    def get(request, trip_id):
        """
        Get all visits for a trip.
        """
        try:
            visits = VisitService.get_all_visits(trip_id)
            serializer = VisitSerializerInput(visits, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": f"An error occurred while processing the visit, Here are the details: '{e}'"}, status=400)
