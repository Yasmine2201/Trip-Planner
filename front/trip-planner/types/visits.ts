import type {Image, PublicUser} from "~/types/core";

export type Visit = {
  visit_id: number;
  name: string;
  start_date: string;
  end_date: string;
  location: Location;
  trip_id: number;
  participations: VisitParticipation[];
}

export type VisitParticipation = {
    status: string;
    user: PublicUser;
}

export type Location = {
  location_id: number;
  name: string;
  latitude: number;
  longitude: number;
  description: string;
  prices: LocationPrice[];
  pictures: Image[];
}

export type LocationPrice = {
  price_id: number;
  price: number;
  price_name: string;
  description?: string | null;
}
