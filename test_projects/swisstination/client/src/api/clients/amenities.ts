import { BaseClient } from "./base";
import { AmenityLabelFilters, AmenityResponse } from "../models";

export class AmenitiesClient extends BaseClient {
  async getAmenity(id: string) {
    const res = await this.request<AmenityResponse>("GET", `/amenities/${id}`);
    return res!.result!;
  }

  async getAmenityLabels(filters: AmenityLabelFilters) {
    const params = [];

    if (filters.order) {
      params.push(`order=${filters.order}`);
    }
    if (filters.search) {
      params.push(`search=${filters.search}`);
    }
    if (filters.limit) {
      params.push(`limit=${filters.limit}`);
    }

    const res = await this.request<string[]>(
      "GET",
      `/amenities?${params.join("&")}`
    );
    return res!.result!;
  }
}
