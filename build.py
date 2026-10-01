"""Builds the portfolio-style resume website into ./dist (standard library only)."""
import shutil
from html import escape as e
from pathlib import Path

import resume_data as d

ROOT = Path(__file__).parent
OUT = ROOT / "dist"

ICON = {
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "folder": '<path d="M3 6a2 2 0 012-2h4l2 2h8a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>',
    "work": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M3 13h18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/>',
    "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "arrow": '<path d="M7 17L17 7M9 7h8v8"/>',
}


def icon(name, size=18):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>')


SOCIAL_SVG = {
    "facebook": '<path fill="currentColor" d="M13.5 22v-8h2.7l.5-3.2h-3.2V8.7c0-.9.3-1.6 1.7-1.6h1.6V4.3c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.1v2.5H7.8V14h2.6v8h3.1z"/>',
    "instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3.8" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/>',
    "tiktok": '<path fill="currentColor" d="M16.6 3c.3 2.3 1.7 3.9 3.9 4.1v3c-1.4.1-2.7-.4-3.9-1.2v6.2c0 3.2-2.6 5.4-5.5 5.4S5.6 18.3 5.6 15.3c0-3.3 2.8-5.6 6.1-5.2v3.1c-1.6-.4-3 .6-3 2.1 0 1.2 1 2.2 2.2 2.2 1.4 0 2.3-1 2.3-2.4V3h3.4z"/>',
}
# Facebook and Instagram open a chat with you; TikTok only has a profile page.
SOCIAL_URL = {
    "facebook": ("Message me on Facebook", "https://m.me/{u}"),
    "instagram": ("Message me on Instagram", "https://ig.me/m/{u}"),
    "tiktok": ("Visit my TikTok", "https://www.tiktok.com/@{u}"),
}
INVERT = {"github", "express", "nextjs", "flask", "django", "markdown", "vercel"}
CARD_COLORS = [
    "linear-gradient(135deg,#1c1c1f,#3a3a40)",
    "linear-gradient(135deg,#9a9aa2,#d9d9de)",
    "linear-gradient(135deg,#c98a4b,#f0c58f)",
    "linear-gradient(135deg,#0f5c4a,#1f9a7a)",
]

