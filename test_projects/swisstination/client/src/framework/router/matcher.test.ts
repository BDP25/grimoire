import { expect, test } from "vitest";
import { defaultFallback, matchRoute } from "./matcher";

// Example routes
const routes = [
  { href: "/home", html: "" },
  { href: "/optional/:id", html: "" },
  { href: "/required/!id", html: "" },
  { href: "/both/:category/!id", html: "" },
];

test("should match the home route with no parameters", () => {
  const result = matchRoute("/home", routes);
  expect(result).toEqual({
    route: { href: "/home", html: "" },
    params: {},
  });
});

test("should match home route with a slash suffix", () => {
  const result = matchRoute("/home/", routes);
  expect(result).toEqual({
    route: { href: "/home", html: "" },
    params: {},
  });
});

test("should match the optional parameter route with the parameter", () => {
  const withParam = matchRoute("/optional/123", routes);
  expect(withParam).toEqual({
    route: { href: "/optional/:id", html: "" },
    params: { id: "123" },
  });
});

test("should match the optional parameter route without the parameter", () => {
  const withoutParam = matchRoute("/optional", routes);
  expect(withoutParam).toEqual({
    route: { href: "/optional/:id", html: "" },
    params: {},
  });
});

test("should match the required parameter route when parameter is provided", () => {
  const withParam = matchRoute("/required/456", routes);
  expect(withParam).toEqual({
    route: { href: "/required/!id", html: "" },
    params: { id: "456" },
  });
});

test("should not match the required parameter without the parameter", () => {
  const withoutParam = matchRoute("/required", routes);
  expect(withoutParam).toEqual(defaultFallback);
});

test("should match the route with both optional and required parameters", () => {
  const bothParams = matchRoute("/both/adventure/789", routes);
  expect(bothParams).toEqual({
    route: { href: "/both/:category/!id", html: "" },
    params: { category: "adventure", id: "789" },
  });
});

test("should not match the parameter when the required param is not provided", () => {
  const missingRequired = matchRoute("/both/adventure", routes);
  expect(missingRequired).toEqual(defaultFallback);
});

test("should match the parameter if the optional param is provided", () => {
  const missingOptional = matchRoute("/both//789", routes);
  expect(missingOptional).toEqual({
    route: { href: "/both/:category/!id", html: "" },
    params: { category: undefined, id: "789" },
  });
});
