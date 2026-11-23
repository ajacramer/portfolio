#!/usr/bin/env python3
"""Builds every landing page from template.html + the page data in pages.py.

  python3 -I build.py            -> preview files (images embedded) in ./out/
  python3 -I build.py --repo     -> repo files (images as /images/landing/... paths) in ./repo/
"""
import base64, json, os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import PAGES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "--repo" in sys.argv
T = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
BR = '<br class="br-d">'


def img_url(path):
    if not path:
        return None
    if REPO:
        return 'url("/images/landing/%s")' % os.path.basename(path).replace(".jpg", ".webp")
    b64 = base64.b64encode(open(os.path.join(HERE, path), "rb").read()).decode()
    return 'url("data:image/jpeg;base64,%s")' % b64


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("  ", " ").strip()


# ---------- demo: phone ----------
PHONE_HTML = """    <figure class="demo">
      <figcaption class="label">{caption}</figcaption>
      <div class="phone">
        <div class="notch"></div>
        <div class="screen">
          <div class="m-head">
            <div class="m-name">{name}</div>
            <div class="m-meta">{meta}</div>
          </div>
          <div class="m-toggle" role="tablist">
{buttons}
          </div>
          <ul class="m-list" id="mList"></ul>
          <div class="m-order">{button}</div>
        </div>
      </div>
    </figure>"""

PHONE_JS = """  // Sample phone screen ({note})
  const MENUS = {menus};
  const TABS = Object.keys(MENUS);
  const list = document.getElementById("mList");
  function showMenu(key){{
    list.innerHTML = MENUS[key].map(([n,d,p],i) =>
      `<li style="animation-delay:${{i*60}}ms"><b>${{n}}</b>${{p ? `<i>${{p}}</i>` : ""}}<small>${{d}}</small></li>`).join("");
    document.querySelectorAll(".m-toggle button").forEach(b=>{{
      const on = b.dataset.menu === key;
      b.classList.toggle("on", on); b.setAttribute("aria-selected", on);
    }});
  }}
  document.querySelectorAll(".m-toggle button").forEach(b=>b.addEventListener("click",()=>showMenu(b.dataset.menu)));
  showMenu(TABS[0]);

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 2. the sample switches itself until someone taps it
  let auto = null, userTapped = false;
  document.querySelectorAll(".m-toggle button").forEach(b=>b.addEventListener("click",()=>{{ userTapped = true; clearInterval(auto); }}));
  if (!reduce) {{
    new IntersectionObserver(([e])=>{{
      clearInterval(auto);
      if (e.isIntersecting && !userTapped) {{
        auto = setInterval(()=>{{
          const cur = document.querySelector(".m-toggle .on").dataset.menu;
          showMenu(TABS[(TABS.indexOf(cur)+1) % TABS.length]);
        }}, 3800);
      }}
    }},{{threshold:.4}}).observe(document.querySelector(".demo"));
  }}"""


def phone(d):
    buttons = "\n".join(
        '            <button type="button"%s data-menu="%s" role="tab" aria-selected="%s">%s</button>'
        % (' class="on"' if i == 0 else "", key, "true" if i == 0 else "false", label)
        for i, (key, label, _) in enumerate(d["tabs"]))
    menus = "{\n" + ",\n".join(
        "    %s: %s" % (key, json.dumps(items, ensure_ascii=False)) for key, _, items in d["tabs"]) + "\n  }"
    h = PHONE_HTML.format(caption=d["caption"], name=d["name"], meta=d["meta"], buttons=buttons, button=d["button"])
    js = PHONE_JS.format(note=d.get("note", "sample content"), menus=menus)
    return h, js, "", "320px"


