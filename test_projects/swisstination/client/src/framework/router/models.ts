import { Actions, Atom } from "xoid";

export type Route = {
  href: string;
  html: string;
};

export type RouterState = {
  activePath: string;
  activeRoute: Route;
  params: Record<string, string | undefined>;
  routes: Route[];
  fallback?: string;
};

export type RouterActions = {
  navigateTo: (path: string) => void;
  setActiveRoute: (
    path: string,
    nextActiveRoute: Route,
    params: Record<string, string | undefined>
  ) => void;
};

export type Router = Atom<RouterState> & Actions<RouterActions>;
