def render_preview_index(items: str) -> str:
    return f"""<!doctype html>
<html lang="sv">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Dokument</title>
    <style>
      :root {{
        --max: 920px;
        --fg: #111827;
        --muted: #6b7280;
        --bg: #ffffff;
        --panel: #f8fafc;
        --border: #e5e7eb;
        --link: #2563eb;
      }}
      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: var(--fg);
        background: var(--bg);
      }}
      header {{
        border-bottom: 1px solid var(--border);
        background: var(--panel);
      }}
      .wrap {{ max-width: var(--max); margin: 0 auto; padding: 16px; }}
      .crumbs {{ font-size: 14px; color: var(--muted); }}
      .crumbs a {{ color: var(--link); text-decoration: none; }}
      h1 {{ margin: 8px 0 0; font-size: 28px; }}
      main .wrap {{ padding: 24px 16px 48px; }}
      a {{ color: var(--link); }}
      .meta {{ color: var(--muted); font-size: 14px; }}
    </style>
  </head>
  <body>
    <header>
      <div class="wrap">
        <div class="crumbs">
          <a href="/">Projektveckor</a> / <span>Dokument</span>
        </div>
        <h1>Dokument</h1>
      </div>
    </header>
    <main>
      <div class="wrap">
        <h2>Översikt</h2>
        <p>Här är dokument som portalen hostar.</p>
        <ul>
          {items if items else '<li>Inga dokument ännu.</li>'}
        </ul>
      </div>
    </main>
  </body>
</html>
"""
