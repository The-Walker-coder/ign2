#!/usr/bin/env python3
"""
Ignasia Consulting — website build script.
Generates all static HTML pages from a shared template + content,
and re-wraps the 16 legacy blog posts in the new design system.
"""
import os, re, html, json
from bs4 import BeautifulSoup, NavigableString

ROOT = "/home/user/workspace/ignasia-site"
OLD_BLOGS = "/home/user/workspace/ign2-old/blogs"
OLD_ROOT = "/home/user/workspace/ign2-old"

# ---------- Brand / site data ----------
SITE = {
    "name": "ignasia Consulting",
    "tagline": "Audit, Consulting & Business Process Optimisation",
    "desc": "ignasia Consulting is your global partner in information security, risk management, and organisational transformation. We empower ambitious organisations to navigate uncertainty, defend against cyber threats, and unlock lasting growth.",
    "email": "info@ignasia.in",
    "phone": "+91 8971 21 2227",
    "phone_href": "+918971212227",
    "address": "Future Knowledge Labs, Bengaluru 560102, India",
    "linkedin": "https://www.linkedin.com/company/ignasia/",
    "year": "2026",
}

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("team.html", "Team"),
    ("blogs.html", "Insights"),
    ("contact.html", "Contact"),
]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">'

# SVG logo mark
LOGO_MARK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 3 7v10l9 5 9-5V7z"/><path d="M12 2v20M3 7l9 5 9-5"/></svg>'

ICONS = {
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "briefcase": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-2 1.5-4 1.5-6 0M2 16l3-8 3 8c-2 1.5-4 1.5-6 0M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>',
    "arrow": '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .962 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.962 0z"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 7 13.5 15.5l-5-5L2 17"/><path d="M16 7h6v6"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18M7 16V9M12 16V5M17 16v-3"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
}

def icon(name): return ICONS.get(name, "")

# ---------- Shared template parts ----------
def head(title, desc, path_prefix="", extra=""):
    pp = path_prefix
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="{pp}assets/img/favicon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{FONTS}
<link rel="stylesheet" href="{pp}assets/css/style.css">
{extra}
</head>
<body>"""

def header(active, path_prefix=""):
    pp = path_prefix
    links = ""
    for href, label in NAV:
        cls = " active" if href == active else ""
        links += f'<li><a class="nav-link{cls}" href="{pp}{href}">{label}</a></li>'
    return f"""
<header class="site-header" id="header">
  <div class="container">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="{pp}index.html" aria-label="{SITE['name']} home">
        <span class="brand-mark">{LOGO_MARK}</span>
        <span>ignasia<b>.</b>Consulting</span>
      </a>
      <ul class="nav-links" id="navLinks">
        {links}
      </ul>
      <div class="nav-cta">
        <a class="btn btn-primary" href="{pp}contact.html">Get in touch</a>
        <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">{ICONS['menu']}</button>
      </div>
    </nav>
  </div>
</header>"""

def footer(path_prefix=""):
    pp = path_prefix
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{pp}index.html">
          <span class="brand-mark">{LOGO_MARK}</span>
          <span>ignasia<b>.</b>Consulting</span>
        </a>
        <p>{SITE['tagline']}. Your global partner in information security, risk management, and organisational transformation.</p>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <ul>
          <li><a href="{pp}about.html">About</a></li>
          <li><a href="{pp}services.html">Services</a></li>
          <li><a href="{pp}team.html">Team</a></li>
          <li><a href="{pp}blogs.html">Insights</a></li>
          <li><a href="{pp}contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <ul>
          <li><a href="{pp}services.html#audit">Audit</a></li>
          <li><a href="{pp}services.html#consulting">Consulting</a></li>
          <li><a href="{pp}services.html#optimization">Process Optimisation</a></li>
          <li><a href="{pp}contact.html?service=social-impact">Social Impact</a></li>
        </ul>
      </div>
      <div class="footer-col footer-contact">
        <h5>Get in touch</h5>
        <ul>
          <li><span class="ic">{ICONS['mail']}</span><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li><span class="ic">{ICONS['phone']}</span><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
          <li><span class="ic">{ICONS['pin']}</span>{SITE['address']}</li>
          <li><span class="ic">{ICONS['linkedin']}</span><a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; {SITE['year']} {SITE['name']}. All rights reserved.</span>
      <span>Bengaluru, India &middot; Serving clients worldwide</span>
    </div>
  </div>
</footer>
<script src="{pp}assets/js/main.js"></script>
</body>
</html>"""

