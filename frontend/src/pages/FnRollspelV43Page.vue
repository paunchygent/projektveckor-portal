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
        Startpunkt i portalen. Dokumenten ligger i SharePoint och kräver inloggning.
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
      <h2>Snabblänkar (SharePoint)</h2>
      <ul>
        <li>
          <a :href="links.startPdf" target="_blank" rel="noopener">Börja här (instruktioner för lärare)</a>
          <span class="meta">— PDF</span>
        </li>
        <li>
          <a :href="links.schemaPdf" target="_blank" rel="noopener">Schema v.43 (HT25)</a>
          <span class="meta">— PDF</span>
        </li>
        <li>
          <a :href="links.bookingFolder" target="_blank" rel="noopener">Bokningsinfo externa aktörer</a>
          <span class="meta">— SharePoint-mapp</span>
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

const links = {
  startPdf:
    "https://harrydakommun.sharepoint.com/teams/ArbetslagSA/Shared%20Documents/General/L%C3%A4s%C3%A5r%2025-26/Resursdagar%20och%20projektveckor/%C3%85k%202/v-43-f%C3%B6rberedelseveckan/B%C3%B6rja%20h%C3%A4r.%20Instruktioner%20f%C3%B6r%20l%C3%A4rare.pdf",
  schemaPdf:
    "https://harrydakommun.sharepoint.com/teams/ArbetslagSA/Shared%20Documents/General/L%C3%A4s%C3%A5r%2025-26/Resursdagar%20och%20projektveckor/%C3%85k%202/v-43-f%C3%B6rberedelseveckan/Schema%20v.%2043%20HT25.pdf",
  bookingFolder:
    "https://harrydakommun.sharepoint.com/teams/ArbetslagSA/Shared%20Documents/General/L%C3%A4s%C3%A5r%2025-26/Resursdagar%20och%20projektveckor/%C3%85k%202/v-43-f%C3%B6rberedelseveckan/05_Bokningsinfo_externa_f%C3%B6rel%C3%A4sare_etc/"
};
</script>
