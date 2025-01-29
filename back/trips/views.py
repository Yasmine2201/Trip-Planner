from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView
from core.models import User
from trips.models import Trip, TripInvitation
from trips.serializers import TripSerializer, TripInvitationSerializer
from trips.services import TripService, TripInvitationService
from utils import NOT_FOUND_ERROR, ForbiddenActionError, INVALID_BODY_ERROR


class TripView(ProtectableAPIView):

    @staticmethod
    def get(request: Request, trip_id: int = None):
        """
        Fetch all trips or a specific trip associated with a user.
        If a trip_id is provided, it fetches that specific trip.
        Otherwise, it fetches all trips for the user.
        """
        if trip_id is None:
            return TripView._get_all_trips(request)
        else:
            return TripView._get_trip_by_id(request, trip_id)

    @staticmethod
    def _get_trip_by_id(request: Request, trip_id: int) -> Response:
        try:
            trip = TripService.get_user_trip_by_id(request.user, trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=200)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def _get_all_trips(request: Request) -> Response:
        trips = TripService.get_all_user_trips(request.user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=200)

    @staticmethod
    def post(request):
        """
        Create a new trip and trip participation for a user.
        """
        try:
            trip = TripService.create_user_trip(request.user, request.data)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, status=400)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def put(request, trip_id):
        """
        Update a specific trip associated with a user.
        """
        try:
            trip = TripService.update_user_trip(request.user, request.data, trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=200)
        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, status=400)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def delete(request: Request, trip_id: int):
        """
        Delete a specific trip associated with a user.
        """
        try:
            TripService.delete_user_trip(request.user, trip_id)
            return Response(status=204)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)


class LastTripView(ProtectableAPIView):

    @staticmethod
    def get(request):
        """
        Fetch the last trip associated with a user.
        """
        trip = TripService.get_last_user_trip(request.user)
        serializer = TripSerializer(trip)
        return Response(serializer.data)


class LeaveTripView(ProtectableAPIView):

    @staticmethod
    def post(request: Request, trip_id: int):
        try:
            TripService.leave_trip(request.user, trip_id)
            return Response(status=204)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class TripSentInvitation(ProtectableAPIView):

    @staticmethod
    def __get_all_trip_invitations(request, trip_id):
        try:
            trip_invitations = TripInvitationService.get_sent_trip_invitations(request.user, trip_id)
            serializer = TripInvitationSerializer(trip_invitations, many=True)
            return Response(serializer.data, status=200)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def __get_trip_invitation_by_id(request, trip_id, invitation_id):
        try:
            trip_invitation = TripInvitationService.get_sent_trip_invitations_by_id(request.user, trip_id,
                                                                                    invitation_id)
            serializer = TripInvitationSerializer(trip_invitation)
            return Response(serializer.data, status=200)
        except TripInvitation.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="TripInvitation")}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def get(request, trip_id, invitation_id=None):
        """
        Fetch all trip invitations sent by a user for a trip.
        If an invitation_id is provided, it fetches that specific invitation.
        Otherwise, it fetches all invitations for the trip.
        """
        if invitation_id is None:
            return TripSentInvitation.__get_all_trip_invitations(request, trip_id)
        else:
            return TripSentInvitation.__get_trip_invitation_by_id(request, trip_id, invitation_id)

    @staticmethod
    def post(request, trip_id: int):
        """
        Create a new trip invitation.
        """
        try:
            receiver_alias = request.GET.get('alias', None)
            trip_invitation = TripInvitationService.create_trip_invitation(request.user, receiver_alias, trip_id)
            serializer = TripInvitationSerializer(trip_invitation)
            return Response(serializer.data, status=201)

        #  if user is not the owner of the trip
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

        # if receiver is not found
        except User.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="User")}, status=404)

        # if receiver is already participating in the trip
        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, status=400)

        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)

    @staticmethod
    def delete(request, trip_id, invitation_id):
        """
        Delete a specific trip invitation.
        """
        try:
            TripInvitationService.delete_trip_invitation(request.user, trip_id, invitation_id)
            return Response(status=204)
        except TripInvitation.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="TripInvitation")}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class TripReceivedInvitation(ProtectableAPIView):

    @staticmethod
    def get(request, invitation_id=None):
        """
        Fetch all trip invitations received by a user.
        """
        if invitation_id is None:
            trip_invitations = TripInvitationService.get_received_trip_invitations(request.user)
            if trip_invitations is None:
                return Response({"error": NOT_FOUND_ERROR.format(Model="TripInvitation")}, status=404)

            serializer = TripInvitationSerializer(trip_invitations, many=True)
            return Response(serializer.data, status=200)

        else:
            try:
                trip_invitation = TripInvitationService.get_received_trip_invitations_by_id(request.user, invitation_id)
                serializer = TripInvitationSerializer(trip_invitation)
                return Response(serializer.data, status=200)

            except TripInvitation.DoesNotExist:
                return Response({"error": NOT_FOUND_ERROR.format(Model="TripInvitation")}, status=404)
            except ValueError as e:
                return Response({"error": str(e)}, status=400)

    @staticmethod
    def put(request, invitation_id):
        """
        Accept or decline a trip invitation.
        """
        status = request.data.get('status', None)  # boolean
        if status is None:
            return Response({"error": INVALID_BODY_ERROR}, status=400)

        try:
            if status:  # accept
                trip_invitation = TripInvitationService.accept_trip_invitation(request.user, invitation_id)
            else:  # decline
                trip_invitation = TripInvitationService.decline_trip_invitation(request.user, invitation_id)

            serializer = TripInvitationSerializer(trip_invitation)
            return Response(serializer.data, status=200)

        except TripInvitation.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="TripInvitation")}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
