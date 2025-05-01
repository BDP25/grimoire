import { Route } from "./models";

export const defaultFallback = {
  route: {
    href: "/404",
    html: "<h1>Not found!</h1>",
  },
  params: {},
};

export function matchRoute(
  path: string,
  routes: Route[],
  fallback?: string
): { route: Route; params: Record<string, string | undefined> } {
  for (const route of routes) {
    const match = matchPath(path, route.href);
    if (match) {
      return { route, params: match.params };
    }
  }

  if (fallback) {
    const fallbackRoute = routes.find((r) => r.href === fallback);
    if (!fallbackRoute) throw new Error("Did not found given fallback route!");
  }

  return defaultFallback;
}

const optionalRegex = /:([^\s/]+)/g;
const requiredRegex = /!([^\s/]+)/g;

function matchPath(path: string, routePattern: string) {
  let pattern = routePattern
    .replace(optionalRegex, "([^/]+)?")
    .replace(requiredRegex, "([^/]+)")
    .replace(/\//g, "\\/");
  pattern += "\\/?";

  // Normalize path to allways end with a slash
  if (path.slice(-1) != "/") path += "/";

  const regex = new RegExp(`^${pattern}$`);
  const match = path.match(regex);

  if (!match) return null;

  // Extract keys and params
  const optionalKeys = [...routePattern.matchAll(optionalRegex)].map(
    (m) => m[1]
  );
  const requiredKeys = [...routePattern.matchAll(requiredRegex)].map(
    (m) => m[1]
  );

  const params: Record<string, string | undefined> = {};
  [...optionalKeys, ...requiredKeys].forEach((key, index) => {
    params[key] = match[index + 1] || undefined;
  });

  // Ensure required params are present
  for (const key of requiredKeys) {
    if (!params[key]) return null;
  }

  return { params };
}
