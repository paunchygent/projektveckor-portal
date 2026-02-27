<template>
  <main class="page">
    <header class="header">
      <div class="crumbs">
        <RouterLink to="/">Projektveckor</RouterLink>
        <span class="crumb-sep">/</span>
        <span>Logga in</span>
      </div>
      <h1>Logga in</h1>
      <p class="sub">Inloggningen används för lärarytan (redigering, export och bulletin).</p>
    </header>

    <section class="panel">
      <form class="form" @submit.prevent="onSubmit">
        <label class="field">
          <span class="label">E-post</span>
          <input v-model="email" type="email" autocomplete="username" required />
        </label>

        <label class="field">
          <span class="label">Lösenord</span>
          <input v-model="password" type="password" autocomplete="current-password" required />
        </label>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="actions">
          <button class="btn" type="submit" :disabled="busy">Logga in</button>
          <RouterLink class="btn btn-secondary" to="/">Avbryt</RouterLink>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const email = ref("");
const password = ref("");
const busy = computed(() => auth.status === "loading");
const error = computed(() => auth.error);

function getNext(): string {
  const next = route.query.next;
  if (typeof next !== "string") return "/";
  if (!next.startsWith("/")) return "/";
  if (next.startsWith("/login")) return "/";
  return next;
}

async function onSubmit(): Promise<void> {
  await auth.login({ email: email.value, password: password.value });
  await router.replace(getNext());
}
</script>

<style scoped>
.form {
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
}

.label {
  font-weight: 600;
}

input {
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: #fff;
  font: inherit;
}

.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: #fff;
  font-weight: 700;
  text-decoration: none;
  color: var(--accent);
  cursor: pointer;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-secondary {
  color: var(--muted);
}

.error {
  margin: 0;
  color: #b91c1c;
  font-weight: 600;
}
</style>