# ---------- Blog metadata (parsed from old blogs.html index) ----------
def parse_blog_index():
    with open(os.path.join(OLD_ROOT, "blogs.html"), encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    posts = []
    for card in soup.select("article.blog-card"):
        a = card.select_one("h3 a")
        if not a: continue
        href = a["href"]
        title = a.get_text(strip=True)
        date_el = card.select_one(".blog-date")
        date = date_el.get_text(strip=True) if date_el else ""
        tags = [t.get_text(strip=True) for t in card.select(".tag")]
        excerpt_el = card.select_one(".blog-card-body p")
        excerpt = excerpt_el.get_text(strip=True) if excerpt_el else ""
        posts.append({"slug": os.path.basename(href).replace(".html",""),
                      "href": href, "title": title, "date": date,
                      "tags": tags, "excerpt": excerpt})
    return posts

def parse_blog_meta_from_file(path):
    """Extract title, description, first paragraph excerpt, and tags from a blog HTML file."""
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    title = ""
    if soup.title: title = soup.title.get_text(strip=True)
    # strip trailing site name
    title = re.sub(r'\s*[\-\|]\s*ignasia.*$', '', title, flags=re.I).strip()
    # prefer first h1
    h1 = soup.find('h1')
    if h1: title = h1.get_text(strip=True)
    desc = ""
    m = soup.find('meta', attrs={'name': 'description'})
    if m and m.get('content'): desc = m['content'].strip()
    # excerpt: first non-heading paragraph with substance
    excerpt = desc
    for p in soup.find_all('p'):
        txt = p.get_text(strip=True)
        if len(txt) > 60:
            excerpt = txt[:240].rsplit(' ',1)[0] + '…'
            break
    # tags: look for .tag spans in file, else derive from title keywords
    tags = [t.get_text(strip=True) for t in soup.select('.tag')][:3]
    if not tags:
        kw = {"iso":"ISO 27001","ai":"AI","cybersecurity":"Cybersecurity","gdpr":"GDPR","dpdp":"DPDP",
              "risk":"Risk Management","business continuity":"Business Continuity","forensic":"Digital Forensics",
              "training":"Awareness","enterprise":"Enterprise","compliance":"Compliance","process":"Process"}
        low = (title + ' ' + excerpt).lower()
        tags = [v for k,v in kw.items() if k in low][:3]
        if not tags: tags = ["GRC"]
    return {"title": title, "excerpt": excerpt, "tags": tags}

def all_blog_posts():
    """Combine index metadata with direct-from-file metadata for ALL blog files."""
    indexed = {p["slug"]: p for p in parse_blog_index()}
    posts = []
    for fn in sorted(os.listdir(OLD_BLOGS)):
        if not fn.endswith('.html'): continue
        slug = fn[:-5]
        path = os.path.join(OLD_BLOGS, fn)
        meta = parse_blog_meta_from_file(path)
        if slug in indexed:
            p = indexed[slug]
            # keep index date/tags if present, but ensure title/excerpt
            p.setdefault('title', meta['title'])
            p.setdefault('excerpt', meta['excerpt'])
            if not p.get('tags'): p['tags'] = meta['tags']
            posts.append(p)
        else:
            posts.append({"slug": slug, "title": meta['title'], "date": "",
                          "tags": meta['tags'], "excerpt": meta['excerpt']})
    return posts

def extract_blog_content(path):
    """Extract main article HTML from a legacy blog file, re-wrapped in new design."""
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    # Find the article/main content container
    content = None
    for sel in ["article.blog-article .col-lg-8", "article.blog-article", "main.blog-post article",
                "main.blog-post", "main .container", "article"]:
        content = soup.select_one(sel)
        if content: break
    if content is None:
        content = soup.body or soup

    # Remove nav, header, footer, breadcrumbs, scripts within content
    for tag in content.select("nav, header, footer, .breadcrumb, script, style, .blog-card, .share-buttons, .related-posts, .cta, .btn, .article-cta"):
        tag.decompose()

    # Clean classes & bootstrap cruft from all tags
    for tag in content.find_all(True):
        if tag.has_attr("class"):
            del tag["class"]
        for attr in list(tag.attrs):
            if attr in ("style","id","data-bs-toggle","data-bs-target","data-bs-spy"):
                del tag[attr]
    # Remove empty <div> wrappers
    for div in content.find_all("div"):
        if not div.get_text(strip=True) and not div.find(["img","table","ul","ol"]):
            div.decompose()

    # Convert <br> separated lines in <p> to proper list where appropriate — keep simple
    inner = content.decode_contents()
    # Tidy up excessive whitespace
    inner = re.sub(r'\n{3,}', '\n\n', inner)
    inner = re.sub(r'<p>\s*</p>', '', inner)
    return inner

# ---------- Page builders ----------
def write_page(filename, title, desc, body, active="", path_prefix=""):
    page = head(title, desc, path_prefix) + header(active, path_prefix) + "\n<main>\n" + body + "\n</main>\n" + footer(path_prefix)
    out = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)

