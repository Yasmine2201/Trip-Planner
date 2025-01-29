import type {Image, User} from "~/types/core";

export type Trip = {
  trip_id: number;
  trip_name: string;
  start_date: string;
  end_date: string;
  latitude: number;
  longitude: number;
  radius: number;
  image: Image | null;
}

export type TripInvitation = {
    tripInvitationId: number;
    trip: Trip;
    user: User;
    status: string;
    url: string;
}