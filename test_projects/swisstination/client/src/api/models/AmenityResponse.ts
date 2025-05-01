export type AmenityResponse = {
  id: string;
  lat: string;
  lon: string;
  amenity: string;

  // Optional fields as OSM data is not always complete
  name?: string;
  operator?: string;
  brand?: string;

  url?: string;
  website?: string;

  "addr:street"?: string;
  "addr:housenumber"?: string;
  "addr:postcode"?: string;
  "addr:city"?: string;

  // additional unknown fields
  [key: string]: string | undefined;
};
