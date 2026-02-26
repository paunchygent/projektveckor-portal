<template>
  <main class="page">
    <header class="header">
      <h1>Projektveckor</h1>
      <p class="sub">Portalen på hule.education — länkar till SharePoint-resurser.</p>
    </header>

    <section class="panel">
      <h2>Aktuellt</h2>
      <ul>
        <li>
          <RouterLink to="/fn-rollspel/v43">FN-rollspel — v.43 (HT25)</RouterLink>
          <span class="meta">— portalsida</span>
        </li>
        <li>
          <a :href="weeks.fnRollspelV43.schemaUrl" target="_blank" rel="noopener">Schema v.43 (HT25)</a>
          <span class="meta">— PDF</span>
        </li>
        <li>
          <a :href="weeks.fnRollspelV43.bookingUrl" target="_blank" rel="noopener">
            Bokningsinfo externa aktörer
          </a>
          <span class="meta">— SharePoint-mapp</span>
        </li>
      </ul>
    </section>

    <footer class="footer">
      <a href="/healthz" target="_blank" rel="noopener">Driftstatus</a>
    </footer>
  </main>
</template>

<script setup lang="ts">
const weeks = {
  fnRollspelV43: {
    schemaUrl:
      "https://harrydakommun.sharepoint.com/teams/ArbetslagSA/Shared%20Documents/General/L%C3%A4s%C3%A5r%2025-26/Resursdagar%20och%20projektveckor/%C3%85k%202/v-43-f%C3%B6rberedelseveckan/Schema%20v.%2043%20HT25.pdf",
    bookingUrl:
      "https://harrydakommun.sharepoint.com/teams/ArbetslagSA/Shared%20Documents/General/L%C3%A4s%C3%A5r%2025-26/Resursdagar%20och%20projektveckor/%C3%85k%202/v-43-f%C3%B6rberedelseveckan/05_Bokningsinfo_externa_f%C3%B6rel%C3%A4sare_etc/"
  }
};
</script>