# ============ HOME ============
def build_home():
    body = f"""
<section class="hero">
  <div class="container">
    <div class="hero-inner">
      <span class="hero-tag"><span class="dot"></span>Audit &middot; Consulting &middot; Business Process Optimisation</span>
      <h1>Trust, resilience, and impact — <span class="grad">engineered for a changing world.</span></h1>
      <p>{SITE['desc']} Backed by industry-leading expertise and a passion for making the world a better place.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="services.html">Explore our services {ICONS['arrow']}</a>
        <a class="btn btn-ghost btn-lg" href="contact.html">Get started</a>
      </div>
    </div>
    <div class="stats reveal">
      <div class="stat"><div class="num">35<span class="accent">+</span></div><div class="lbl">Years Combined Experience</div></div>
      <div class="stat"><div class="num">99<span class="accent">%</span></div><div class="lbl">First-Time ISO 27001 Pass Rate</div></div>
      <div class="stat"><div class="num">70<span class="accent">+</span></div><div class="lbl">Successful Implementations</div></div>
      <div class="stat"><div class="num">5</div><div class="lbl">Industry Sectors Served</div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Why choose ignasia</span>
      <h2 class="section-title">Boutique agility. <span class="accent">Premier consulting depth.</span></h2>
      <p class="section-sub">We fuse proven methodologies with tailored, creative thinking — so every engagement feels bespoke, not templated.</p>
    </div>
    <div class="grid grid-3">
      {feature("01","Global experts","Real-world, hands-on experience in cybersecurity, GRC, risk-driven, and operational excellence.","users")}
      {feature("02","Impact-oriented","We deliver measurable business value and strategic resilience — not slide-deck advice.","trend")}
      {feature("03","Tailored solutions","Every engagement designed around your specific needs, sector, and growth stage.","target")}
      {feature("04","Trusted worldwide","Serving clients from high-growth startups to established enterprises and mission-driven NGOs.","globe")}
      {feature("05","Recognised credentials","Our certified professionals are trusted by regulators like RBI, IRDAI, SEBI, SEC and FTC.","scale")}
      {feature("06","Built for scale","Frameworks and automation designed to grow with you, from first audit to enterprise programme.","settings")}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Our core services</span>
      <h2 class="section-title">Comprehensive solutions for <span class="accent">modern business challenges.</span></h2>
    </div>
    {service_card("01","Audit","Independent assurance & certification readiness","ISO 27001, regulatory compliance, and information security audits that stand up to scrutiny.","services.html#audit")}
    {service_card("02","Consulting","Strategic advisory & implementation","GRC strategy, information security, data privacy, and RSA Archer platform advisory.","services.html#consulting")}
    {service_card("03","Process Optimisation","Operational excellence & automation","RSA Archer implementation, GRC process automation, and business continuity programmes.","services.html#optimization")}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="impact">
      <div class="reveal">
        <span class="eyebrow">Our commitment to social good</span>
        <h2 class="section-title" style="font-size:var(--text-xl)">Building a kinder, <span class="accent">sustainable, better future.</span></h2>
        <p class="section-sub" style="margin-top:var(--s-5)">At ignasia, we know prosperity means nothing unless shared. That's why we champion causes beyond profit — supporting NGOs, nonprofits, and social innovators with preferential pricing and dedicated support. If your work makes lives better or the world safer, we want to help you succeed.</p>
        <a class="link-arrow" href="contact.html?service=social-impact">Talk to us about your mission {ICONS['arrow']}</a>
      </div>
      <div class="impact-boxes reveal">
        {impact_box("gift","Preferred rates","For NGOs and social enterprises")}
        {impact_box("heart","Pro-bono work","Select mission-aligned assessments")}
        {impact_box("chart","Impact metrics","Frameworks for social outcomes")}
        {impact_box("target","Mission strategy","Security aligned to purpose")}
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="cta-banner reveal">
      <h2>Ready to elevate your risk and compliance posture?</h2>
      <p>Start with a conversation, or take our complimentary 25-question GRC self-assessment.</p>
      <div class="cta-actions">
        <a class="btn btn-primary btn-lg" href="contact.html">Contact us</a>
        <a class="btn btn-ghost btn-lg" href="contact.html?service=assessment">Start GRC assessment</a>
      </div>
    </div>
  </div>
</section>
"""
    write_page("index.html", f"{SITE['name']} — Audit, Consulting & Business Process Optimisation", SITE['desc'], body, "index.html")

