# Aja Cramer portfolio: guide for Claude

Read this before changing anything on the site. It records how the site is built and the rules Aja has set.

## What this is
- Aja Cramer's design portfolio. She's a digital designer and Membership Manager at Valley Forge Tourism & Convention Board (VFTCB).
- A static site: plain HTML pages with the CSS and JS written inline. There is no framework or build step.
- The site files live in `site/`. `netlify.toml` tells Netlify to publish that folder. Anything in the repo root outside `site/` (this guide, the README) is not public.
- Hosted on Netlify. The site folder is the source of truth, so edit those files directly.
- Live address: https://aja-design.com (Netlify). GitHub repo: ajacramer/portfolio. If the address changes, update `og:url` and `og:image` in `index.html`.

## Files (all inside `site/`)
| File | What it is |
|---|---|
| `index.html` | Home page: hero, work cards, About, After hours, contact form, footer |
| `vftcb-membership.html` | VFTCB hub page linking the 4 mini projects |
| `vftcb-presentation.html`, `vftcb-signup.html`, `vftcb-coop.html`, `vftcb-renewal.html` | VFTCB mini projects |
| `freedom-from-hunger.html`, `beyond-barriers.html`, `last-chance-getaways.html` | Case studies |
| `images/` | All images and videos, one folder per project (`vftcb/`, `ffh/`, `bb/`, `lcg/`, `deck/`, `landing/`) |
| `services/` | Services overview page, linked in the main nav (generated, see below) |
| `web-design/` | SEO landing pages (see below) |
| `sitemap.xml`, `robots.txt` | For search engines |
| `images/share-card.jpg` | Link preview image (1200×630) |
| `favicon.ico`, `images/favicon-32.png`, `images/apple-touch-icon.png` | Site icon: an "A" plus a lilac dot on navy |

"View the next project" order: VFTCB hub → Freedom From Hunger → Last Chance Getaways → Beyond Barriers → VFTCB hub. The VFTCB minis go Presentation → Sign-up → Co-op → Renewal.

## Rules Aja has set (always follow)
**Name**
- The business name is **Aja Cramer Designs**: page titles, footers, metadata and structured data. The header logo on the home page and case studies stays "Aja Cramer" (the landing pages use "Aja Cramer Designs"). Her personal name, Aja Cramer, stays in the About copy.

**Colors**
- Never use pure white or pure black.
- Off-white is `#E7E3F1` (`--paper`) and near-black is `#14132A` (`--ink`).
- Other colors: navy `#201E43`, lilac `#B69CFF` (`--sun`), teal `#508C9B`, blue `#134B70`, muted `#BFC6D6`.

**Copy**
- Use her copy word for word.
- No em dashes.
- Never invent numbers or stats.
- Headers must not sound AI-written.
- Credit the colleague as "a colleague at VFTCB". Never name her.

**Handwritten notes**
- Only add notes where she asks for them.
- Every arrow needs a visible arrowhead lined up with the end of its line.

**Layout preferences**
- Keep vertical space tight.
- Section headings go on one line where possible.
- Things shouldn't jump or resize while they animate.

**Fonts**
- League Spartan for headings, Instrument Sans for body text, Space Mono for labels, Caveat for handwritten notes.
- Each hero word has its own display font.

## Things that are easy to break
- **Hero "Bringing a little ___ back to the internet."** The words rotate, and each has its own font and animation. Each word waits for its font to load before it animates. Without that, "intention" lines up wrong on phones. Avoid `steps()` easing with `fill`, because Safari can freeze it partway.
- **After hours card**
  - Moon: clicking it, or an automatic timer every 30 seconds, triggers either the eclipse or Kasi the wolf howling.
  - Shooting stars: clicking one is a wish, counted in localStorage under `aja-wishes`.
  - Aurora: shows up at random, and every 5th wish.
  - UFO: appears at random and abducts a word from the text.
  - To test in the browser console: `eclipseNow()`, `howlNow()`, `auroraNow()`, `summonUFO()`.
  - The moon's glow is allowed to spill outside the card.
- **Contact form**
  - It's a Netlify Form named `work-with-me`. Fields: name, email, phone, business or organization, what can I help with, timeline, budget, message. Every field is required except budget.
  - A hidden `subject` field makes the notification email read `**NEW DESIGN SUBMISSION** from [name]`. Keep the stars.
  - After sending, the thank-you sequence plays: a paper plane, a checkmark and the text "Thanks!".
- **Tall screenshots** are split into tiles no taller than 1600px, because browsers drop very tall images.

## How to add a new project
Aja provides:
1. The copy, written by her. Mark exactly where any handwritten notes go.
2. Screens or images, a Figma link and the live link if there is one.
3. A cover image for the home page card.

Claude then:
1. Copies the closest existing case study page and keeps its structure and components.
2. Puts the images in `images/<short-name>/`.
3. Adds a work card to the home page.
4. Updates the "next project" links so the order stays a loop.
5. Sets the page `<title>` to "Project name | Aja Cramer Designs".
6. Checks the page at desktop and phone widths before handing it back.

## Landing pages (`site/web-design/`)
- SEO landing pages: an overview at `/services/` (in the main nav: Work · Services · About · Contact; `/web-design/` redirects there in `netlify.toml`) plus one page per service: `restaurants`, `breweries-wineries-distilleries`, `retail`, `attractions-events`, `contractors-home-services`, `presentations`. Each lives at `site/web-design/<slug>/index.html`.
- **Don't edit those HTML files by hand.** They are generated from `landing-pages/` in the repo root (not public):
  - `pages.py` holds every page's copy, photos, rotating words and sample screen. Aja's copy, word for word.
  - `template.html` is the shared layout. A design change here applies to all pages.
  - `build.py` builds them. Run `python3 build.py --repo ../site` from `landing-pages/` to rebuild the pages, the services page, the WebP photos in `site/images/landing/`, and the footer services list on every hand-built page. Run `python3 build.py` alone for self-contained preview files in `landing-pages/out/`.
- Photos are Adobe Stock (free license), tinted purple for the hero and teal elsewhere. Source JPGs are in `landing-pages/images/`.
- Each page's contact form is the same Netlify form as the home page (`work-with-me`, same fields, same thank-you sequence), with a hidden `source-page` field so the email says which page it came from. The home page form has `source-page` = "Home page" so Netlify keeps that field. If the home page form fields change, change `template.html` to match.
- Rules for these pages: no single word alone on a last line; step numbers 02 and 04 are lilac; each page varies its buttons (hero names the business, "Let's grab coffee" after the steps, "Start the conversation" on the form).
- The Presentations page shows `vftcb-presentation.html` live in a scaled frame. It works because it's the same site. Don't add headers that block framing from the same origin.
- The home page has a "What can we make together?" section before Work that links each service by its descriptive name, plus an "Explore all services" button. Every footer has a small Services list (`<nav class="fsvc">`), generated from `pages.py`.
- `site/sitemap.xml` and `site/robots.txt` list every public page. Add new pages to the sitemap.

## After hours / blog (not built yet)
- Right now it's a "Coming soon" card for nail art, coding experiments and fun write-ups.
- Building it out probably means an `after-hours.html` index page plus one page per post. The posts should follow the same style as the rest of the site, and the night-sky look of the card can carry over.
- Ask Aja what the first posts are before designing the layout.

## Open questions still waiting on Aja
- **Last Chance Getaways:** her copy says "Twenty fictional five-star reviews", but the site shows five reviews with mixed star ratings.
- **Last Chance Getaways:** the recording doesn't show where the countdown comes from.
- **Share cards for project pages:** only the home page has one so far.
