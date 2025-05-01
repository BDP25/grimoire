import { Destination } from "./TourGetResponse";

export type TourCreateRequest = {
  title: string;
  description: string;
  duration: number;
  tags: string[];
  destinations: Destination[];
};
