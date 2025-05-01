import "./css/styles.css";
import "./components";
import "./pages";

import { createRouter, documentReady } from "./framework";

createRouter({
  initalHref: "/home",
  fallback: "/404",
  routes: [
    {
      href: "/404",
      html: "<page-layout><p>Page not found!</p></page-layout>",
    },
    {
      href: "/home",
      html: "<home-page />",
    },
    {
      href: "/about",
      html: "<about-page />",
    },
    {
      href: "/tours",
      html: "<tours-page />",
    },
    {
      href: "/tour/!id",
      html: "<tour-page />",
    },
    {
      href: "/login",
      html: "<login-page />",
    },
    {
      href: "/signup",
      html: "<signup-page />",
    },
    {
      href: "/me",
      html: "<me-page/>",
    },
    /* Test pages */
    {
      href: "/test/btn",
      html: "<test-btn-state-page />",
    },
    {
      href: "/test/routing/:id",
      html: "<test-router-state />",
    },
    {
      href: "/test/passing-data",
      html: "<test-passing-data-page />",
    },
  ],
});

function onLoad() {
  const app = document.getElementById("app")!;
  app.innerHTML = `<router-active-page></router-active-page>`;
}

documentReady(onLoad);
