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
        try:
            visit = VisitService.create_visit(user_id, trip_id, visit_data)
            serializer = VisitSerializerInput(visit)

            return Response(serializer.data, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def get(request, trip_id):
        """
        Get all visits for a trip.
        """

        visits = VisitService.get_all_visits(trip_id)
        if visits is None:
            return Response({"error": "No visits found"}, status=404)

        serializer = VisitSerializerInput(visits, many=True)
        return Response(serializer.data, status=200)
