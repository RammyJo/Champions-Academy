#!/usr/bin/env python3
"""Render the school site as standalone HTML pages."""
import json
import os
import shutil
from html import escape as e
from pathlib import Path
from content import *

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
ORIGIN = os.environ.get("SITE_ORIGIN", "https://champions.edu.ph").rstrip("/")
NAV = [
    ("Home", "/", []),
    ("About", "/about/", [("Our story", "/history/"), ("Vision, mission & values", "/values/"), ("Leadership & faculty", "/faculty/")]),
    ("Academics", "/program/", [(p["name"], route) for route, p in PROGRAMS.items()]),
    ("Admissions", "/admissions/", [("Requirements", "/requirements/"), ("Pre-registration", "/pre-register/")]),
    ("School Life", "/school-life/", [("News & events", "/news/")]),
    ("Contact", "/contact/", []),
]
PAGES = {}

def link(label, href, css=""):
    return f'<a class="{e(css)}" href="{e(href)}">{e(label)}</a>'

def button(label, href, css=""):
    return link(label, href, f"button {css}")

def kicker(label):
    return f'<p class="eyebrow">{e(label)}</p>'

def photo(key, sizes="(max-width: 700px) 100vw, 50vw", eager=False):
    alt, ratio = PHOTOS[key]
    widths = PHOTO_WIDTHS.get(key, (480, 960, 1440))
    width = widths[1]
    sources = ", ".join(f"/assets/{key}-{w}.webp {w}w" for w in widths)
    priority = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="/assets/{key}-{width}.webp" srcset="{sources}" sizes="{sizes}" alt="{e(alt)}" width="{width}" height="{round(width/ratio)}" decoding="async" {priority}>'

def section(body, css=""):
    return f'<section class="section {css}"><div class="wrap">{body}</div></section>'

def heading(title, summary, category, parent=None):
    trail = link("Home", "/")
    if parent:
        trail += ' <span aria-hidden="true">/</span> ' + link(*parent)
    return f'<section class="pagehead"><div class="wrap"><nav class="crumb" aria-label="Breadcrumb">{trail} <span aria-hidden="true">/</span> <span aria-current="page">{e(title)}</span></nav>{kicker(category)}<h1>{e(title)}</h1><p>{e(summary)}</p></div></section>'

def page(path, title, summary, body, image_key="celebration"):
    PAGES[path] = (title, summary, body, image_key)

def brand():
    return '<a href="/" class="brand"><img src="/assets/crest.png" width="48" height="48" alt=""><span>Champions Academy<small>San Fernando, La Union</small></span></a>'

