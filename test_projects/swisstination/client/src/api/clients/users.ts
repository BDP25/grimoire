import {
  UserSignupRequest,
  UserLoginRequest,
  UserProfileResponse,
  UserProfileMeResponse,
  UserUpdateRequest,
  UserProfile,
} from "../models";
import { BaseClient } from "./base.ts";

export class UsersClient extends BaseClient {
  async signup(data: UserSignupRequest) {
    await this.request("POST", "/users/signup", data);
  }

  async login(data: UserLoginRequest) {
    await this.request("POST", "/users/login", data);
  }

  async logout() {
    return this.request("POST", "/users/logout");
  }

  async getUserById(id: string) {
    const res = await this.request<UserProfileResponse>("GET", `/users/${id}`);
    return res!.result!;
  }

  async getCurrentUser() {
    const res = await this.request<UserProfileMeResponse>("GET", "/users/me");
    return res!.result!;
  }

  async updateCurrentUser(data: UserUpdateRequest) {
    await this.request<any>("PATCH", "/users/me", data);
  }

  getAvatarURI(user: UserProfile) {
    return `${this.baseUrl}/users/${user.username}/avatar`;
  }
}
