# Sno-White Drive-In, Taft CA

Production single-page site for **Sno-White Drive-In**, 825 Center St, Taft, CA 93268. Built by Tastetrak.

- Live: https://tastetrak.github.io/Snow-White-Taft/
- `index.html` is self-contained (CSS inlined, logo SVGs embedded as data URIs, vanilla JS) and can be pasted into BobCRM as-is.
- Regenerate it with `python3 build/build.py`. All facts, menu items, gallery entries and links live in `build/build.py`; the markup lives in `build/template.html`.
- The absolute URLs that must change when the domain moves are listed in a comment at the top of `index.html` and come from `SITE_URL` in `build/build.py`.
- Order, review and directions links are set once on `<body data-order-url data-review-url data-directions-url>`; a few lines of JS fill every Order, Review and Directions link from them. There is no online ordering, so every Order button dials the shop (the printed menu says "we take call in orders").

## Layout

Same bones as the other Tastetrak sites (sticky top bar, ticker, hero, photo strip, story, menu rail, gallery rail, reviews/follow band, visit, footer, floating phone pill) with a drive-in theme:

- The hero is the front of the restaurant, full-bleed, with a red marquee sign over it: bulb border that twinkles (off under `prefers-reduced-motion`), a dotted inner rule, and an arrow tail that points at the building's own Sno-White sign. A round rating sticker sits top right. On phones the photo stacks above and the sign overlaps it.
- Headings are Oswald in caps, like the backlit menu boards; the script accents and the wordmark are Pacifico, the closest open font to the red script on their menu cover and cups; body text is Instrument Sans. The three fonts are self-hosted in `assets/fonts/` (SIL Open Font License, copied from the `@fontsource` npm packages), so the page does not depend on Google Fonts.
- Menu cards without a photo get a drawn tile (cup, cone, burger, fries boat, strips, rings, kids' meal) in the menu's colors.

## Logo and assets

No logo file was attached to the brief. The business's own mark is a red script "Sno white" with a white outline (menu cover, cups, the dessert menu). `assets/sno-white-wordmark.svg`, `-wordmark-snow.svg` (for dark backgrounds) and `-script.svg` (top bar) redraw it in Pacifico with the same red and outline, as outlines from the font so they need no font to render. `assets/sno-white-mark.svg` / `.png` is a round badge with a soft-serve cone, used as the favicon (`favicon.png`) and in the story cluster. `assets/og-card.jpg` is the 1200×630 share card. Ask the owner for the real logo file and swap the three SVGs.

Photos in `assets/photos/` (24 files, plus 14 square tiles in `assets/photos/strip/`) are the business's own photo on its Google Business Profile (the storefront, used for the hero, the share card and gallery) plus customer photos from Google and Yelp, re-cropped so the whole subject stays in frame. Each `<img>` carries a `title` naming the source. The Yelp photos are 750–1000 px, the Google ones up to 2400 px. Ask the owner for originals.

## Palette, with where each value was sampled

| Token | Hex | Sampled from |
|---|---|---|
| snow (page background) | `#fbfbfd` | the white stucco and the name |
| ink (text, dark band) | `#16213a` | navy background of the printed menu pages |
| blue (ticker, strip, headings on cards) | `#1b3f8f` | menu cover and the Sno-White cups |
| red (sign, buttons, script) | `#d12b2b` | the red script logo and the band on the menu cover |
| cherry (hover) | `#b8122a` | red tile and booths in the dining room |
| cream (price chips, sign accents) | `#fff5d6` | soft serve on the dessert menu |
| stucco (footer) | `#ede6d6` | storefront stucco |
| stone (reserved) | `#b89a6a` | stacked stone on the storefront |
| sky (story section, tiles) | `#d9e8f5` | sky in the storefront photo |
| tan (stars, drawn fries) | `#d9a65a` | crinkle fries |

## Research sources

- Google Business Profile (place id `ChIJ01W_5lfK64ARw0K1oDb_3og`, cid `9862600844077515459`): name, address, phone, hours (Mon–Thu and Sat–Sun 10 AM–10 PM, Fri 2–10 PM), 4.4 rating / 580 reviews, categories (fast food, hamburger restaurant), service options (drive-through, dine-in, takeout, no delivery), kids' menu, review tags (burgers, shakes, pastrami sandwich, crinkle cut fries, pastrami chili cheese fries, jalapeño poppers, root beer freeze, 60s vibe), 5 listing photos and 25 reviews. The quote in the band is a five-star Google review from January 2024.
- Yelp https://www.yelp.com/biz/sno-white-drive-in-taft : 4.1 / 37 reviews, hours agree with Google, 22 photos including the four printed menu pages (burgers 1–20, sandwiches, sides, desserts and the dollar menu) and the menu cover, which supplied the logo reference, the colors and "we take call in orders".
- MenuPix https://www.menupix.com/bakersfield/restaurants/5513262/Sno-White-Drive-In-Taft-CA : the five current prices on the page (#1 Giant $9.99 combo / $6.99 single, #6 Double K.O. $12.99, Animal Fries $7.99, French Fries $2.99) and item descriptions.
- Restaurantji, Restaurant Guru, Hyperflyer, Yellow Pages: cross-checks for address, phone and hours. Yellow Pages lists a second number, (661) 745-4944, not used.
- RoadsideArchitecture.com (Sno-White Drive-ins page): the chain was founded in Stockton in the 1950s with about 200 California locations by the mid-1960s; the Taft building looked closed in 2012, was rebuilt by 2015 and had reopened by 2017. Google reviews call it a Taft icon from the 1980s and before.
- No Instagram or TikTok account was found (Google lists an Instagram profile link but the handle could not be read), so the follow cards are Facebook, Call and Directions.
- No local press coverage of the Taft location was found.

## Publishing

`.github/workflows/pages.yml` deploys the branch to GitHub Pages on every push. GitHub Pages has to be switched on once by a repository admin, because the workflow token is not allowed to create the Pages site and the Pages API is not reachable from the build session: open **Settings → Pages**, set **Source** to **GitHub Actions**, then re-run the "Deploy to GitHub Pages" workflow (or push). The site will be served at https://tastetrak.github.io/Snow-White-Taft/. If you prefer **Deploy from a branch** (branch `claude/cool-pascal-05tozm`, folder `/ (root)`), that works too; delete the workflow file in that case.

## Still needed from the owner

1. Current prices. The printed menu on Yelp is from 2018 and MenuPix shows newer names and prices (Giant, Double K.O., Animal Fries), so only those five dollar amounts are on the page; the other cards say "Combo available", "4 sizes" and so on. A photo of the current menu boards fixes this in `MENU` in `build/build.py`.
2. The real logo file, to replace the three redrawn SVGs in `assets/`.
3. Confirm the Friday hours (2 PM–10 PM, per Google, Yelp and the menu cover's "Fridays only from 2 PM–10 PM").
4. Confirm the phone number (661) 763-1732 and whether call-in orders are still taken; if they add online ordering, set `order_url` in `build/build.py`.
5. The Facebook page URL. The page uses the one Google lists (`facebook.com/Sno-White-Drive-In-108122955896707`); a second page id (`100065307137418`) also turns up in search.
6. An Instagram handle, if one exists.
7. Original, full-resolution food photos, especially of the Giant, Double K.O., Animal Fries, shakes, freezes and sundaes, which are the drawn placeholder tiles in the menu rail.
8. When the restaurant was first opened in Taft, for the story section.
9. The domain they want to use. Update `SITE_URL` in `build/build.py`, rebuild, and point DNS.
