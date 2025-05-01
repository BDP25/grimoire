import { ApiResponse } from "../models";

export abstract class BaseClient {
  protected baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  protected async request<T>(
    method: "GET" | "POST" | "DELETE" | "PATCH",
    endpoint: string,
    body?: any,
    headers: HeadersInit = {}
  ): Promise<ApiResponse<T> | undefined> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      body: body ? JSON.stringify(body) : null,
      credentials: "include",
    });

    await this.handleError(response);

    try {
      const result = (await response.json()) as ApiResponse<T>;
      return result;
    } catch (ex) {
      return;
    }
  }

  protected async handleError(response: Response) {
    if (response.ok) return;
    try {
      const result = await response.json();
      throw new Error(
        `API Error (${response.status}): ${result.error || response.text}`
      );
    } catch (Ex) {
      throw new Error(`Request Error (${response.status}): ${response.text}`);
    }
  }
}
