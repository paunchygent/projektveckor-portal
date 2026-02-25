import { createRouter, createWebHistory } from "vue-router";

import FnRollspelV43Page from "./pages/FnRollspelV43Page.vue";
import HomePage from "./pages/HomePage.vue";
import NotFoundPage from "./pages/NotFoundPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomePage },
    {
      path: "/fn-rollspel/v43",
      name: "fn-rollspel-v43",
      component: FnRollspelV43Page,
      props: { doc: "index" }
    },
    {
      path: "/fn-rollspel/v43/schema",
      name: "fn-rollspel-v43-schema",
      component: FnRollspelV43Page,
      props: { doc: "schema" }
    },
    {
      path: "/fn-rollspel/v43/bokningsinfo",
      name: "fn-rollspel-v43-bokningsinfo",
      component: FnRollspelV43Page,
      props: { doc: "bokningsinfo" }
    },
    { path: "/:pathMatch(.*)*", name: "not-found", component: NotFoundPage }
  ]
});