# ---------- demo: slide deck ----------
DECK_CSS = """  /* sample slide deck */
  .deck{width:100%;max-width:440px}
  .deck-screen{position:relative;aspect-ratio:16/10;border-radius:14px;overflow:hidden;background:#0E0D20;border:1px solid #2E2B5C;
    box-shadow:0 30px 60px -20px rgba(80,140,155,.45);padding:10px}
  .slides{position:relative;width:100%;height:100%;border-radius:8px;overflow:hidden}
  .slide{position:absolute;inset:0;padding:22px 24px;display:flex;flex-direction:column;justify-content:center;gap:10px;
    opacity:0;transform:translateX(24px);transition:opacity .5s ease,transform .5s cubic-bezier(.2,.7,.2,1)}
  .slide.on{opacity:1;transform:none}
  .slide.gone{opacity:0;transform:translateX(-24px)}
  .slide.s1{background:radial-gradient(circle at 85% 20%,rgba(182,156,255,.45),transparent 50%),linear-gradient(135deg,var(--navy),var(--blue))}
  .slide.s2{background:linear-gradient(135deg,var(--teal-deep),var(--navy))}
  .slide.s3{background:radial-gradient(circle at 15% 85%,rgba(80,140,155,.5),transparent 55%),var(--navy)}
  .slide .k{font-family:"Space Mono";font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal-light)}
  .slide h4{font-family:"League Spartan";font-weight:800;font-size:28px;line-height:1.05}
  .slide ul{list-style:none;display:grid;gap:7px;font-size:14px}
  .slide li:before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--sun);margin-right:9px}
  .slide .sbtn{align-self:flex-start;background:var(--sun);color:var(--ink);font-family:"Space Mono";font-weight:700;font-size:12px;padding:8px 14px;border-radius:999px}
  .deck-nav{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:14px}
  .deck-nav button{width:34px;height:34px;border-radius:50%;border:1px solid #3A3770;background:var(--navy);color:var(--paper);font-size:16px;cursor:pointer;transition:background .2s,border-color .2s}
  .deck-nav button:hover{border-color:var(--sun);background:#2A2754}
  .dots{display:flex;gap:7px}
  .dots i{width:8px;height:8px;border-radius:50%;background:#3A3770;transition:background .3s,transform .3s}
  .dots i.on{background:var(--sun);transform:scale(1.25)}"""

DECK_JS = """  // Sample slide deck (generic sample content)
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const slides = [...document.querySelectorAll(".slide")], dots = document.querySelector(".dots");
  slides.forEach(()=>dots.appendChild(document.createElement("i")));
  let cur = 0, auto = null, userTapped = false;
  function go(n){
    slides[cur].classList.remove("on"); slides[cur].classList.add("gone");
    const prev = cur; setTimeout(()=>slides[prev].classList.remove("gone"), 500);
    cur = (n + slides.length) % slides.length;
    slides[cur].classList.add("on");
    [...dots.children].forEach((d,i)=>d.classList.toggle("on", i===cur));
  }
  slides[0].classList.add("on"); dots.children[0].classList.add("on");
  const stop = ()=>{ userTapped = true; clearInterval(auto); };
  document.querySelector(".dprev").addEventListener("click", ()=>{ stop(); go(cur-1); });
  document.querySelector(".dnext").addEventListener("click", ()=>{ stop(); go(cur+1); });
  if (!reduce) {
    new IntersectionObserver(([e])=>{
      clearInterval(auto);
      if (e.isIntersecting && !userTapped) auto = setInterval(()=>go(cur+1), 3800);
    },{threshold:.4}).observe(document.querySelector(".demo"));
  }"""


def deck(d):
    sl = []
    for i, s in enumerate(d["slides"], 1):
        body = ""
        if s.get("bullets"):
            body += "<ul>" + "".join("<li>%s</li>" % b for b in s["bullets"]) + "</ul>"
        if s.get("line"):
            body += "<p>%s</p>" % s["line"]
        if s.get("button"):
            body += '<span class="sbtn">%s</span>' % s["button"]
        sl.append('          <div class="slide s%d"><span class="k">%s</span><h4>%s</h4>%s</div>' % (i, s["kicker"], s["title"], body))
    h = """    <figure class="demo">
      <figcaption class="label">%s</figcaption>
      <div class="deck">
        <div class="deck-screen"><div class="slides">
%s
        </div></div>
        <div class="deck-nav"><button type="button" class="dprev" aria-label="Previous slide">‹</button><div class="dots"></div><button type="button" class="dnext" aria-label="Next slide">›</button></div>
      </div>
    </figure>""" % (d["caption"], "\n".join(sl))
    return h, DECK_JS, DECK_CSS, "440px"


