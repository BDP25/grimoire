export type ApiResponse<T = unknown> = {
  error?: string;
  message?: string;
  result?: T;
};
