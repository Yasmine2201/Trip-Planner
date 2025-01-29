import type {Image} from "~/types/core";

export type Visit = {
  visit_id: number;
  name: string;
  start_date: string;
  end_date: string;
  location: Location;
  trip_id: number;
}

export type VisitParticipation = {
    visit_participation_id: number;
    visit: number;
    user: string;
    status: string;
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