def feature(idx, title, text, ic):
    return f"""<div class="feature-card reveal"><div class="ic">{ICONS[ic]}</div><div class="idx">{idx}</div><h3>{title}</h3><p>{text}</p></div>"""

def service_card(num, title, tag, desc, href):
    return f"""<a class="service-card reveal" href="{href}"><span class="num">{num}</span><div><h3>{title}</h3><div class="tag">{tag}</div><p>{desc}</p></div><span class="arrow">{ICONS['arrow']}</span></a>"""

def impact_box(ic, title, text):
    return f"""<div class="impact-box"><div class="ic">{ICONS[ic]}</div><h4>{title}</h4><p>{text}</p></div>"""

# ============ SERVICES ============
def build_services():
    body = f"""
<section class="page-header">
  <div class="container">
    <span class="eyebrow">What we do</span>
    <h1>Audit, Consulting & Business Process Optimisation</h1>
    <p class="lead">We deliver Governance, Risk, and Compliance excellence through three core service pillars designed to protect, transform, and optimise your organisation.</p>
  </div>
</section>

<section class="section">
  <div class="container">

    <div class="service-block reveal" id="audit">
      <h2><span class="ic">{ICONS['search']}</span> Audit</h2>
      <p class="lead">Independent assurance and certification readiness</p>
      <div class="service-grid">
        <div><h4>ISO 27001 Audit & Certification</h4><p>Gap analysis against ISO 27001:2022 requirements, internal audit services and management reviews, pre-certification readiness assessments, external certification support and surveillance, and ISMS documentation review and validation.</p></div>
        <div><h4>Regulatory Compliance Audits</h4><p>RBI, IRDAI, and SEBI compliance assessments; DPDP Act and GDPR compliance audits; SOC 2 Type I and Type II readiness; third-party vendor security assessments; and privacy impact assessments (PIAs).</p></div>
        <div><h4>Information Security Audits</h4><p>Comprehensive security posture assessments, vulnerability assessments and penetration testing readiness, cloud security configuration reviews, access control and privilege management audits, and data governance and classification audits.</p></div>
        <div><h4>Certification Readiness</h4><p>Pre-audit gap remediation, evidence preparation, control implementation tracking, management review facilitation, and ongoing surveillance support to keep your certifications current.</p></div>
      </div>
    </div>

    <div class="service-block reveal" id="consulting">
      <h2><span class="ic">{ICONS['briefcase']}</span> Consulting</h2>
      <p class="lead">Strategic advisory and implementation services</p>
      <div class="service-grid">
        <div><h4>GRC Strategy & Framework Development</h4><p>Enterprise risk management program design, governance framework implementation, risk appetite and tolerance definition, board-level risk reporting and dashboards, and regulatory horizon scanning and impact analysis.</p></div>
        <div><h4>Information Security Consulting</h4><p>Security strategy and roadmap development, threat modelling and risk assessment, security architecture design and review, incident response planning and testing, and security awareness program design.</p></div>
        <div><h4>Data Privacy & Protection Advisory</h4><p>DPDP Act implementation roadmaps, GDPR compliance strategy and gap remediation, privacy by design consulting, cross-border data transfer assessments, and data retention and deletion policy development.</p></div>
        <div><h4>RSA Archer Platform Advisory</h4><p>Archer platform strategy and roadmap, use case design and optimisation, integration architecture planning, governance model establishment, and ROI optimisation consulting.</p></div>
      </div>
    </div>

    <div class="service-block reveal" id="optimization">
      <h2><span class="ic">{ICONS['settings']}</span> Business Process Optimisation</h2>
      <p class="lead">Operational excellence and automation</p>
      <div class="service-grid">
        <div><h4>RSA Archer Implementation & Optimisation</h4><p>Complete platform deployment and configuration, custom use case development (Risk, Compliance, Audit, TPRM), workflow automation and integration, user training and change management, and ongoing managed services and support.</p></div>
        <div><h4>GRC Process Automation</h4><p>Risk assessment workflow automation, compliance monitoring and reporting automation, policy management lifecycle optimisation, vendor risk management process streamlining, and risk-driven management workflow implementation.</p></div>
        <div><h4>Business Continuity & Crisis Management</h4><p>Business impact analysis (BIA) and process mapping, BCP/DRP development and testing, crisis communication framework design, supply chain resilience planning, and tabletop exercises and simulation training.</p></div>
        <div><h4>Operational Risk Management</h4><p>Process risk identification and mapping, key risk indicator (KRI) development, loss event management frameworks, control effectiveness testing automation, and operational resilience program design.</p></div>
      </div>
    </div>

    <div class="service-block reveal" id="specialised">
      <h2><span class="ic">{ICONS['spark']}</span> Specialised Programs</h2>
      <p class="lead">Designed for purpose-driven organisations and self-directed teams</p>
      <div class="service-grid">
        <div><h4>For Purpose-Driven Organisations</h4><p>Preferred-rate consulting packages, pro-bono risk assessments for select NGOs, social impact measurement frameworks, and mission-aligned security strategies.</p></div>
        <div><h4>Self-Assessment Tools</h4><p>A 25-question GRC maturity assessment, ISO 27001 readiness scoring, NIST CSF alignment evaluation, and instant dashboard with recommendations.</p></div>
      </div>
    </div>

    <div class="cta-banner reveal" style="margin-top:var(--s-10)">
      <h2>Ready to elevate your risk and compliance posture?</h2>
      <p>Contact us for a confidential consultation, or begin with our complimentary GRC self-assessment.</p>
      <div class="cta-actions">
        <a class="btn btn-primary btn-lg" href="contact.html">Contact us</a>
        <a class="btn btn-ghost btn-lg" href="contact.html?service=assessment">Start assessment</a>
      </div>
    </div>
  </div>
</section>
"""
    write_page("services.html", f"Our Services — {SITE['name']}", "Comprehensive GRC, cybersecurity, and business process optimisation services from ignasia Consulting's expert team.", body, "services.html")