# ---------- demo: live embed of a real project ----------
EMBED_CSS = """  /* live project embed */
  .embed{width:100%;max-width:440px}
  .embed-screen{position:relative;aspect-ratio:16/10;border-radius:14px;overflow:hidden;background:#0E0D20;border:1px solid #2E2B5C;
    box-shadow:0 30px 60px -20px rgba(80,140,155,.45)}
  .embed-screen:before{content:"Loading the presentation…";position:absolute;inset:0;display:grid;place-items:center;font-family:"Space Mono";font-size:11px;color:var(--muted)}
  .embed-screen iframe{position:absolute;top:0;left:0;width:1280px;height:800px;border:0;transform-origin:0 0;transform:scale(var(--es,.34))}
  .embed-link{display:inline-block;margin-top:14px;font-family:"Space Mono";font-size:12px;color:var(--sun);text-decoration:underline;text-decoration-color:rgba(182,156,255,.45);text-underline-offset:4px}
  .embed-link:hover{text-decoration-color:var(--sun)}"""

EMBED_JS = """  // Live embed of a real project, scaled to fit its frame
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  (function(){
    const scr = document.querySelector(".embed-screen");
    const fit = () => scr.style.setProperty("--es", (scr.clientWidth / 1280).toFixed(4));
    fit(); addEventListener("resize", fit);
  })();"""


def embed(d):
    h = """    <figure class="demo">
      <figcaption class="label">%s</figcaption>
      <div class="embed">
        <div class="embed-screen"><iframe src="%s" title="%s" loading="lazy"></iframe></div>
        <a class="embed-link" href="%s" target="_blank" rel="noopener">%s</a>
      </div>
    </figure>""" % (d["caption"], d["url"], d["caption"], d["url"], d["link_text"])
    return h, EMBED_JS, EMBED_CSS, "440px"


# ---------- demo: link card for a real project ----------
CARD_CSS = """  /* real project card */
  .pcard{display:block;width:100%;max-width:440px;text-decoration:none;color:var(--paper)}
  .pcard-screen{position:relative;aspect-ratio:16/10;border-radius:14px;overflow:hidden;border:1px solid #2E2B5C;
    background:radial-gradient(circle at 85% 18%,rgba(182,156,255,.5),transparent 45%),radial-gradient(circle at 12% 88%,rgba(80,140,155,.55),transparent 50%),linear-gradient(135deg,var(--navy),var(--blue));
    box-shadow:0 30px 60px -20px rgba(80,140,155,.45);display:flex;flex-direction:column;justify-content:flex-end;padding:24px;gap:8px;
    transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s ease}
  .pcard-screen img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .pcard-screen .k{font-family:"Space Mono";font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal-light);position:relative}
  .pcard-screen h4{font-family:"League Spartan";font-weight:800;font-size:28px;line-height:1.05;position:relative}
  .pcard-blurb{margin-top:14px;font-size:15px;color:var(--muted)}
  .pcard-go{display:inline-block;margin-top:12px;font-family:"Space Mono";font-weight:700;font-size:13px;color:var(--sun)}
  .pcard-go:after{content:" →";display:inline-block;transition:transform .25s}
  @media (hover:hover){.pcard:hover .pcard-screen{transform:translateY(-4px);box-shadow:0 36px 70px -20px rgba(182,156,255,.5)}.pcard:hover .pcard-go:after{transform:translateX(4px)}}"""


def card(d):
    img = '<img src="%s" alt="">' % d["image"] if d.get("image") else '<span class="k">Interactive web presentation</span><h4>%s</h4>' % d["title"]
    h = """    <figure class="demo">
      <figcaption class="label">%s</figcaption>
      <a class="pcard" href="%s">
        <div class="pcard-screen">%s</div>
        <p class="pcard-blurb">%s</p>
        <span class="pcard-go">%s</span>
      </a>
    </figure>""" % (d["caption"], d["url"], img, d["blurb"], d["link_text"])
    js = '  // Real project card\n  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;'
    return h, js, CARD_CSS, "440px"


