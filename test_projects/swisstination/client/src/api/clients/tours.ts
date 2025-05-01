import {
  TourListResponse,
  TourListFilters,
  TourCreateRequest,
  TourGetResponse,
  TourVoteResponse
} from "../models";
import { BaseClient } from "./base";

export class ToursClient extends BaseClient {
  async listTours(filters: TourListFilters) {
    const params = [];

    if (filters.sort) {
      params.push(`sort=${filters.sort}`);
    }
    if (filters.order) {
      params.push(`order=${filters.order}`);
    }
    if (filters.tags) {
      params.push(`tags=${filters.tags.join(",")}`);
    }
    if (filters.search) {
      params.push(`search=${filters.search}`);
    }

    const res = await this.request<TourListResponse[]>(
      "GET",
      `/tours?${params.join("&")}`
    );
    return res!.result!;
  }

  async createTour(data: TourCreateRequest) {
    await this.request("POST", "/tours", data);
  }

  async getTour(id: string) {
    const res = await this.request<TourGetResponse>("GET", `/tours/${id}`);
    return res!.result!;
  }

  async likeTour(id: string) {
    const res = await this.request<TourVoteResponse>(
      "POST",
      `/tours/${id}/like`
    );
    return res!.result!;
  }

  async dislikeTour(id: string) {
    const res = await this.request<TourVoteResponse>(
      "DELETE",
      `/tours/${id}/like`
    );
    return res!.result!;
  }

  async getTourTags() {
    const res = await this.request<string[]>("GET", "/tours/tags");
    return res!.result!;
  }
}
