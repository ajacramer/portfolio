"""Mobile menu (hamburger) shared by every page. build.py inserts it into the generated pages;
apply_static() inserts it into the hand-built pages (home, case studies) once."""

BTN = ('<button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu">'
       '<span></span><span></span><span></span></button>')

CSS = """/* mobile menu */
.menu-btn{display:none}
@media (max-width:640px){
  header.top .wrap,header.site-top .wrap{position:relative}
  .menu-btn{display:grid;place-content:center;gap:5px;width:44px;height:44px;margin-right:-8px;border:0;border-radius:12px;background:transparent;color:var(--paper);cursor:pointer;-webkit-tap-highlight-color:transparent}
  .menu-btn span{display:block;width:22px;height:2.5px;border-radius:2px;background:currentColor;transition:transform .3s cubic-bezier(.2,.8,.2,1),opacity .2s}
  .menu-btn:focus-visible{outline:2px solid var(--sun);outline-offset:2px}
  .menu-open .menu-btn span:nth-child(1){transform:translateY(7.5px) rotate(45deg)}
  .menu-open .menu-btn span:nth-child(2){opacity:0}
  .menu-open .menu-btn span:nth-child(3){transform:translateY(-7.5px) rotate(-45deg)}
  header.top nav#main-nav,header.site-top nav#main-nav{position:absolute;top:100%;left:0;right:0;display:flex;flex-direction:column;gap:.15rem;
    padding:.6rem var(--gutter,16px) 1.1rem;background:rgba(32,30,67,.98);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
    border-bottom:1px solid rgba(80,140,155,.4);box-shadow:0 18px 30px -18px rgba(20,19,42,.9);
    visibility:hidden;opacity:0;transform:translateY(-8px);transition:opacity .25s ease,transform .3s cubic-bezier(.2,.8,.2,1),visibility 0s .3s}
  .menu-open nav#main-nav{visibility:visible!important;opacity:1!important;transform:none!important;transition:opacity .25s ease,transform .3s cubic-bezier(.2,.8,.2,1)!important}
  header.top nav#main-nav a,header.site-top nav#main-nav a{font:700 1.35rem/1 var(--head)!important;padding:.85rem .9rem!important;border-radius:14px}
  header.top nav#main-nav a[aria-current],header.site-top nav#main-nav a[aria-current]{background:var(--blue);color:var(--sun)}
}
@media (max-width:640px) and (prefers-reduced-motion:reduce){.menu-btn span,nav#main-nav{transition:none!important}}"""

JS = """(()=>{const h=document.querySelector("header.top,header.site-top"),b=h&&h.querySelector(".menu-btn"),n=document.getElementById("main-nav");if(!b||!n)return;
const set=o=>{h.classList.toggle("menu-open",o);b.setAttribute("aria-expanded",o);b.setAttribute("aria-label",o?"Close menu":"Open menu");};
b.addEventListener("click",e=>{e.stopPropagation();set(!h.classList.contains("menu-open"));if(h.classList.contains("menu-open"))n.querySelector("a").focus({preventScroll:true});});
n.addEventListener("click",e=>{if(e.target.closest("a"))set(false);});
document.addEventListener("click",e=>{if(!h.contains(e.target))set(false);});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&h.classList.contains("menu-open")){set(false);b.focus();}});
addEventListener("resize",()=>{if(innerWidth>640)set(false);});})();"""


def apply(html):
    """Add the button, nav id, CSS and JS to one page. Safe to run twice."""
    if 'class="menu-btn"' in html:
        return html
    html = html.replace('<nav aria-label="Main">', BTN + '\n    <nav aria-label="Main" id="main-nav">', 1)
    html = html.replace('</style>', '\n' + CSS + '\n</style>', 1)
    i = html.rindex('</body>')
    html = html[:i] + '<script>\n' + JS + '\n</script>\n' + html[i:]
    return html