CSS = """
:root{--bg:#000;--ink:#fff;--muted:#b9b9b9;--accent:#ffb300;--line:#2b2b2b;
  --font:"Outfit","Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 1.05rem/1.6 var(--font);overflow-x:hidden}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:6px}
.bg{position:fixed;right:0;bottom:0;height:88vh;max-width:100vw;z-index:-1;pointer-events:none;display:flex;
  transition:filter .7s ease,opacity .7s ease;animation:bg-in 1.4s .3s both}
.bg.glow{width:min(60vw,720px);right:-8vw;bottom:-6vh;background:radial-gradient(closest-side,rgba(40,110,255,.35),transparent 70%)}
.bg img{height:100%;width:auto;max-width:100%;object-fit:cover;filter:brightness(.92) contrast(1.05);
  -webkit-mask-image:radial-gradient(ellipse 85% 92% at 50% 100%,#000 48%,transparent 100%);
  mask-image:radial-gradient(ellipse 85% 92% at 50% 100%,#000 48%,transparent 100%)}
body:not([data-sec="home"]) .bg{filter:blur(14px);opacity:.45}
@keyframes bg-in{from{opacity:0;transform:translateX(60px)}to{opacity:1;transform:none}}
section{min-height:100vh;min-height:100svh;padding:5rem max(clamp(1.3rem,6vw,6rem),env(safe-area-inset-left)) 8rem max(clamp(1.3rem,6vw,6rem),env(safe-area-inset-right));display:flex;flex-direction:column;justify-content:center;max-width:62rem}
h2{font:700 clamp(2rem,4.5vw,2.8rem)/1.1 var(--font);color:var(--accent);margin:0 0 1rem}
h3{font:600 1.35rem var(--font);color:var(--accent);margin:2rem 0 1rem}
.p{max-width:38rem;color:#e6e6e6}
#home{max-width:none;position:relative}
.top{position:absolute;top:1.4rem;left:clamp(1.3rem,6vw,6rem);right:clamp(1.3rem,6vw,6rem);display:flex;justify-content:space-between;align-items:center}
.avail{display:flex;gap:.5rem;align-items:center;font-weight:500;font-size:.95rem}
.avail i{width:.5rem;height:.5rem;border-radius:50%;background:#22e06b;box-shadow:0 0 8px #22e06b}
.btn{background:var(--accent);color:#000;text-decoration:none;font-weight:600;padding:.5rem 1.1rem;border-radius:999px;font-size:.9rem;border:0;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(1.1)}
.role{color:var(--accent);font-weight:600;font-size:1.2rem;margin:0 0 .2rem;animation:slide-up 1.2s .2s both}
h1{font:700 clamp(3rem,9vw,5.6rem)/1 var(--font);margin:0 0 1.6rem;letter-spacing:-.02em;animation:slide-in 1.2s .3s both}
.info{display:grid;grid-template-columns:repeat(2,max-content);gap:.8rem 2.5rem;color:#ddd;font-size:.98rem;animation:slide-up 1.2s .6s both}
.info span{display:flex;gap:.55rem;align-items:center}
.info svg{color:var(--accent)}
@keyframes slide-in{from{opacity:0;transform:translateX(-50px)}to{opacity:1;transform:none}}
@keyframes slide-up{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.tl{border-left:2px solid var(--accent);padding-left:1rem;display:grid;gap:1rem;max-width:34rem}
.tl b{display:block;font-weight:600}
.tl small{display:block;color:var(--accent);font-size:.9rem}
.tl a{display:inline-flex;gap:.3rem;align-items:center;width:max-content;margin-top:.15rem;font-size:.9rem;color:#fff;text-decoration:underline;text-underline-offset:3px}
.tl a:hover{color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.3rem 1.2rem;max-width:44rem}
.card{display:block;text-decoration:none}
.card .img{aspect-ratio:4/3;border-radius:14px;position:relative;overflow:hidden;display:grid;place-items:center;font-weight:700;font-size:1.3rem;color:rgba(255,255,255,.85);transition:transform .25s}
.card:hover .img{transform:translateY(-4px)}
.card .img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.card .img svg{position:absolute;top:.7rem;right:.7rem;color:#fff}
.card b{display:block;margin-top:.6rem;font-weight:600}
.card small{color:var(--muted)}
ul.roles{list-style:none;padding:0;margin:0 0 2rem;display:grid;gap:.3rem}
ul.roles li{display:flex;gap:.7rem;align-items:center}
ul.roles li:before{content:"";width:.4rem;height:.4rem;border-radius:50%;background:var(--accent)}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(5rem,1fr));gap:1.2rem 1rem;max-width:34rem}
.tool{display:grid;justify-items:center;gap:.35rem;font-size:.78rem}
.tool img,.tool svg{width:2.6rem;height:2.6rem;object-fit:contain}
.tool img.inv{filter:invert(1)}
form{display:grid;gap:1rem;max-width:32rem;margin-top:.5rem}
label{display:grid;gap:.3rem;font-weight:500}
input,textarea{font:inherit;color:#fff;background:#111;border:1.5px solid #333;border-radius:10px;padding:.7rem .85rem}
input:focus,textarea:focus{border-color:var(--accent);outline:none}
textarea{min-height:8rem;resize:vertical}
.hp{position:absolute;left:-9999px}
.form-status{margin:0;min-height:1.5em;font-weight:500}
.form-status.ok{color:#22e06b}
.form-status.err{color:#ff6b6b}
.socials{display:flex;gap:.8rem;margin-top:2.2rem}
.socials a{width:2.6rem;height:2.6rem;border-radius:50%;background:var(--accent);color:#000;display:grid;place-items:center;transition:transform .2s}
.socials a:hover{transform:scale(1.1)}
footer{color:var(--muted);font-size:.85rem;margin-top:1.4rem}
nav{position:fixed;left:50%;bottom:calc(1rem + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:10;
  display:flex;gap:.2rem;padding:.35rem;border-radius:999px;background:rgba(28,28,28,.82);backdrop-filter:blur(10px);border:1px solid #2a2a2a}
nav a{display:flex;align-items:center;gap:.4rem;padding:.55rem .9rem;border-radius:999px;text-decoration:none;font-size:.85rem;font-weight:500;color:#fff;transition:background .25s,color .25s}
nav a.on{background:#fff;color:#000}
.thanks{min-height:100vh;min-height:100svh;display:grid;place-content:center;text-align:center;gap:1rem;padding:2rem}
@media (min-width:1700px){
  body{font-size:1.15rem}
  section{max-width:72rem}
  .grid{max-width:52rem}
}
@media (max-width:900px){
  section{padding-top:4.5rem}
  .grid{max-width:none}
  .bg{height:70vh;opacity:.9}
}
@media (max-width:620px){
  nav a{padding:.55rem .7rem}
  nav a span{display:none}
  nav a.on span{display:inline}
  .info{grid-template-columns:1fr}
  .bg{height:56vh;opacity:.85}
  #home{justify-content:flex-start;padding-top:6.5rem}
  .top{top:1rem}
  .btn{padding:.45rem .9rem}
}
@media (max-width:380px){
  .grid{grid-template-columns:1fr}
  .tools{grid-template-columns:repeat(auto-fill,minmax(4.2rem,1fr))}
  nav a{padding:.5rem .55rem}
}
@media (pointer:coarse){
  nav a{min-height:44px;min-width:44px;justify-content:center}
  .btn,button{min-height:44px;display:inline-flex;align-items:center}
  .socials a{width:3rem;height:3rem}
}
@media (max-height:520px) and (orientation:landscape){
  section{min-height:auto;padding-top:4rem;padding-bottom:6rem}
  #home{min-height:100vh}
  nav{bottom:.5rem}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
"""