def header(path):
    entries = []
    for title, route, children in NAV:
        current = ' aria-current="page"' if route == path else ""
        if children:
            options = [("Overview", route)] + children
            submenu = "".join(f'<li>{link(t, r)}</li>' for t, r in options)
            entries.append(f'<li><details><summary>{e(title)}</summary><ul class="submenu">{submenu}</ul></details></li>')
        else:
            entries.append(f'<li><a href="{route}"{current}>{title}</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
    <div class="utility"><div class="wrap"><span>Christ-centered education in La Union</span>{link("(072) 700 2700","tel:+63727002700")}</div></div>
    <header class="header"><div class="wrap header-row">{brand()}
    <button id="menu" type="button" aria-expanded="false" aria-controls="primary">Menu <span aria-hidden="true">☰</span></button>
    <nav id="primary" aria-label="Primary"><ul class="nav-list">{''.join(entries)}</ul></nav>
    {button("Enroll / Pre-register","/pre-register/","header-cta")}</div></header>'''

def footer():
    return f'''<footer class="footer"><div class="wrap footer-grid">
    <div>{brand()}<p>{e(ADDRESS)}</p><p>{link("(072) 700 2700","tel:+63727002700")} · {link("0976 111 0320","tel:+639761110320")}</p>
    {link("info@champions.edu.ph","mailto:info@champions.edu.ph")}</div>
    <div><h2>Academics</h2>{''.join(link(p["name"],r) for r,p in PROGRAMS.items())}</div>
    <div><h2>For families</h2>{link("Admissions","/admissions/")}{link("Requirements","/requirements/")}{link("News & events","/news/")}{link("Contact","/contact/")}</div>
    <div><h2>Connect</h2>{link("Facebook",FACEBOOK)}{link("Instagram",INSTAGRAM)}{link("Privacy","/privacy/")}</div>
    </div><div class="wrap footer-base"><span>© Champions Academy</span><span>Producing Champions in Life</span></div></footer>'''

def program_cards():
    cards = []
    for route, program in PROGRAMS.items():
        name, stage = program["name"], program["stage"]
        cards.append(f'<article class="program-card">{photo(program["image"], "(max-width: 700px) 100vw, 33vw")}<div>{kicker(stage)}<h3>{e(name)}</h3><p>{e(program["intro"])}</p>{link(f"Explore {name} →",route,"text-link")}</div></article>')
    return '<div class="program-grid">' + "".join(cards) + '</div>'

def values_pair():
    return f'<div class="values-pair"><article>{kicker("01 / Our Vision")}<p>{e(VISION)}</p></article><article>{kicker("02 / Our Mission")}<p>{e(MISSION)}</p></article></div>'

def invitation():
    return section(f'''{kicker("Admissions")}<h2>Applying to Champions Academy</h2>
    <p>Check the requirements for your child’s grade, then submit the school’s pre-registration form.</p>
    <div class="actions">{button("Begin pre-registration","/pre-register/")}{button("View requirements","/requirements/","outline light")}{link("Contact Admissions →","mailto:"+EMAIL,"text-link")}</div>''',"invite")

def gallery():
    return '<div class="gallery">' + "".join(
        f'<figure>{photo(key)}<figcaption>{label}</figcaption></figure>'
        for key, label in [("campus","Our campus in Santiago Norte"),("school-event","A school event"),("classroom-activity","Working on classroom activities")]
    ) + '</div>'

def hero_gallery():
    slides = [
        ("classroom-together", "A classroom at Champions Academy"),
        ("preschool", "Learning together in Preschool"),
        ("junior-high", "Inside a Junior High classroom"),
    ]
    panels = "".join(
        f'<figure class="hero-slide" data-caption="{e(caption)}" {"hidden" if index else ""}>'
        f'{photo(key, "(max-width: 850px) 100vw, 55vw", not index)}</figure>'
        for index, (key, caption) in enumerate(slides)
    )
    return f'''<div class="hero-visual" aria-label="Life at Champions Academy">{panels}
    <div class="hero-controls"><p id="hero-caption" aria-live="polite">{slides[0][1]}</p>
    <div class="hero-buttons" hidden><button type="button" aria-label="Previous photo">←</button>
    <button type="button" aria-label="Next photo">→</button></div></div></div>'''


home = f'''<section class="hero"><div class="hero-copy">{kicker("Champions Academy")}
<h1>Producing<br> Champions<br> <em>in Life.</em></h1>
<p>A Christian school in San Fernando, La Union, serving Nursery through Grade 10.</p>
<div class="actions">{button("View programs","/program/","outline light")}{button("Admissions","/admissions/")}</div>
</div>
{hero_gallery()}</section>'''
home += section('<h2>Academic programs</h2>'+program_cards(),"tint")
home += section(f'<h2>School life</h2>{gallery()}{link("See more of school life →","/school-life/","text-link")}')
page("/", "Producing Champions in Life", "A Christ-centered learning community in San Fernando, La Union, with Preschool, Grade School and Junior High School.", home+invitation())

def standard(route, title, intro, category, body, parent=None, image_key="celebration"):
    page(route,title,intro,heading(title,intro,category,parent)+body,image_key)

standard("/about/","About Champions Academy","Christian education shaped by faith, active learning, and close partnership with families.","About",
    section(f'''<div class="split"><div><h2>How children learn</h2><p>Children come to school curious and capable. At Champions Academy, they build understanding by asking questions, working together, and connecting what they learn to everyday life.</p>
    <p>Teachers and families share responsibility for helping children develop academic skills and grow in Christian character.</p></div>{photo("campus")}</div>''')+
    section(f'<h2>Get to know the school</h2><div class="actions">{button("Our story","/history/")}{button("Vision, mission & values","/values/","outline")}{button("Leadership & faculty","/faculty/","outline")}</div>',"tint"))

standard("/history/","Our story","From a community outreach to a school serving children from Preschool through Junior High.","About",
    section('''<ol class="timeline"><li><strong>1992</strong><div><h2>San Fernando Christian Community</h2><p>Missionary Timothy Lee Warden and a team of local Christians established the community that gave rise to the school.</p></div></li>
    <li><strong>2004</strong><div><h2>Make Kids Smile Foundation</h2><p>Timothy and Bambi Warden founded the outreach to support children through health, education, and feeding programs.</p></div></li>
    <li><strong>2016</strong><div><h2>Champions Academy opens</h2><p>The school began with a small group of students and grew to offer early education, elementary, and junior high levels.</p></div></li></ol>'''),("About","/about/"))

standard("/values/","Vision, mission & values","The commitments that guide teaching and formation at Champions Academy.","About",
    section(values_pair())+section('''<div class="reading"><h2>Values in our institutional materials</h2>
    <p>The school’s published core-values graphic names Grace, Commitment to Growth, Leadership Reproduction, Excellence, and Family.</p>
    <p>Its homepage also highlights Christ-likeness, Honoring, Integrity, Leadership, and Discipline.</p></div>''',"tint"),("About","/about/"))

def faculty_directory():
    if not FACULTY:
        return f'<div class="notice"><h2>Meet the people behind the school</h2><p>Contact the school office for current leadership, administration, and teaching staff information.</p>{button("Contact the school","/contact/")}</div>'
    groups = {}
    for profile in FACULTY:
        groups.setdefault(profile["group"], []).append(profile)
    blocks = []
    for group, profiles in groups.items():
        cards = []
        for profile in profiles:
            portrait = profile.get("portrait")
            photo_tag = f'<img src="/assets/{e(portrait)}" alt="" width="240" height="240" loading="lazy">' if portrait else ""
            cards.append(f'<article>{photo_tag}<h3>{e(profile["name"])}</h3><p>{e(profile["role"])}</p></article>')
        blocks.append(f'<h2>{e(group)}</h2><div class="profile-grid">{"".join(cards)}</div>')
    return "".join(blocks)

standard("/faculty/","Leadership & faculty","Our educators help children build knowledge, develop character, and practice Christian values.","About",
    section(faculty_directory()),("About","/about/"))
standard("/program/","Academic programs","A Christ-centered education from the first years of school through Junior High.","Academics",
    section('<h2>Explore by school level</h2>'+program_cards())+invitation())
for route,p in PROGRAMS.items():
    items = "".join(f'<article><h3>{e(title)}</h3><p>{e(copy)}</p></article>' for title,copy in p["areas"])
    body = section(f'<div class="program-detail"><figure>{photo(p["image"],"(max-width: 700px) 100vw, 55vw",True)}</figure><div>{kicker(p["stage"])}<h2>What children learn</h2><div class="area-list">{items}</div></div></div>',p["image"])
    body += section(f'<div class="notice"><h2>Entry guidance</h2><p>{e(p["guidance"])}</p>{button("Review requirements","/requirements/")} {link("Ask Admissions →","mailto:"+EMAIL,"text-link")}</div>',"tint")
    standard(route,p["name"],p["intro"],p["stage"],body,("Academics","/program/"),p["image"])

steps = [
    ("Explore the programs","Find the right school level for your child.","/program/"),
    ("Review requirements","See the published checklist and confirm which documents apply.","/requirements/"),
    ("Complete pre-registration","Use the school’s Google Form to provide learner information.","/pre-register/"),
    ("Ask about next steps","Contact Admissions for help with placement, documents, or enrollment status.","mailto:"+EMAIL),
]
standard("/admissions/","Admissions","Start with your child’s school level and work through each step at your own pace.","Join Champions Academy",
    section('<h2>How to get started</h2><ol class="steps">'+''.join(f'<li><h3>{link(title,route)}</h3><p>{e(copy)}</p></li>' for title,copy,route in steps)+'</ol>')+invitation())
standard("/requirements/","Admission requirements","Use the school’s published checklist to prepare for your child’s application.","Admissions",
    section('<div class="reading"><h2>Document checklist</h2><p>Ask Admissions to confirm the current requirements for your child’s grade and circumstances.</p><ul class="checklist">'+
        ''.join(f'<li><strong>{e(label)}</strong><p>{e(copy)}</p></li>' for label,copy in REQUIREMENTS)+'</ul>'+
        f'<div class="actions">{button("Continue to pre-registration","/pre-register/")}{link("Ask Admissions","mailto:"+EMAIL,"text-link")}</div></div>'),("Admissions","/admissions/"))
standard("/pre-register/","Pre-registration","Parents and guardians can start through the Google Form linked by Champions Academy.","Admissions",
    section(f'''<div class="split enrollment"><div><h2>Open the school’s registration form</h2>
    <p>Have your child’s learner information ready. You’ll continue to Google Forms to complete the school’s pre-registration step.</p>
    <p>After completing the form, contact Admissions for guidance on placement, supporting documents, and the remaining enrollment steps.</p>
    {button("Open official Google Form ↗",FORM)}</div><aside class="notice"><h2>Before you begin</h2>
    <p>Review the school’s published requirements and ask Admissions about current intake, eligibility, or how learner information is handled.</p>
    {link("Review requirements →","/requirements/","text-link")}{link("Registration privacy →","/privacy/","text-link")}{link("Email Admissions →","mailto:"+EMAIL,"text-link")}</aside></div>'''),("Admissions","/admissions/"))

standard("/school-life/","School life","See the campus and some of the ways students learn and take part in school activities.","Campus & community",
    section('<h2>Campus and learning environment</h2>'+gallery()+link("See news and events →","/news/","text-link")),image_key="campus")
def announcements():
    if not ANNOUNCEMENTS:
        return f'<div class="notice"><h2>School updates</h2><p>For current announcements and events, visit the school’s official Facebook page or contact the school office.</p>{button("Visit Champions Academy on Facebook ↗",FACEBOOK)}</div>'
    return "".join(f'<article class="notice"><time datetime="{e(a["date"])}">{e(a["date"])}</time><h2>{e(a["title"])}</h2><p>{e(a["summary"])}</p></article>'
                   for a in sorted(ANNOUNCEMENTS,key=lambda a:a["date"],reverse=True))
standard("/news/","News & events","Announcements and activities from the Champions Academy community.","School life",section(kicker("Latest updates")+announcements(),"news-current"),("School life","/school-life/"))

archive_entries = []
for date, slug, title, summary in ARCHIVE:
    route = "/blog/" + date.replace("-", "/") + "/" + slug + "/"
    standard(route,title,summary,"From the 2017 archive",section(link("Back to the news archive →","/news/#archive","text-link")),("News & events","/news/"))
    archive_entries.append(f'<li><time datetime="{date}">{date}</time>{link(title+" →",route)}</li>')
title, summary, body, key = PAGES["/news/"]
page("/news/",title,summary,body+section('<h2 id="archive">From the 2017 archive</h2><ul class="archive-list">'+''.join(archive_entries)+'</ul>',"tint"),key)

directory = [
    ("General inquiries","info@champions.edu.ph"),("Enrollment",EMAIL),
    ("Technical support","tech@champions.edu.ph"),("Financial transactions","finance@champions.edu.ph"),
]
standard("/contact/","Contact Champions Academy","Get in touch with the school office or find the campus in Santiago Norte.","Contact",
    section(f'''<div class="split"><div><h2>School office</h2><address>{e(ADDRESS)}</address>
    <p>Monday–Friday, 8:00 AM–4:00 PM</p>
    <p>{link("(072) 700 2700","tel:+63727002700","text-link")}<br>{link("0976 111 0320","tel:+639761110320","text-link")}</p>
    <div class="actions">{button("Get directions ↗",MAP)}{link("Ask Admissions →","mailto:"+EMAIL,"text-link")}</div></div>{photo("campus")}</div>''')+
    section('<h2>Email directory</h2><dl class="directory">'+''.join(f'<div><dt>{label}</dt><dd>{link(email,"mailto:"+email)}</dd></div>' for label,email in directory)+'</dl>',"tint"),image_key="campus")

standard("/privacy/","Website & registration privacy","Information for parents and guardians using this website and the school’s pre-registration link.","For families",
    section(f'''<div class="reading"><h2>Public website</h2><p>The public pages use no registration fields or analytics scripts. Contact links open your phone or email application.</p>
    <h2>Registration through Google Forms</h2><p>Pre-registration opens a school-linked Google Form, where the school requests learner information for admissions. Review the form before entering information and contact Admissions about how it is used, who can access it, and how long it is kept.</p>
    <h2>Questions about learner information</h2><p>Parents and guardians can contact the school at {link("info@champions.edu.ph","mailto:info@champions.edu.ph")} for its current privacy notice and guidance on access or correction requests.</p></div>'''))
standard("/summer-class/","Summer classes","Ask the school about current summer offerings and registration dates.","Programs",
    section(f'<div class="notice"><h2>Check availability</h2><p>Contact Admissions to confirm whether a summer program is open and which age groups it serves.</p>{button("Ask Admissions","mailto:"+EMAIL)}</div>'))

REDIRECTS = {
    "/home/gradeschool/": "/grade-school/",
    "/home/": "/",
    "/blog/": "/news/",
    "/blog/2017/10/18/quick-preview-of-the-nursery-class/": "/preschool/",
}
def document(path, title, summary, body, key, missing=False):
    canonical = ORIGIN+path
    full_title = f"{title} | Champions Academy"
    meta = '<meta name="robots" content="noindex">' if missing else f'<link rel="canonical" href="{e(canonical)}">'
    schema = {"@context":"https://schema.org","@type":"School","name":NAME,"url":ORIGIN+"/",
              "address":{"@type":"PostalAddress","streetAddress":"F. Ortega Highway, Santiago Norte","addressLocality":"City of San Fernando","addressRegion":"La Union","addressCountry":"PH"},
              "logo":ORIGIN+"/assets/crest.png","telephone":"+63 72 700 2700","sameAs":[FACEBOOK,INSTAGRAM]}
    return f'''<!doctype html><html lang="en-PH"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(full_title)}</title>
