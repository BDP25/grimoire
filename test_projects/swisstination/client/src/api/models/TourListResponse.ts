export type TourListResponse = {
  _id: string;
  id: number;
  title: string;
  description: string;
  duration: number | string;
  likes: number;
  creatorId: number;
  tags: string[];
};