JS = """
const links=[...document.querySelectorAll('nav a')];
const obs=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){
  document.body.dataset.sec=en.target.id;
  links.forEach(l=>l.classList.toggle('on',l.getAttribute('href')==='#'+en.target.id));}});},{threshold:.5});
document.querySelectorAll('section').forEach(s=>obs.observe(s));

const form=document.querySelector('form[name="contact"]');
if(form){
  const status=form.querySelector('.form-status');
  const btn=form.querySelector('button[type="submit"]');
  form.addEventListener('submit',async ev=>{
    ev.preventDefault();
    btn.disabled=true;status.className='form-status';status.textContent='Sending...';
    try{
      const res=await fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:new URLSearchParams(new FormData(form)).toString()});
      if(!res.ok) throw new Error(res.status);
      form.reset();status.className='form-status ok';status.textContent='Message sent. Thank you! I will reply to your email soon.';
    }catch(err){
      status.className='form-status err';status.textContent='Sorry, the message could not be sent. Please try again or use the social buttons.';
    }
    btn.disabled=false;
  });
}
"""

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#000000">
<meta name="color-scheme" content="dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
"""


def timeline(items):
    def row(i):
        link = ""
        if i.get("link"):
            link = (f'<a href="{e(i["link"])}" target="_blank" rel="noopener">'
                    f'{e(i.get("link_text", "View"))} {icon("arrow", 14)}</a>')
        return f'<div><b>{e(i["title"])}</b><small>{e(i["detail"])}</small>{link}</div>'

    rows = "".join(row(i) for i in items)
    return f'<div class="tl">{rows}</div>' if rows else ""


def projects():
    cards = []
    for n, p in enumerate(d.PROJECTS):
        bg = CARD_COLORS[n % len(CARD_COLORS)]
        inner = f'<img src="{e(p["image"])}" alt="" loading="lazy">' if p.get("image") else e(p["title"])
        arrow = icon("arrow", 18) if p.get("link") else ""
        tag, extra = ("a", f' href="{e(p["link"])}" target="_blank" rel="noopener"') if p.get("link") else ("div", "")
        cards.append(
            f'<{tag} class="card"{extra}><div class="img" style="background:{bg}">{inner}{arrow}</div>'
            f'<b>{e(p["title"])}</b><small>{e(p["desc"])}</small></{tag}>'
        )
    return "".join(cards)


def _t(txt, size, fill, y=16):
    return (f'<text x="12" y="{y}" text-anchor="middle" font-size="{size}" font-weight="700" '
            f'font-family="Arial,Helvetica,sans-serif" fill="{fill}">{txt}</text>')


# Built-in logos (simplified) so the skill pictures work offline and never break.
TOOL_SVG = {
    "html5": ('0 0 24 24', '<path d="M3 2h18l-1.6 18L12 22l-7.4-2z" fill="#E44D26"/>'
              '<path d="M12 20.3l5.9-1.6L19.3 4H12z" fill="#F16529"/>' + _t("5", 12, "#fff", 15.5)),
    "css3": ('0 0 24 24', '<path d="M3 2h18l-1.6 18L12 22l-7.4-2z" fill="#1572B6"/>'
             '<path d="M12 20.3l5.9-1.6L19.3 4H12z" fill="#33A9DC"/>' + _t("3", 12, "#fff", 15.5)),
    "javascript": ('0 0 24 24', '<rect x="2" y="2" width="20" height="20" rx="2" fill="#F7DF1E"/>'
                   + '<text x="21" y="20" text-anchor="end" font-size="9.5" font-weight="700" '
                     'font-family="Arial,Helvetica,sans-serif" fill="#111">JS</text>'),
    "php": ('0 0 24 24', '<ellipse cx="12" cy="12" rx="11" ry="6.5" fill="#777BB4"/>' + _t("php", 7.5, "#fff", 14.6)),
    "c": ('0 0 24 24', '<polygon points="12,1.5 21.2,6.75 21.2,17.25 12,22.5 2.8,17.25 2.8,6.75" fill="#00599C"/>'
          + _t("C", 12, "#fff", 16.2)),
    "python": ('0 0 24 24',
               '<path fill="#3776AB" d="M11.9 2C7.3 2 7.6 4 7.6 4v2.1H12v.7H5.8S2.5 6.4 2.5 12s2.9 5.4 2.9 5.4h1.7v-2.6s-.1-2.9 2.9-2.9h4.9s2.7 0 2.7-2.6V4.8S18 2 11.9 2zM9.3 3.6a.9.9 0 110 1.8.9.9 0 010-1.8z"/>'
               '<path fill="#FFD43B" d="M12.1 22c4.6 0 4.3-2 4.3-2v-2.1H12v-.7h6.2s3.3.4 3.3-5.2-2.9-5.4-2.9-5.4h-1.7v2.6s.1 2.9-2.9 2.9H9.1s-2.7 0-2.7 2.6v4.4S6 22 12.1 22zm2.6-1.6a.9.9 0 110-1.8.9.9 0 010 1.8z"/>'),
    "mysql": ('0 0 24 24', '<rect x="1.5" y="4" width="21" height="16" rx="4" fill="#00618A"/>'
              '<text x="12" y="15.2" text-anchor="middle" font-size="6" font-weight="700" '
              'font-family="Arial,Helvetica,sans-serif"><tspan fill="#F29111">My</tspan><tspan fill="#fff">SQL</tspan></text>'),
    "github": ('0 0 24 24', '<path fill="#fff" d="M12 .3a12 12 0 00-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.700-.3-5.500-1.300-5.500-5.900 0-1.300.5-2.400 1.200-3.200-.1-.3-.5-1.500.1-3.200 0 0 1-.3 3.300 1.200a11.500 11.500 0 016 0c2.300-1.500 3.300-1.200 3.300-1.200.6 1.700.2 2.900.1 3.200.8.800 1.200 1.900 1.200 3.200 0 4.600-2.800 5.600-5.500 5.900.4.400.8 1.100.8 2.200v3.300c0 .3.2.7.8.6A12 12 0 0012 .3"/>'),
    "git": ('0 0 24 24', '<rect x="4.2" y="4.2" width="15.6" height="15.6" rx="2" transform="rotate(45 12 12)" fill="#F05032"/>'
            '<g stroke="#fff" stroke-width="1.5" fill="#fff" stroke-linecap="round"><path d="M9.200 8.300v7.400M9.200 9l5.300 3.400" fill="none"/>'
            '<circle cx="9.200" cy="8.300" r="1.500"/><circle cx="9.200" cy="15.700" r="1.500"/><circle cx="14.600" cy="12.400" r="1.500"/></g>'),
    "figma": ('0 0 38 57',
              '<path fill="#F24E1E" d="M0 9.500A9.500 9.500 0 0 1 9.500 0H19v19H9.500A9.500 9.500 0 0 1 0 9.500z"/>'
              '<path fill="#FF7262" d="M19 0h9.500a9.500 9.500 0 0 1 0 19H19z"/>'
              '<path fill="#A259FF" d="M0 28.500A9.500 9.500 0 0 1 9.500 19H19v19H9.500A9.500 9.500 0 0 1 0 28.500z"/>'
              '<circle fill="#1ABCFE" cx="28.500" cy="28.500" r="9.500"/>'
              '<path fill="#0ACF83" d="M0 47.500A9.500 9.500 0 0 1 9.500 38H19v9.500a9.500 9.500 0 0 1-19 0z"/>'),
}


def tools():
    out = []
    for label, slug in d.TOOLS:
        if slug in TOOL_SVG:
            vb, body = TOOL_SVG[slug]
            pic = f'<svg viewBox="{vb}" role="img" aria-label="{e(label)}">{body}</svg>'
        else:  # any other tool: fetch its logo from the devicon CDN
            cls = ' class="inv"' if slug in INVERT else ""
            url = f"https://cdn.jsdelivr.net/gh/devicons/devicon@v2.16.0/icons/{slug}/{slug}-original.svg"
            pic = f'<img{cls} src="{url}" alt="{e(label)}" loading="lazy">'
        out.append(f'<div class="tool">{pic}<span>{e(label)}</span></div>')
    return "".join(out)


def socials():
    out = []
    for key, (label, url) in SOCIAL_URL.items():
        user = d.SOCIALS.get(key, "").strip().lstrip("@")
        if user:
            out.append(
                f'<a href="{e(url.format(u=user))}" target="_blank" rel="noopener" aria-label="{label}" title="{label}">'
                f'<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">{SOCIAL_SVG[key]}</svg></a>'
            )
    return "".join(out)


def index_html():
    has_photo = (ROOT / d.PHOTO).exists()
    has_resume = (ROOT / d.RESUME_FILE).exists()
    photo = f'<img src="{e(d.PHOTO)}" alt="">' if has_photo else ""
    resume_btn = f'<a class="btn" href="{e(d.RESUME_FILE)}" download>Download Resume</a>' if has_resume else ""
    avail = '<span class="avail"><i></i>Available for work</span>' if d.AVAILABLE else "<span></span>"
    info_items = "".join(
        f"<span>{icon(ic)}{e(val)}</span>"
        for ic, val in (("mail", d.EMAIL), ("phone", d.PHONE), ("cap", d.SCHOOL), ("pin", d.LOCATION))
        if val
    )
    projects_section = (
        f'<section id="projects"><h2>Projects</h2><div class="grid">{projects()}</div></section>'
        if d.PROJECTS else ""
    )
    exp = f"<h3>Experience</h3>{timeline(d.EXPERIENCE)}" if d.EXPERIENCE else ""

    nav = [("home", "Home", "home"), ("about", "About", "user")]
    if d.PROJECTS:
        nav.append(("projects", "Projects", "folder"))
    nav += [("skills", "Skills", "work"), ("contact", "Contact", "mail")]
    nav_html = "".join(
        f'<a href="#{i}"{" class=on" if i == "home" else ""}>{icon(ic)}<span>{t}</span></a>' for i, t, ic in nav
    )
    return (
        HEAD.format(title=f"{e(d.NAME)} - {e(d.ROLE)}", desc=e(d.SUMMARY), css=CSS)
        + f"""<body data-sec="home">
