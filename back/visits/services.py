from django.db.models import Min, Max, Q
from rest_framework.exceptions import ValidationError

from core.models import User
from trips.models import Trip
from trips.services import TripService
from utils import ForbiddenActionError, haversine
from visits.models import Visit, Location, VisitParticipation
from visits.serializers import VisitInputSerializer, LocationQueryParamsSerializer


class VisitService:

    @staticmethod
    def create_visit(user: User, trip_id: int, visit_data: dict):
        """
        Create a new visit for a user in a trip.
        """
        visit_serializer = VisitInputSerializer(data=visit_data)
        visit_serializer.is_valid(raise_exception=True)

        visit_data_object = visit_serializer.data
        trip: Trip = visit_data_object.get('trip')

        if trip.trip_id != trip_id:
            raise ValueError(f"Mismatch between trip_id in URL and trip_id in request body")

        if not TripService.check_participation(trip, user, is_owner=True):
            raise ForbiddenActionError(f"User is not part of the trip")

        visit = Visit.objects.create(**visit_data_object)

        trip_participations = TripService.get_trip_participations(trip.trip_id)

        for trip_participation in trip_participations:
            if trip_participation.user.user_id != user.user_id:
                VisitParticipation.objects.create(visit=visit, user=trip_participation.user)
            else:
                VisitParticipation.objects.create(visit=visit, user=user, status=VisitParticipation.VisitParticipationStatus.ACCEPTED)

        return visit

    @staticmethod
    def get_all_visits(user: User, trip_id: int):
        """
        Get all visits for a trip.
        """
        trip = TripService.get_user_trip_by_id(user, trip_id)

        return Visit.objects.filter(trip=trip)


class LocationService:

    @staticmethod
    def get_all_locations() -> list[Location]:
        return Location.objects.all().order_by('location_id')

    @staticmethod
    def get_filtered_locations(query_params: dict) -> list[Location]:
        params_serializer = LocationQueryParamsSerializer(data=query_params)
        params_serializer.is_valid(raise_exception=True)
        params: dict = params_serializer.data

        # Extract query parameters
        lat: float | None = params.get('lat', None)
        lon: float | None = params.get('lon', None)
        radius: float | None = params.get('radius', None)
        min_lat: float | None = params.get('min_lat')
        max_lat: float | None = params.get('max_lat')
        min_lon: float | None = params.get('min_lon')
        max_lon: float | None = params.get('max_lon')
        min_price: float | None = params.get('min_price')
        max_price: float | None = params.get('max_price')
        search: str | None = params.get('search', None)
        sort_by: str = params.get('sort_by', 'location_id')
        sort_order: str = params.get('sort_order', 'asc')
        is_viewport: bool = params.get('is_viewport', False)
        only_prices: bool = params.get('only_prices', False)

        if sort_by and sort_order:
            if sort_order == 'desc':
                sort_by = f"-{sort_by}"

        # Initialize base query
        queryset = Location.objects.all()

        # 1. Add a complex filter for partial name search
        filters = Q()
        if search:
            filters &= Q(name__icontains=search)

        # 2. Add price range filter
        if min_price and min_price > 0:
            queryset = queryset.annotate(
                min_price=Min('prices__price'),
            )
            filters &= Q(min_price__gte=min_price)

        if max_price:
            queryset = queryset.annotate(
                max_price=Max('prices__price')
            )
            filters &= Q(max_price__lte=max_price)

        if not only_prices:
            filters |= Q(prices__isnull=True)

        # 3. Add geographical filter (Haversine formula or viewport)
        if lat and lon and radius:
            try:
                valid_ids = [
                    loc.location_id for loc in queryset
                    if haversine(lat, lon, loc.latitude, loc.longitude) <= radius
                ]
                filters &= Q(location_id__in=valid_ids)
            except ValueError:
                raise ValidationError("Invalid latitude, longitude, or radius.")

        elif is_viewport:
            filters &= Q(latitude__gte=min_lat, latitude__lte=max_lat, longitude__gte=min_lon, longitude__lte=max_lon)

        # Apply filters to the queryset
        queryset = queryset.filter(filters)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset

    @staticmethod
    def get_location_by_id(location_id):
        return Location.objects.get(location_id=location_id)
