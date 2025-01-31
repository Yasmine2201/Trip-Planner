import type {Image, PublicUser} from "~/types/core";

export type Trip = {
  trip_id: number;
  trip_name: string;
  start_date: string;
  end_date: string;
  latitude: number;
  longitude: number;
  radius: number;
  image: Image | null;
  owner_id: string;
  members: PublicUser[];
}

export type TripInvitation = {
    tripInvitationId: number;
    trip: Trip;
    user: PublicUser;
    status: string;
    url: string;
}