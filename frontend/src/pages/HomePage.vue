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
    </footer>
  </main>
</template>

<script setup lang="ts"></script>