# ============ ABOUT ============
def build_about():
    body = f"""
<section class="page-header">
  <div class="container">
    <span class="eyebrow">About us</span>
    <h1>Independent, values-driven consultancy</h1>
    <p class="lead">Dedicated to strengthening trust, resilience, and positive impact in a rapidly changing world.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="prose" style="max-width:760px;margin-inline:auto;">
      <p class="section-sub" style="font-size:var(--text-lg);color:var(--text);">ignasia Consulting is an independent, values-driven consultancy dedicated to strengthening trust, resilience, and positive impact in a rapidly changing world.</p>
      <p>Founded by industry veterans, our mission is to help organisations unlock their full potential while navigating the complex landscape of cyber risk, regulatory change, and operational challenges. Beyond our core team, ignasia boasts a wide and diverse network of professionals and industry experts — giving us access to a vast pool of knowledge and skills.</p>
      <h2>Our Story</h2>
      <p>Born out of a desire to blend deep technical expertise with a genuine commitment to societal good, ignasia Consulting brings together leading professionals from cybersecurity, risk management, business process optimisation, and governance. We believe in partnership — not just providing advice, but working side by side with our clients to co-create sustainable, effective solutions.</p>
      <h2>Our Values</h2>
    </div>
    <div class="values" style="max-width:760px;margin-inline:auto;margin-top:var(--s-8);">
      {value("scale","Integrity","We stand for honesty, transparency, and ethical leadership.")}
      {value("spark","Excellence","Every engagement is built on rigorous standards and a commitment to results.")}
      {value("heart","Empathy","We care about your people, your purpose, and your impact on the world.")}
      {value("globe","Responsibility","We support organisations that make a difference — social enterprises, NGOs, and businesses committed to positive change.")}
    </div>
    <div class="prose" style="max-width:760px;margin-inline:auto;">
      <h2>Why We're Different</h2>
      <ul>
        <li>We fuse proven methodologies with tailored, creative thinking.</li>
        <li>We serve clients ranging from innovative startups to established global organisations and social ventures.</li>
        <li>Our team's collective experience spans diverse sectors and geographies, giving us a unique perspective on modern business risk and opportunity.</li>
      </ul>
    </div>
    <div class="cta-banner reveal" style="margin-top:var(--s-16)">
      <h2>See how ignasia can help your organisation thrive?</h2>
      <p>Let's start a conversation about your goals.</p>
      <div class="cta-actions"><a class="btn btn-primary btn-lg" href="contact.html">Contact us</a></div>
    </div>
  </div>
</section>
"""
    write_page("about.html", f"About Us — {SITE['name']}", "Learn about ignasia Consulting's mission, values, and expertise in governance, risk, compliance, and cybersecurity consulting.", body, "about.html")

