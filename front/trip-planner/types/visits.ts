import type {Image} from "~/types/core";

export type Visit = {
  visit_id: number;
  name: string;
  start_date: string;
  end_date: string;
  location: Location;
  trip_id: number;
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
  location_id: number;
  price: number;
  price_name: string;
  description?: string | null;
}
