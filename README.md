# ignasia Consulting — Website

Professional website for ignasia Consulting — an independent GRC, cybersecurity, and business process optimisation consultancy based in Bengaluru, India.

## Tech stack

- **Static HTML/CSS/JS** — no framework, no build step. Fast, free to host, easy to maintain.
- **Custom design system** — dark-navy aesthetic with royal-blue accent (`assets/css/style.css`).
- **Fonts** — Inter (body) + Space Grotesk (display) via Google Fonts.
- **Contact form** — Netlify Forms (free) — set `data-netlify="true"` on the form (already done).

## Structure

```
├── index.html          # Home
├── about.html          # About / story / values
├── services.html       # Audit · Consulting · Process Optimisation
├── team.html           # Team + certifications
├── contact.html        # Contact form + info
├── blogs.html          # Insights index
├── blogs/*.html        # 16 articles
├── assets/
│   ├── css/style.css   # Design system
│   ├── js/main.js      # Nav, scroll, reveal, form
│   └── img/            # Logos, team photos, cert badges
├── build.py            # Generator (rebuilds pages from content)
├── netlify.toml         # Netlify config (caching, headers)
├── sitemap.xml
└── robots.txt
```

## Rebuild

```bash
python3 build.py
```

This regenerates all pages and blog articles from `build.py` + the legacy blog source files.

## Hosting (free)

### Option A — Netlify (recommended, supports the contact form)

1. Push this folder to a GitHub repo.
2. Netlify → "Add new site" → "Import from Git" → pick the repo.
3. Build command: *(none — leave blank)*. Publish directory: `.` (root).
4. The contact form submissions appear under Netlify → "Forms".

### Option B — GitHub Pages

1. Push to GitHub.
2. Repo Settings → Pages → Source: `main` branch `/` (root).
3. Note: GitHub Pages has no form backend — the contact form will need Formspree, Getform, or a mailto fallback.

### Option C — Cloudflare Pages

1. Push to GitHub.
2. Cloudflare Pages → "Create project" → connect repo.
3. Build command: *(none)*. Output directory: `.`.

## Custom domain

Connect `ignasia.in` (or your preferred domain) via the hosting provider's domain settings. SSL is free on all three providers.

---

© 2026 ignasia Consulting Private Limited.