def value(ic, title, text):
    return f"""<div class="value-item reveal"><div class="ic">{ICONS[ic]}</div><h4>{title}</h4><p>{text}</p></div>"""

# ============ TEAM ============
def build_team():
    body = f"""
<section class="page-header">
  <div class="container">
    <span class="eyebrow">Our team</span>
    <h1>Meet our expert team</h1>
    <p class="lead">Our strength lies in our people — combining deep technical expertise with a commitment to creating a secure digital future.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="section-sub" style="max-width:760px;margin-inline:auto;text-align:center;margin-bottom:var(--s-16);">At ignasia Consulting, our strength lies in our people. Our team combines deep technical expertise, premier consulting experience, and a shared commitment to creating a kinder, more secure digital future. Each member brings verified certifications and proven track records that collectively deliver world-class GRC solutions.</p>

    <div class="founder-card reveal">
      <div class="photo"><img src="assets/img/team-abhishek.jpg" alt="Abhishek Divakar" loading="lazy"></div>
      <div class="info">
        <h3>Abhishek Divakar</h3>
        <p class="team-role">Founder & Director</p>
        <p class="team-bio">Abhishek is the visionary leader behind ignasia Consulting, bringing over 12 years of expertise in information security, risk management, and GRC advisory. His journey spans prestigious organisations including PwC India and Wipro's award-winning risk function, where he pioneered innovative security solutions and led enterprise-wide cybersecurity initiatives.</p>
        <div class="certs-row">
          <span class="cert-badge">CISA</span>
          <span class="cert-badge">CISM</span>
          <span class="cert-badge">CRISC</span>
          <span class="cert-badge">ISO 27001 Lead Auditor</span>
          <span class="cert-badge">RSA Certified Archer Administrator</span>
          <span class="cert-badge">ICSI-CNSS</span>
        </div>
        <div class="team-quote">"Security isn't just about protecting data — it's about enabling organisations to confidently pursue their mission unburdened by fear and doubt."</div>
        <a class="team-link" href="https://www.linkedin.com/in/abhishekdivakar/" target="_blank" rel="noopener">{ICONS['linkedin']} Connect on LinkedIn</a>
      </div>
    </div>

    <div class="team-grid">
      {team_card("team-shalu.jpg","Shalu Jain","Information Security Analyst & RSA Archer Specialist","Shalu brings over 10 years of enterprise security excellence and GRC platform mastery. Her expertise in RSA Archer development, combined with comprehensive security management experience at Sony and Wipro, makes her instrumental in delivering automated, scalable security solutions.",["CISM","CompTIA Security+","Certified in Cybersecurity (CC)","ISO 27001 Lead Auditor"],"\"Complex compliance challenges deserve elegant, automated solutions that empower teams to focus on strategic security outcomes.\"","https://www.linkedin.com/in/shalujain18/")}
      {team_card("team-akshita.jpg","Akshita Satish","Information Security Analyst & ISO 27001 Specialist","Akshita represents the next generation of cybersecurity professionals, combining rigorous technical training with creative problem-solving perspectives from her unique multi-domain background. Her fresh approach to traditional security challenges brings innovative solutions to complex GRC requirements.",["ISO 27001:2022 Lead Auditor","Certified in Cybersecurity (CC)"],"\"Security should be intuitive and accessible — when we make it understandable, we make it stronger.\"","https://www.linkedin.com/in/akshita-satish/")}
      {team_card("team-dolly.jpg","Dolly Kumar","Client Relations & Operations Manager","Dolly drives operational excellence and client success at ignasia, bringing entrepreneurial leadership and proven business development expertise. Her experience spans business operations, project management, and strategic growth across multiple industries, with a deep commitment to social impact initiatives.",[],"\"Success is measured not just in business outcomes, but in the positive impact we create for our clients and communities.\"","https://www.linkedin.com/in/kdolly/")}
    </div>

    <div class="service-block reveal" style="margin-top:var(--s-12);text-align:center;">
      <h2 style="justify-content:center;">Our Collective Strength</h2>
      <div class="stats" style="margin-top:var(--s-8);">
        <div class="stat"><div class="num">35<span class="accent">+</span></div><div class="lbl">Years Combined Experience</div></div>
        <div class="stat"><div class="num">99<span class="accent">%</span></div><div class="lbl">First-Time ISO 27001 Pass Rate</div></div>
        <div class="stat"><div class="num">70<span class="accent">+</span></div><div class="lbl">Successful Implementations</div></div>
        <div class="stat"><div class="num">5</div><div class="lbl">Industry Sectors Served</div></div>
      </div>
      <h4 style="font-size:var(--text-sm);color:var(--text-faint);letter-spacing:0.12em;text-transform:uppercase;margin-top:var(--s-10);margin-bottom:var(--s-6);">Certifications Held</h4>
      <div class="cert-strip">
        <img src="assets/img/cert-cisa-logo.png" alt="CISA">
        <img src="assets/img/cert-cism-logo.png" alt="CISM">
        <img src="assets/img/cert-crisc-logo.png" alt="CRISC">
        <img src="assets/img/cert-iso27001-lead-auditor-logo.png" alt="ISO 27001 Lead Auditor">
        <img src="assets/img/cert-rsa-archer-admin-logo.png" alt="RSA Certified Archer Administrator">
        <img src="assets/img/cert-isc2-cc-logo.png" alt="(ISC)² Certified in Cybersecurity">
      </div>
    </div>
  </div>
</section>
"""
    write_page("team.html", f"Our Team — {SITE['name']}", "Meet the ignasia Consulting team — certified experts in GRC, cybersecurity, and business process optimisation.", body, "team.html")

