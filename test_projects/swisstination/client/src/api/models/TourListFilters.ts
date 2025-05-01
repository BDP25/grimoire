export type Sort = "likes" | "duration" | "title";
export type Order = "asc" | "desc";

export type TourListFilters = {
  sort?: Sort;
  order?: Order;
  tags?: string[];
  search?: string;
};
