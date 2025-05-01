import { AmenityResponse } from "./AmenityResponse";

export type Destination = {
  amenityId: string;
  amenity: AmenityResponse;
  title: string;
  description: string;
};

export type TourGetResponse = {
  _id: string;
  id: number;
  title: string;
  description: string;
  duration: number;
  likes: number;
  creatorId: string | null;
  tags: string[];
  destination: Destination[];
};