def team_card(img, name, role, bio, certs, quote, linkedin):
    certs_html = "".join(f'<span class="cert-badge">{c}</span>' for c in certs)
    quote_html = f'<div class="team-quote">{quote}</div>' if quote else ""
    certs_block = f'<div class="team-certs">{certs_html}</div>' if certs else ""
    return f"""<div class="team-card reveal">
      <div class="team-photo-wrap"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
      <div class="team-body">
        <h3>{name}</h3>
        <p class="team-role">{role}</p>
        <p class="team-bio">{bio}</p>
        {certs_block}
        {quote_html}
        <a class="team-link" href="{linkedin}" target="_blank" rel="noopener">{ICONS['linkedin']} Connect on LinkedIn</a>
      </div>
    </div>"""

# ============ CONTACT ============
def build_contact():
    body = f"""
<section class="page-header">
  <div class="container">
    <span class="eyebrow">Contact us</span>
    <h1>Let's find a GRC solution perfect for you</h1>
    <p class="lead">Clear communication is our priority. Whether you're exploring GRC solutions or ready to dive into a project, we're here to support you every step of the way.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div class="reveal">
        <h2 style="font-size:var(--text-xl);margin-bottom:var(--s-6);">Get in touch</h2>
        <div class="contact-item"><div class="ic">{ICONS['mail']}</div><div><h5>Email</h5><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></div>
        <div class="contact-item"><div class="ic">{ICONS['phone']}</div><div><h5>Phone</h5><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></div>
        <div class="contact-item"><div class="ic">{ICONS['pin']}</div><div><h5>Address</h5><p>{SITE['address']}</p></div></div>
        <div class="contact-item"><div class="ic">{ICONS['linkedin']}</div><div><h5>LinkedIn</h5><a href="{SITE['linkedin']}" target="_blank" rel="noopener">linkedin.com/company/ignasia</a></div></div>

        <div style="margin-top:var(--s-8);padding:var(--s-6);border:1px solid var(--border);border-radius:var(--r-lg);background:var(--surface);">
          <h4 style="margin-bottom:var(--s-2);">Begin with a free GRC self-assessment</h4>
          <p style="color:var(--text-muted);font-size:var(--text-sm);">Take our 25-question assessment benchmarking your GRC maturity against ISO 27001, NIST CSF, and CIS Controls. Instant insights and tailored guidance.</p>
          <a class="btn btn-ghost btn-block" href="contact.html?service=assessment" style="margin-top:var(--s-4);">Start your assessment</a>
        </div>
      </div>

      <div class="form-card reveal">
        <div class="form-success" id="formSuccess">{ICONS['check']} Thank you — your message has been received. We'll respond within one business day.</div>
        <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" id="contactForm">
          <input type="hidden" name="form-name" value="contact">
          <p class="sr-only"><label>Don't fill this out: <input name="bot-field"></label></p>
          <div class="field"><label for="name">Name <span class="req">*</span></label><input type="text" id="name" name="name" required></div>
          <div class="field"><label for="email">Email <span class="req">*</span></label><input type="email" id="email" name="email" required></div>
          <div class="field"><label for="company">Company</label><input type="text" id="company" name="company"></div>
          <div class="field"><label for="service">Service of interest</label>
            <select id="service" name="service">
              <option value="">Select a service</option>
              <option value="audit">Audit Services</option>
              <option value="consulting">Consulting Services</option>
              <option value="optimization">Business Process Optimisation</option>
              <option value="social-impact">Social Impact Program</option>
              <option value="assessment">Free GRC Self-Assessment</option>
            </select>
          </div>
          <div class="field"><label for="message">Message <span class="req">*</span></label><textarea id="message" name="message" rows="4" required></textarea></div>
          <button type="submit" class="btn btn-primary btn-lg btn-block">Send message</button>
          <p class="form-note">Your information is treated with strict confidentiality. We respond within one business day.</p>
        </form>
      </div>
    </div>

    <div class="cta-banner reveal" style="margin-top:var(--s-16)">
      <h2>Supporting purpose-driven organisations</h2>
      <p>Preferred support rates available for NGOs, nonprofits, and social enterprises. If your work aims to improve lives, strengthen communities, or protect our shared future — we'd love to explore how we can support your mission.</p>
      <div class="cta-actions"><a class="btn btn-primary btn-lg" href="contact.html?service=social-impact">Tell us about your mission</a></div>
    </div>
  </div>
</section>
"""
    write_page("contact.html", f"Contact Us — {SITE['name']}", "Contact ignasia Consulting for GRC, cybersecurity, and compliance solutions. Email info@ignasia.in or call +91 8971 21 2227.", body, "contact.html")

