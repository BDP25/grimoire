import { AmenitiesClient, ToursClient, UsersClient } from "./clients";

export function clientFactory(baseUrl: string) {
  return {
    amenities: new AmenitiesClient(baseUrl),
    users: new UsersClient(baseUrl),
    tours: new ToursClient(baseUrl)
  };
}

export const client = clientFactory("http://localhost:5000/api/v1");