<div class="bg{"" if has_photo else " glow"}" aria-hidden="true">{photo}</div>
<main>
<section id="home">
  <div class="top">{avail}{resume_btn}</div>
  <p class="role">{e(d.ROLE)}</p>
  <h1>{e(d.NAME)}</h1>
  <div class="info">
    {info_items}
  </div>
</section>
<section id="about">
  <h2>About</h2>
  <p class="p">{e(d.SUMMARY)}</p>
  <h3>Education &amp; Certificates</h3>
  {timeline(d.EDUCATION)}
  {exp}
</section>
{projects_section}
<section id="skills">
  <h2>Skills &amp; Tools</h2>
  <ul class="roles">{"".join(f"<li>{e(r)}</li>" for r in d.ROLES)}</ul>
  <div class="tools">{tools()}</div>
</section>
<section id="contact">
  <h2>Send me a message</h2>
  <form name="contact" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="contact">
    <p class="hp"><label>Leave this empty <input name="bot-field"></label></p>
    <label>Your name <input type="text" name="name" required autocomplete="name"></label>
    <label>Your email <input type="email" name="email" required autocomplete="email"></label>
    <label>Message <textarea name="message" required></textarea></label>
    <button class="btn" type="submit">Send message</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
  <div class="socials">{socials()}</div>
  <footer>&copy; {e(d.NAME)}. All rights reserved.</footer>
</section>
</main>
<nav aria-label="Sections">{nav_html}</nav>
<script>{JS}</script>
</body>
</html>
"""
    )


def thanks_html():
    return (
        HEAD.format(title="Message sent", desc="Message sent", css=CSS)
        + """<body><div class="thanks"><h1 style="font-size:2.6rem;animation:none">Message sent</h1>
<p>Thanks for reaching out. I will reply to the email you gave me.</p>
<p><a class="btn" href="/">Back to the site</a></p></div></body></html>
"""
    )


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / "index.html").write_text(index_html(), encoding="utf-8")
    (OUT / "thanks.html").write_text(thanks_html(), encoding="utf-8")
    print(f"Built site in {OUT}")


if __name__ == "__main__":
    main()
