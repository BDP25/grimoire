import { Actions, atom, Atom } from "xoid";
import { UserProfile } from "../api/models";
import { client } from "../api/client";
import { router } from "../framework";

export type AppState = {
  currentUser: UserProfile | undefined;
};

export type AppActions = {
  logout: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  isLoggedIn: () => boolean;
  restoreSession: () => Promise<void>;
};

export function appFactory() {
  const app = atom<AppState, AppActions>(
    {
      currentUser: undefined,
    },
    (state) => ({
      async logout() {
        await client.users.logout();
        state.focus((s) => s.currentUser).set(undefined);
      },
      async login(email, password) {
        await client.users.login({
          email,
          password,
        });
        const currentUser = await client.users.getCurrentUser();
        state.focus((s) => s.currentUser).set(currentUser);
        router.actions.navigateTo("/me");
      },
      isLoggedIn() {
        return state.value.currentUser !== undefined;
      },
      async restoreSession() {
        let currentUser = undefined;
        try {
          currentUser = await client.users.getCurrentUser();
        } catch (ex) {
          console.log("Failed to restore session!");
        }
        if (state.value.currentUser !== currentUser) {
          state.focus((s) => s.currentUser).set(currentUser);
        }
      },
    })
  );

  // Restore existing sessions
  app.actions.restoreSession();

  return app;
}

export const app = appFactory();
