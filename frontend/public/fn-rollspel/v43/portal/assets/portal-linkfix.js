(() => {
  const isBlankable = (href) => {
    if (!href) return false;
    if (href.startsWith("#")) return false;
    if (href.startsWith("mailto:")) return true;
    if (href.startsWith("tel:")) return true;
    if (!href.startsWith("http://") && !href.startsWith("https://")) return false;
    try {
      const url = new URL(href, window.location.href);
      return url.origin !== window.location.origin;
    } catch {
      return false;
    }
  };

  for (const anchor of document.querySelectorAll("a[href]")) {
    const href = anchor.getAttribute("href") ?? "";
    if (!isBlankable(href)) continue;
    anchor.setAttribute("target", "_blank");
    anchor.setAttribute("rel", "noopener");
  }
})();