# ============ BLOG INDEX ============
def build_blog_index(posts):
    cards = ""
    for p in posts:
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"][:3])
        cards += f"""<article class="blog-card reveal">
        <div class="blog-card-body">
          <div class="tags">{tags}</div>
          <h3><a href="blogs/{p['slug']}.html">{p['title']}</a></h3>
          <p class="excerpt">{p['excerpt']}</p>
          <div class="blog-meta"><span>{p['date']}</span></div>
          <a class="link-arrow read" href="blogs/{p['slug']}.html">Read article {ICONS['arrow']}</a>
        </div>
      </article>"""
    body = f"""
<section class="page-header">
  <div class="container">
    <span class="eyebrow">Insights</span>
    <h1>Insights & expertise</h1>
    <p class="lead">Latest thoughts on governance, risk, compliance, and cybersecurity — from the ignasia team.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="blog-grid">
      {cards}
    </div>
  </div>
</section>
"""
    write_page("blogs.html", f"Insights — {SITE['name']}", "Insights on governance, risk, compliance, and cybersecurity from ignasia Consulting.", body, "blogs.html")

# ============ BLOG POSTS ============
def build_blog_posts(posts):
    for p in posts:
        old_path = os.path.join(OLD_BLOGS, p["slug"] + ".html")
        if not os.path.exists(old_path):
            print("  MISSING:", p["slug"]); continue
        content_html = extract_blog_content(old_path)
        tags = "".join(f'<span class="tag">{t}</span>' for t in p["tags"])
        body = f"""
<section class="page-header">
  <div class="container">
    <div class="tags" style="display:flex;gap:var(--s-2);flex-wrap:wrap;margin-bottom:var(--s-4);">{tags}</div>
    <p style="color:var(--text-faint);font-size:var(--text-sm);">{p['date']}</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="article-layout">
      <article class="article">
        <div class="content">
          {content_html}
        </div>
        <footer class="article-footer">
          <a class="article-back" href="../blogs.html">{ICONS['arrow'].replace('class="arr"','style="transform:rotate(180deg)"')} Back to all insights</a>
        </footer>
      </article>
    </div>
  </div>
</section>
"""
        out = os.path.join(ROOT, "blogs", p["slug"] + ".html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        page = head(p["title"] + f" — {SITE['name']}", p["excerpt"][:157], "../") + header("", "../") + "\n<main>\n" + body + "\n</main>\n" + footer("../")
        with open(out, "w", encoding="utf-8") as f:
            f.write(page)
        print("  built:", p["slug"])

def main():
    print("Building home, services, about, team, contact...")
    build_home(); build_services(); build_about(); build_team(); build_contact()
    posts = all_blog_posts()
    # sort: dated posts first (by date desc-ish, keep file order), undated last
    dated = [p for p in posts if p.get('date')]
    undated = [p for p in posts if not p.get('date')]
    posts = dated + undated
    print(f"Found {len(posts)} blog posts. Building index + articles...")
    build_blog_index(posts)
    build_blog_posts(posts)
    print("Done.")

if __name__ == "__main__":
    main()