<meta name="description" content="{e(summary)}">{meta}
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(summary)}">
<meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(ORIGIN)}/assets/{key}-960.webp">
<link rel="icon" href="/assets/crest.png"><link rel="stylesheet" href="/styles.css?v=interaction-1">
<script type="application/ld+json">{json.dumps(schema)}</script><script src="/navigation.js?v=interaction-1" defer></script>
</head><body>{header(path)}<main id="main" tabindex="-1">{body}</main>{footer()}</body></html>'''

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT/"static",DIST)
    for path,(title,summary,body,key) in PAGES.items():
        target = DIST/path.strip("/")/"index.html"
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(document(path,title,summary,body,key),encoding="utf-8")
    (DIST/"404.html").write_text(document("/404.html","Page not found","Find your way back to Champions Academy.",heading("Page not found","This address may have moved.","Champions Academy")+section(button("Return home","/")),"celebration",True),encoding="utf-8")
    (DIST/"_redirects").write_text("".join(f"{alias} {target} 301\n{alias.rstrip('/')} {target} 301\n" for alias,target in REDIRECTS.items()))
    urls = "".join(f"<url><loc>{e(ORIGIN+path)}</loc></url>" for path in PAGES)
    (DIST/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (DIST/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
    print(f"Built {len(PAGES)} routes and a 404 page in {DIST}")

if __name__ == "__main__":
    build()
