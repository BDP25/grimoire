import { Route } from "./models";

export function findRouteOrFallback(
  href: string,
  routes: Route[],
  fallback: string = "<h1>Not found</h1>"
) {
  const route = routes.find((route) => route.href == href);
  if (!route)
    return {
      href: href,
      html: fallback,
    } as Route;
  return route;
}
