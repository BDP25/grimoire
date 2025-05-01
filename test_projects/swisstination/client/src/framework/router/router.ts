import { atom } from "xoid";
import { Route, Router, RouterActions, RouterState } from "./models";
import { matchRoute } from "./matcher";

// Router singelton
export let router: Router;

export type CreateRouterConfig = {
  initalHref?: string;
  routes: Route[];
  fallback?: string;
};

export function createRouter({
  routes,
  fallback,
  initalHref = "/",
}: CreateRouterConfig) {
  if (router) throw new Error("Router has already been initalized");

  // Init active route
  const initialPath =
    window.location.pathname === "/" ? initalHref : window.location.pathname;
  const { route: initialRoute, params: initialParams } = matchRoute(
    initialPath,
    routes,
    fallback
  );
  history.replaceState({}, "", initialPath);

  router = atom<RouterState, RouterActions>(
    {
      activePath: initialPath,
      activeRoute: initialRoute,
      params: initialParams,
      routes,
      fallback,
    },
    (state) => ({
      navigateTo(path) {
        const { route, params } = matchRoute(path, routes, fallback);
        this.setActiveRoute(path, route, params);
      },
      setActiveRoute(path, nextActiveRoute, params = {}) {
        state.focus((s) => s.activePath).set(path);
        state.focus((s) => s.activeRoute).set(nextActiveRoute);
        state.focus((s) => s.params).set(params);
      },
    })
  );

  // Subscribe to activeRoute changes to update history
  router.subscribe((state, previousState) => {
    if (state.activePath != previousState.activePath) {
      history.pushState({}, "", state.activePath);
    }
  });

  // Listen to external navigation change (back, forward button)
  window.addEventListener("popstate", () => {
    const path = window.location.pathname;
    const { route, params } = matchRoute(
      path,
      router.value.routes,
      router.value.fallback
    );
    router.actions.setActiveRoute(path, route, params);
  });

  return router;
}
