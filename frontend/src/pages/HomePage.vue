<template>
  <main class="page">
    <header class="header">
      <h1>Projektveckor</h1>
      <p class="sub">Portalen på hule.education — dokument och resurser hostas här.</p>
    </header>

    <section class="panel">
      <h2>Aktuellt</h2>
      <ul>
        <li>
          <RouterLink to="/fn-rollspel/v43">FN-rollspel — v.43 (HT25)</RouterLink>
          <span class="meta">— portalsida</span>
        </li>
        <li>
          <RouterLink to="/fn-rollspel/v43/schema">Schema v.43 (HT25)</RouterLink>
          <span class="meta">— förhandsvisning</span>
        </li>
        <li>
          <RouterLink to="/fn-rollspel/v43/bokningsinfo">Bokningsinfo externa aktörer</RouterLink>
          <span class="meta">— förhandsvisning</span>
        </li>
      </ul>
    </section>

    <footer class="footer">
      <a href="/healthz" target="_blank" rel="noopener">Driftstatus</a>
      <span class="footer-sep">·</span>
      <RouterLink v-if="!auth.isAuthenticated" to="/login">Logga in</RouterLink>
      <button v-else class="linklike" type="button" @click="onLogout">Logga ut</button>
    </footer>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from "vue";

import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();

onMounted(async () => {
  await auth.bootstrap();
});

async function onLogout(): Promise<void> {
  await auth.logout();
}
</script>

<style scoped>
.linklike {
  border: 0;
  padding: 0;
  background: transparent;
  color: var(--accent);
  font: inherit;
  cursor: pointer;
  text-decoration: underline;
}
</style>
