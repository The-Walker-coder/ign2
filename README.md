# ignasia Consulting — Website

Professional website for ignasia Consulting — an independent GRC, cybersecurity, and business process optimisation consultancy based in Bengaluru, India.

## Tech stack

- **Static HTML/CSS/JS** — no framework, no build step. Fast, free to host, easy to maintain.
- **Custom design system** — dark-navy aesthetic with royal-blue accent (`assets/css/style.css`).
- **Fonts** — Inter (body) + Space Grotesk (display) via Google Fonts.
- **Contact form** — [FormSubmit](https://formsubmit.co) (free, no account) posting to info@ignasia.in.

## Structure

```
├── index.html          # Home
├── about.html          # About / story / values
├── services.html       # Audit · Consulting · Process Optimisation
├── team.html           # Team + certifications
├── contact.html        # Contact form + info
├── thank-you.html      # Form submission confirmation
├── blogs.html          # Insights index
├── blogs/*.html        # 16 articles
├── assets/
│   ├── css/style.css   # Design system
│   ├── js/main.js      # Nav, scroll, reveal, form
│   └── img/            # Logo, favicon, hero visuals, team photos, cert badges
├── build.py            # Generator (rebuilds pages from content)
├── CNAME                # Custom domain → ignasia.in
├── .nojekyll            # Serve raw files on GitHub Pages
├── sitemap.xml
└── robots.txt
```

## Rebuild

```bash
python3 build.py
```

This regenerates all pages and blog articles.

## Hosting — GitHub Pages (free)

This repo is configured for GitHub Pages with a custom domain.

### Setup

1. Push this folder to a GitHub repository (e.g. `The-Walker-coder/ign2`).
2. In the repo: **Settings → Pages → Source: `main` branch, `/` (root)**.
3. The included `CNAME` file points the site to `ignasia.in`.
4. The `.nojekyll` file tells GitHub Pages to serve files as-is (no Jekyll processing).

### Custom domain (ignasia.in via GoDaddy)

In GoDaddy DNS, add these records:

| Type | Name | Value |
|------|------|-------|
| A    | @    | 185.199.108.153 |
| A    | @    | 185.199.109.153 |
| A    | @    | 185.199.110.153 |
| A    | @    | 185.199.111.153 |
| CNAME | www | `your-username.github.io.` |

Then in GitHub: **Settings → Pages → Custom domain → enter `ignasia.in` → Enforce HTTPS**.

SSL is free and automatic once DNS propagates (may take up to 24h).

### Contact form (FormSubmit)

The contact form posts to `https://formsubmit.co/info@ignasia.in`.

- **First submission:** FormSubmit sends a one-time confirmation email to info@ignasia.in. Click the link to activate.
- **After activation:** all form submissions arrive in the info@ignasia.in inbox as formatted emails.
- No account, no cost, no limits.

---

© 2026 ignasia Consulting Private Limited.
