import { defineStore } from "pinia";

import { apiFetch, apiGet } from "../api/client";

type AuthStatus = "idle" | "loading" | "ready" | "error";

type MeResponse = {
  authenticated: boolean;
  user_id?: string | null;
  roles?: string[];
};

type CsrfResponse = {
  csrf_token: string;
};

const ROLE_RANK: Record<string, number> = {
  student: 0,
  teacher: 1,
  admin: 2
};

function hasAtLeastRole(params: { actualRoles: string[]; minRole: string }): boolean {
  const min = ROLE_RANK[params.minRole] ?? 999;
  const best = Math.max(...params.actualRoles.map((r) => ROLE_RANK[r] ?? -1), -1);
  return best >= min;
}

type AuthState = {
  authenticated: boolean;
  userId: string | null;
  roles: string[];
  csrfToken: string | null;
  bootstrapped: boolean;
  status: AuthStatus;
  error: string | null;
};

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    authenticated: false,
    userId: null,
    roles: [],
    csrfToken: null,
    bootstrapped: false,
    status: "idle",
    error: null
  }),
  getters: {
    isAuthenticated: (state) => state.authenticated,
    isTeacher: (state) => state.roles.includes("teacher") || state.roles.includes("admin"),
    isAdmin: (state) => state.roles.includes("admin"),
    hasAtLeastRole: (state) => {
      return (minRole: string): boolean => hasAtLeastRole({ actualRoles: state.roles, minRole });
    }
  },
  actions: {
    clear(): void {
      this.authenticated = false;
      this.userId = null;
      this.roles = [];
      this.csrfToken = null;
      this.status = "ready";
      this.error = null;
      this.bootstrapped = true;
    },
    async bootstrap(): Promise<void> {
      if (this.bootstrapped) return;
      this.status = "loading";
      this.error = null;

      try {
        const payload = await apiGet<MeResponse>("/api/v1/auth/me");
        if (!payload.authenticated) {
          this.clear();
          return;
        }

        this.authenticated = true;
        this.userId = payload.user_id ?? null;
        this.roles = payload.roles ?? [];
        this.bootstrapped = true;
        this.status = "ready";
        this.error = null;

        await this.ensureCsrfToken();
      } catch (error: unknown) {
        // I dev kan Identity/Portal-auth vara avstängt eller otillgängligt.
        // För att inte förstöra elev-/publikupplevelsen faller vi tillbaka till “utloggad”.
        this.clear();
      }
    },
    async ensureCsrfToken(): Promise<string | null> {
      if (this.csrfToken) return this.csrfToken;

      try {
        const payload = await apiGet<CsrfResponse>("/api/v1/auth/csrf");
        this.csrfToken = payload.csrf_token;
        return this.csrfToken;
      } catch {
        return null;
      }
    },
    async login(params: { email: string; password: string }): Promise<void> {
      this.status = "loading";
      this.error = null;

      try {
        await apiFetch("/api/v1/auth/login", {
          method: "POST",
          body: { email: params.email, password: params.password }
        });
        this.bootstrapped = false;
        await this.bootstrap();
      } catch (error: unknown) {
        this.status = "error";
        this.error = error instanceof Error ? error.message : "Inloggningen misslyckades.";
        throw error;
      }
    },
    async logout(): Promise<void> {
      await this.ensureCsrfToken();
      await apiFetch("/api/v1/auth/logout", { method: "POST" });
      this.bootstrapped = false;
      await this.bootstrap();
    }
  }
});
