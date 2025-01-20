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
}
