import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "./stores/auth";
import FnRollspelV43Page from "./pages/FnRollspelV43Page.vue";
import ForbiddenPage from "./pages/ForbiddenPage.vue";
import HomePage from "./pages/HomePage.vue";
import LoginPage from "./pages/LoginPage.vue";
import NotFoundPage from "./pages/NotFoundPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomePage },
    { path: "/login", name: "login", component: LoginPage },
    { path: "/forbidden", name: "forbidden", component: ForbiddenPage },
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

const ROLE_RANK: Record<string, number> = { student: 0, teacher: 1, admin: 2 };

function getNextParam(value: unknown): string | null {
  if (typeof value !== "string") return null;
  if (!value.startsWith("/")) return null;
  if (value.startsWith("/login")) return null;
  return value;
}

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  const requiresAuth = Boolean(to.meta.requiresAuth);
  const rawMinRole = typeof to.meta.minRole === "string" ? to.meta.minRole : null;
  const minRole = rawMinRole ? rawMinRole : null;
  const isLogin = to.path.startsWith("/login");

  if (requiresAuth || minRole || isLogin) {
    await auth.bootstrap();
  }

  if (isLogin) {
    if (auth.isAuthenticated) {
      const nextParam = getNextParam(to.query.next);
      return nextParam ? { path: nextParam } : { path: "/" };
    }
    return true;
  }

  if ((requiresAuth || minRole) && !auth.isAuthenticated) {
    return { path: "/login", query: { next: to.fullPath } };
  }

  if (minRole) {
    const actualRank = Math.max(...auth.roles.map((r) => ROLE_RANK[r] ?? -1), -1);
    const requiredRank = ROLE_RANK[minRole] ?? 999;
    if (actualRank < requiredRank) {
      return { path: "/forbidden" };
    }
  }

  return true;
});
