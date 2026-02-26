<template>
  <main class="page">
    <header class="header">
      <div class="crumbs">
        <RouterLink to="/">Projektveckor</RouterLink>
        <span class="crumb-sep">/</span>
        <span>FN-rollspel v.43</span>
      </div>
      <h1>FN-rollspel — v.43 (HT25)</h1>
      <p class="sub">
        Startpunkt i portalen. Dokumenten hostas här och kan förhandsvisas direkt på sidan.
      </p>
    </header>

    <section class="panel">
      <h2>Portalen</h2>
      <nav class="tabs" aria-label="FN-rollspel v.43">
        <RouterLink class="tab" :to="{ name: 'fn-rollspel-v43' }">Börja här</RouterLink>
        <RouterLink class="tab" :to="{ name: 'fn-rollspel-v43-schema' }">Schema</RouterLink>
        <RouterLink class="tab" :to="{ name: 'fn-rollspel-v43-bokningsinfo' }">Bokningsinfo</RouterLink>
        <a class="tab tab-secondary" :href="iframeSrc" target="_blank" rel="noopener">
          Öppna portalen i ny flik
        </a>
      </nav>
      <iframe class="docframe" :src="iframeSrc" :title="iframeTitle"></iframe>
    </section>

    <section class="panel">
      <h2>Snabblänkar</h2>
      <ul>
        <li>
          <a href="/fn-rollspel/v43/portal/index.html" target="_blank" rel="noopener">
            Börja här (instruktioner för lärare)
          </a>
          <span class="meta">— HTML</span>
        </li>
        <li>
          <a href="/fn-rollspel/v43/portal/schema.html" target="_blank" rel="noopener">Schema v.43 (HT25)</a>
          <span class="meta">— HTML</span>
        </li>
        <li>
          <a href="/fn-rollspel/v43/portal/bokningsinfo.html" target="_blank" rel="noopener">
            Bokningsinfo externa aktörer
          </a>
          <span class="meta">— HTML</span>
        </li>
      </ul>
    </section>

    <footer class="footer">
      <RouterLink to="/">Till startsidan</RouterLink>
      <span class="footer-sep">·</span>
      <a href="/healthz" target="_blank" rel="noopener">Driftstatus</a>
    </footer>
  </main>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  doc: "index" | "schema" | "bokningsinfo";
}>();

const iframeSrc = computed(() => `/fn-rollspel/v43/portal/${props.doc}.html`);
const iframeTitle = computed(() => {
  if (props.doc === "schema") return "Schema v.43 (HT25) – FN-rollspel";
  if (props.doc === "bokningsinfo") return "Bokningsinfo – externa aktörer";
  return "Börja här – lärarinstruktion";
});
</script>