# ---------- page assembly ----------
def build(p):
    s = T
    demo_html, demo_js, demo_css, demo_w = {"phone": phone, "deck": deck, "embed": embed, "card": card}[p["demo"]["type"]](p["demo"])
    ph = p.get("photos", {})

    hero = img_url(ph.get("hero"))
    hero_bg = ('linear-gradient(180deg,rgba(32,30,67,.35),rgba(20,19,42,.55)),%s %s/%s no-repeat' % (hero, ph.get("hero_pos", "center"), ph.get("hero_size", "cover"))) if hero else \
        ('radial-gradient(circle at 62% 38%,rgba(182,156,255,.30),transparent 42%),'
         'radial-gradient(circle at 86% 78%,rgba(80,140,155,.38),transparent 48%),'
         'linear-gradient(140deg,#201E43,#14132A 70%)')
    band = img_url(ph.get("band"))
    band_css = ('  section.band:before{content:"";position:absolute;left:0;top:0;bottom:0;width:52%%;pointer-events:none;\n'
                '    background:linear-gradient(rgba(18,42,51,.6),rgba(18,42,51,.6)),%s %s/cover no-repeat;\n'
                '    -webkit-mask-image:linear-gradient(90deg,#000 35%%,transparent 100%%);mask-image:linear-gradient(90deg,#000 35%%,transparent 100%%)}' % (band, ph.get("band_pos", "30% 35%"))) if band else ""
    proc = img_url(ph.get("process"))
    proc_css = ""
    if proc:
        proc_css = ('  section.process:before{content:"";position:absolute;left:0;right:0;top:-180px;bottom:-180px;z-index:-1;pointer-events:none;\n'
                    '    background:linear-gradient(rgba(20,19,42,.86),rgba(20,19,42,.86)),' + proc + ' ' + ph.get("process_pos", "right 30%") + '/cover no-repeat;\n'
                    '    -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 200px,#000 calc(100% - 200px),transparent 100%);\n'
                    '    mask-image:linear-gradient(180deg,transparent 0,#000 200px,#000 calc(100% - 200px),transparent 100%)}')
    cta = img_url(ph.get("cta")) or "none"

    tiles = "\n".join('      <div class="tile"><h3>%s</h3><p>%s</p></div>' % t for t in p["tiles"])
    promo_tiles = "\n".join('      <div class="tile"><h3>%s</h3><p>%s</p></div>' % t for t in p["promo_tiles"])
    steps = "\n".join('      <li><h3><span class="n%s">%02d</span>%s</h3>%s</li>' % (" lilac" if i % 2 == 0 else "", i, h, d)
                       for i, (h, d) in enumerate(p["steps"], 1))
    faq = "\n".join('    <details%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a)
                    for i, (q, a) in enumerate(p["faq"]))
    band_ps = "\n".join("      <p>%s</p>" % x for x in p["band_ps"])
    if p.get("quiet_link"):
        ql = p["quiet_link"]
        url, text = ql[0], ql[1]
        before, after = (ql[2], ql[3]) if len(ql) > 2 else ("", "")
        band_ps += '\n      <p class="quiet-link">%s<a href="%s">%s</a>%s</p>' % (before, url, text, after)

    area = [{"@type": "AdministrativeArea", "name": "Chester County, PA"},
            {"@type": "AdministrativeArea", "name": "Montgomery County, PA"}]
    url = "https://aja-design.com/web-design/%s/" % p["slug"]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": "https://aja-design.com/#business", "name": "Aja Cramer Designs",
         "url": "https://aja-design.com/", "serviceType": "Website design",
         "address": {"@type": "PostalAddress", "addressLocality": "Downingtown", "addressRegion": "PA", "addressCountry": "US"},
         "areaServed": area},
        {"@type": "Service", "name": p["service"], "provider": {"@id": "https://aja-design.com/#business"},
         "audience": {"@type": "BusinessAudience", "audienceType": p["audience"]}, "areaServed": area},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://aja-design.com/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faq"]]}]}

    words = json.dumps(p["words"], ensure_ascii=False)
    first = p["words"][0][0]
    h1 = p["h1"].replace("{{WORD}}", '<em class="rot" aria-hidden="true">%s</em>' % first)
    h1_aria = strip_tags(p["h1"].replace("{{WORD}}", first))

    rep = {
        "TITLE": html.escape(p["title"], quote=True), "META": html.escape(p["meta"], quote=True), "SLUG": p["slug"],
        "SCHEMA": json.dumps(schema, ensure_ascii=False, indent=2),
        "HERO_BG": hero_bg, "BAND_CSS": band_css, "PROCESS_CSS": proc_css, "CTA_IMG": cta,
        "DEMO_CSS": demo_css, "DEMO_W": "--demo-w:%s" % demo_w, "DEMO_HTML": demo_html, "DEMO_JS": demo_js,
        "PREVIEW_BAR": "" if REPO else '<div class="preview-bar">PREVIEW</div>',
        "LABEL": p["label"], "H1": h1, "H1_ARIA": h1_aria, "HERO_P": p["hero_p"], "HERO_BTN": p["hero_btn"],
        "BAND_H2": p["band_h2"], "BAND_PS": band_ps, "GIVE_H2": p["give_h2"], "TILES": tiles,
        "PROMO_H2": p["promo_h2"], "PROMO_P": p["promo_p"], "PROMO_TILES": promo_tiles, "PROMO_NOTE": p["promo_note"],
        "STEPS": steps, "MID_BTN": p["mid_btn"], "FAQ_HTML": faq,
        "CTA_H2": p["cta_h2"], "CTA_P": p["cta_p"], "SOURCE": p["source"], "BIZ_LABEL": p["biz_label"],
        "SITE_LABEL": p.get("site_label", "Current website"), "WORDS": words, "FORM_BTN": p["form_btn"], "HERO_VARS": "".join("--hero-%s:%s;" % (k, ph['hero_' + k]) for k in ("w", "mask") if ph.get("hero_" + k)), "CTA_POS": "".join("--cta-%s:%s;" % (k, ph['cta_' + k]) for k in ("x", "y") if ph.get("cta_" + k)),
    }
    helps = ["Website design", "Redesign", "Landing page or microsite", "Graphics for email or social", "Presentation", "Something else"]
    pre = "Presentation" if p["slug"] == "presentations" else "Website design"
    rep["HELP_CHIPS"] = "\n".join('          <label><input type="checkbox" name="help" value="%s"%s><span>%s</span></label>' % (h, " checked" if h == pre else "", h) for h in helps)
    rep["MORE_LINKS"] = "\n".join('      <li><a href="/web-design/%s/">%s</a></li>' % (o["slug"], o["nav_label"]) for o in PAGES if o["slug"] != p["slug"])
    for k, v in rep.items():
        s = s.replace("{{%s}}" % k, v)
    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", s)
    assert not left, (p["slug"], left)
    # house rules
    visible = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    assert "—" not in s, "%s: em dash found" % p["slug"]
    return s


HUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Web Design for Local Businesses | Aja Cramer</title>
<meta name="description" content="Website and presentation design by Aja Cramer, a web designer based in Downingtown, PA.">
<link rel="canonical" href="https://aja-design.com/web-design/">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32.png">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<meta name="theme-color" content="#201E43">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;700;800&family=Instrument+Sans:wght@400;500;600&family=Space+Mono:wght@400;700&family=Caveat:wght@600&display=swap" rel="stylesheet">
<style>
  :root{--head:"League Spartan",system-ui,sans-serif;--body:"Instrument Sans",system-ui,sans-serif;--hand:"Caveat",cursive;
    --paper:#E7E3F1;--ink:#14132A;--navy:#201E43;--sun:#B69CFF;--teal:#508C9B;--blue:#134B70;--muted:#BFC6D6;--teal-light:#7FB5C2}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--ink);color:var(--paper);font-family:var(--body);line-height:1.6;font-size:17px}
  a{color:inherit}
  .wrap{max-width:1080px;margin:0 auto;padding:0 28px}
  .skip{position:absolute;left:-999px;top:.5rem;background:var(--sun);color:var(--ink);padding:.5rem 1rem;border-radius:6px;font-weight:600}
  .skip:focus{left:.5rem;z-index:50}
  .site-top{position:sticky;top:0;z-index:100;background:rgba(32,30,67,.9);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
  .site-top .wrap{display:flex;align-items:center;justify-content:space-between;height:4.5rem}
  .logo{font-family:var(--head);font-weight:800;font-size:22px;text-decoration:none;white-space:nowrap}
  .logo span{color:var(--sun);transition:color .25s}
  .logo:hover span{color:var(--teal-light)}
  .site-top nav{display:flex;gap:.3rem}
  .site-top nav a{text-decoration:none;font:600 1rem/1 var(--head);padding:.6rem .9rem;border-radius:999px;transition:background .2s,color .2s}
  .site-top nav a:hover{background:var(--blue);color:var(--sun)}
  .hub{padding:56px 0 30px}
  .label{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--teal-light)}
  h1{font-family:var(--head);font-weight:800;font-size:clamp(40px,5.4vw,64px);line-height:1.05;margin:12px 0 30px;text-wrap:balance}
  .cards{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
  .cards a{position:relative;overflow:hidden;isolation:isolate;display:flex;flex-direction:column;gap:8px;height:100%;min-height:260px;text-decoration:none;background:var(--navy);border-radius:16px;padding:22px;border-top:4px solid var(--teal);
    transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s ease}
  .cards a:before{content:"";position:absolute;inset:0;z-index:-2;background:var(--bg,none) center/cover no-repeat;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
  .cards a:after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(32,30,67,.25) 0%,rgba(32,30,67,.72) 50%,rgba(26,24,56,.93) 100%)}
  .cards h2,.cards p{text-shadow:0 1px 12px rgba(20,19,42,.7)}
  .cards p{color:#D8DCE8}
  .cards li:nth-child(even) a{border-top-color:var(--sun)}
  .cards h2{font-family:var(--head);font-size:22px;line-height:1.15}
  .cards p{font-size:15px;color:var(--muted);text-wrap:pretty}
  .cards .go{margin-top:auto;font-family:"Space Mono";font-weight:700;font-size:12px;color:var(--sun)}
  @media (hover:hover){.cards a:hover{transform:translateY(-4px);box-shadow:0 18px 34px -16px rgba(80,140,155,.6)}.cards a:hover:before{transform:scale(1.06)}}
  footer.site-foot{border-top:1px solid rgba(80,140,155,.4);padding:2rem 0 2.6rem;margin-top:40px}
  footer.site-foot .wrap{display:flex;justify-content:space-between;align-items:center;gap:1rem 2rem;flex-wrap:wrap}
  footer.site-foot .made{font:600 1.35rem/1 var(--hand);color:var(--sun)}
  footer.site-foot nav{display:flex;gap:1.25rem;flex-wrap:wrap}
  footer.site-foot nav a{text-decoration:none;color:var(--muted);font-weight:600}
  footer.site-foot nav a:hover{color:var(--sun)}
  footer.site-foot small{color:var(--muted);font-size:.9rem}
  @media (max-width:560px){.site-top nav a{padding:.55rem .55rem;font-size:.95rem}.logo{font-size:18px}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Aja Cramer Designs, home"><span>Aja</span>&nbsp;Cramer&nbsp;<span>Designs</span></a>
    <nav aria-label="Main"><a href="/#work">Work</a><a href="/#about">About</a><a href="/#contact">Contact</a></nav>
  </div>
</header>
<main id="main" class="hub">
  <div class="wrap">
    <div class="label">Based in Downingtown, PA</div>
    <h1>Web design for local businesses</h1>
    <ul class="cards">
%s
    </ul>
  </div>
</main>
<footer class="site-foot">
  <div class="wrap">
    <span class="made">Made with care.</span>
    <nav aria-label="Footer"><a href="/#work">Work</a><a href="/#about">About</a><a href="/#contact">Contact</a><a href="https://www.linkedin.com/in/ajacramer/" rel="noopener">LinkedIn</a></nav>
    <small>Aja | Digital Designer</small>
  </div>
</footer>
</body>
</html>
"""


def build_hub():
    def bg(p):
        u = img_url(p.get("photos", {}).get("hub") or p.get("photos", {}).get("hero"))
        return ' style="--bg:%s"' % u.replace('"', "'") if u else ""
    cards = "\n".join('      <li><a href="/web-design/%s/"%s><h2>%s</h2><p>%s</p><span class="go">See the page →</span></a></li>'
                      % (p["slug"], bg(p), p["nav_label"], html.escape(p["meta"])) for p in PAGES)
    return HUB.replace("%s", cards, 1)


if __name__ == "__main__":
    import shutil
    site = sys.argv[sys.argv.index("--repo") + 1] if REPO else None
    out = os.path.join(site, "web-design") if REPO else os.path.join(HERE, "out")
    os.makedirs(out, exist_ok=True)
    if REPO:
        imgdir = os.path.join(site, "images", "landing")
        os.makedirs(imgdir, exist_ok=True)
        for p in PAGES:
            for k in ("hub", "hero", "band", "process", "cta"):
                if p.get("photos", {}).get(k):
                    from PIL import Image
                    src = os.path.join(HERE, p["photos"][k])
                    Image.open(src).save(os.path.join(imgdir, os.path.basename(src).replace(".jpg", ".webp")), "WEBP", quality=74, method=6)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(build_hub())
        print("built", os.path.join(out, "index.html"))
    for p in PAGES:
        fn = os.path.join(out, ("%s/index.html" % p["slug"]) if REPO else "web-design-%s.html" % p["slug"])
        os.makedirs(os.path.dirname(fn), exist_ok=True)
        open(fn, "w", encoding="utf-8").write(build(p))
        print("built", fn)
