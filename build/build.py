#!/usr/bin/env python3
"""Regenerates ../index.html from template.html.

Everything the page says about the business lives in SITE below, so a fact
can be corrected in one place. The logo SVGs are embedded as data URIs; photos
and fonts are referenced by absolute URL (see ASSET_BASE) so the page can be
pasted into BobCRM as a single file.

Run:  python3 build/build.py
"""
import base64, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "build", "template.html")
OUT = os.environ.get("OUT", os.path.join(ROOT, "index.html"))

# ---- Absolute URLs. Change these when the domain moves. ---------------------
SITE_URL = os.environ.get("SITE_URL", "https://tastetrak.github.io/Snow-White-Taft/")
ASSET_BASE = SITE_URL + "assets/"

PLACE_ID = "ChIJ01W_5lfK64ARw0K1oDb_3og"
DEST = "Sno-White%20Drive-In%2C%20825%20Center%20St%2C%20Taft%2C%20CA%2093268"

SITE = {
    "name": "Sno-White Drive-In",
    "short": "Sno-White",
    "city": "Taft, CA",
    "street": "825 Center St",
    "locality": "Taft",
    "region": "CA",
    "postal": "93268",
    "phone_display": "(661) 763-1732",
    "phone_tel": "+16617631732",
    "lat": 35.1425316,
    "lng": -119.4647975,
    "place_id": PLACE_ID,
    "rating": "4.4",
    "review_count": "580",
    # No online ordering exists; the menu says "we take call in orders", so every Order button dials the shop.
    "order_url": "tel:+16617631732",
    "review_url": "https://search.google.com/local/writereview?placeid=" + PLACE_ID,
    "reviews_read_url": "https://www.google.com/maps/place/?q=place_id:" + PLACE_ID,
    "directions_url": "https://www.google.com/maps/dir/?api=1&destination=" + DEST + "&destination_place_id=" + PLACE_ID,
    "map_embed": "https://maps.google.com/maps?q=" + DEST + "&z=16&output=embed",
    "facebook": "https://www.facebook.com/Sno-White-Drive-In-108122955896707/",
    "yelp": "https://www.yelp.com/biz/sno-white-drive-in-taft",
    "hours": [
        ("Monday", "10 AM – 10 PM"),
        ("Tuesday", "10 AM – 10 PM"),
        ("Wednesday", "10 AM – 10 PM"),
        ("Thursday", "10 AM – 10 PM"),
        ("Friday", "2 PM – 10 PM"),
        ("Saturday", "10 AM – 10 PM"),
        ("Sunday", "10 AM – 10 PM"),
    ],
}

# Photo credits: gb = the business's own photo on its Google Business Profile,
# g = customer photos on the Google Business Profile, y = customer photos on Yelp.
CREDIT = {"gb": "From the business's Google Business Profile", "g": "Customer photo on Google", "y": "Customer photo on Yelp"}

# Prices: the five dollar amounts are the ones listed on MenuPix for the current
# menu (Giant, Double K.O., Animal Fries, fries). Everything else is from the
# printed menu photographed on Yelp, which is older, so those cards carry a
# size or combo note instead of a price. See README "Still needed from the owner".
MENU = [
    dict(name="Pastrami Burger", desc="A burger stacked with grilled pastrami, cheese, lettuce, tomato and pickle. The one people drive in for.", price="Combo available", photo="pastrami-burger.jpg", alt="Pastrami burger piled high, with the drive-in window behind it", credit="y"),
    dict(name="The Giant", desc="Special sauce, onions, lettuce, pickles and tomatoes. Add cheese, or make it a combo with crinkle fries and a drink.", price="$6.99 · combo $9.99", photo=None, tile="burger"),
    dict(name="Double Cheeseburger", desc="Two patties, American cheese and the works on a toasted bun. Combo it with fries and a Pepsi.", price="Combo available", photo="double-cheeseburger-meal.jpg", alt="Double cheeseburger in paper with crinkle fries", credit="y"),
    dict(name="Double K.O.", desc="Mayo, jalapeños, onions, lettuce, tomatoes, pickles, avocado, bacon and cheese. Two patties underneath all of it.", price="$12.99", photo=None, tile="burger2"),
    dict(name="Pastrami Chili Cheese Fries", desc="Crinkle fries buried in chili, melted cheese and hot pastrami. Small feeds one, large feeds the table.", price="Small · Large", photo="pastrami-chili-cheese-fries.jpg", alt="Takeout box of crinkle fries covered in pastrami, chili and cheese", credit="g"),
    dict(name="Animal Fries", desc="Our famous fries topped with grilled onions and ground beef, Thousand sauce and melted American cheese.", price="$7.99", photo=None, tile="fries"),
    dict(name="Crinkle Cut Fries", desc="Hot, crispy and seasoned, four sizes. Ask for the house ranch; people are picky about it and still rave.", price="$2.99", photo="crinkle-fries.jpg", alt="Crinkle cut fries in paper on a red tray", credit="y"),
    dict(name="Milkshakes & Malts", desc="Chocolate, strawberry, vanilla, peanut butter, banana, cherry, Oreo, Butterfinger, Reese's and more. Small to jumbo.", price="4 sizes", photo=None, tile="shake"),
    dict(name="Freezes, Floats & Slushies", desc="Root beer and orange freezes, floats, and slushies in cherry, blue raspberry, orange, strawberry and kiwi.", price="4 sizes", photo=None, tile="slush"),
    dict(name="Sundaes & Banana Splits", desc="Hot fudge, chocolate, strawberry, pineapple or caramel. Cones plain or dipped, parfaits and candy-mix cups too.", price="Dessert", photo=None, tile="cone"),
    dict(name="Corn Dogs", desc="Hand-dipped and fried to order. Two in a combo, or one off the kids' menu.", price="Combo available", photo="corndog.jpg", alt="A hand-dipped corn dog with a bite taken out", credit="y"),
    dict(name="Chicken Strips", desc="Three or six pieces with dipping sauce, or the chicken dinner plate with fries and a drink.", price="3 or 6 pc", photo=None, tile="strips"),
    dict(name="Grilled Cheese", desc="Buttery and crisp on the griddle. The kids' menu classic that grown-ups keep ordering.", price="Ask at the window", photo="grilled-cheese.jpg", alt="A grilled cheese sandwich, golden on the outside", credit="g"),
    dict(name="Rings, Zucchini & Poppers", desc="Onion rings, fried zucchini, jalapeño poppers, mushrooms, cheese sticks and nachos on the side.", price="Sides", photo=None, tile="rings"),
    dict(name="Kids' Meals", desc="Hamburger, corn dog, burrito or five-piece nuggets, with fries and a drink.", price="Kids", photo=None, tile="kids"),
]

STRIP = [
    ("s01.jpg", "Pastrami burger"), ("s02.jpg", "Crinkle cut fries"), ("s03.jpg", "Pastrami chili cheese fries"),
    ("s04.jpg", "Double cheeseburger meal"), ("s05.jpg", "Corn dog"), ("s06.jpg", "The dining room, red booths and tile"),
    ("s07.jpg", "Double cheeseburger"), ("s08.jpg", "Crinkle fries, close up"), ("s09.jpg", "The Sno-White menu cover"),
    ("s10.jpg", "Cheeseburger, fries and grilled cheese"), ("s11.jpg", "Pastrami burger, stacked"), ("s12.jpg", "Sundaes, slushies and shakes on the menu"),
    ("s13.jpg", "Grilled cheese"), ("s14.jpg", "The front of the restaurant"),
]

STORY_PHOTOS = [
    dict(photo="storefront-2017.jpg", alt="Sno-White Drive-In after the rebuild, stone front and cream stucco", credit="y"),
    dict(photo="dining-room.jpg", alt="Dining room with red tile walls, red booths and black chairs", credit="g"),
    dict(photo="pastrami-burger-stack.jpg", alt="Pastrami burger on the counter", credit="g"),
]

# Mosaic tiles. pos = (column, row, columns spanned, rows spanned) on the 6 x 6
# desktop grid; the pieces are laid out by hand so they fill it exactly. On
# phones the tiles flow into two columns using only the spans.
GALLERY = [
    dict(photo="hero-storefront-square.jpg", alt="The front of Sno-White Drive-In with the sign over the door", cap="The front on Center St", credit="gb", pos=(1, 1, 2, 2)),
    dict(photo="menu-cover.jpg", alt="The blue Sno-White menu cover with shakes, sundaes and a double cheeseburger", cap="The menu cover", credit="y", pos=(3, 1, 1, 2)),
    dict(photo="pastrami-burger-fries.jpg", alt="Pastrami burger with crinkle fries on a tray", cap="Pastrami burger and fries", credit="y", pos=(4, 1, 1, 2)),
    dict(photo="counter.jpg", alt="The order counter with red tile and the menu boards above", cap="The counter", credit="y", pos=(5, 1, 2, 1)),
    dict(photo="crinkle-fries-2.jpg", alt="Crinkle cut fries in a paper boat", cap="Crinkle cut, every time", credit="g", pos=(5, 2, 1, 2)),
    dict(photo="pastrami-burger-stack.jpg", alt="Pastrami burger stacked with cheese and lettuce", cap="Pastrami, stacked", credit="g", pos=(6, 2, 1, 2)),
    dict(photo="dining-room.jpg", alt="Dining room with red booths and tile", cap="Red booths, red tile", credit="g", pos=(1, 3, 2, 2)),
    dict(photo="cheeseburger-grilled-cheese.jpg", alt="Cheeseburger, fries, ranch and a grilled cheese on a red tray", cap="Burger, fries, ranch, grilled cheese", credit="y", pos=(3, 3, 2, 1)),
    dict(photo="double-cheeseburger.jpg", alt="Double cheeseburger unwrapped", cap="Double cheeseburger", credit="y", pos=(3, 4, 1, 1)),
    dict(photo="menu-treats.jpg", alt="The dessert menu: sundaes, slushies, milkshakes, cones and the dollar menu", cap="The freezer side of the menu", credit="y", pos=(4, 4, 1, 2)),
    dict(photo="from-the-road.jpg", alt="Sno-White Drive-In seen from across Center Street with the tall sign", cap="From across Center St", credit="g", pos=(5, 4, 2, 1)),
    dict(photo="walk-up.jpg", alt="Walking up to the door under the Sno-White sign", cap="Walk up or drive through", credit="g", pos=(1, 5, 1, 2)),
    dict(photo="dining-room-2.jpg", alt="Booths along the window", cap="Booths by the window", credit="y", pos=(2, 5, 1, 1)),
    dict(photo="menu-boards.jpg", alt="Backlit menu boards at the drive-thru window", cap="The drive-thru boards", credit="y", pos=(3, 5, 1, 2)),
    dict(photo="pastrami-chili-cheese-fries.jpg", alt="Pastrami chili cheese fries in a takeout box", cap="Pastrami chili cheese fries", credit="g", pos=(5, 5, 1, 2)),
    dict(photo="storefront-2017.jpg", alt="The storefront after the rebuild", cap="The rebuilt front", credit="y", pos=(6, 5, 1, 1)),
    dict(photo="corndog.jpg", alt="A hand-dipped corn dog", cap="Corn dog", credit="y", pos=(2, 6, 1, 1)),
    dict(photo="grilled-cheese.jpg", alt="A grilled cheese sandwich, golden on the outside", cap="Grilled cheese", credit="g", pos=(4, 6, 1, 1)),
    dict(photo="double-cheeseburger-meal.jpg", alt="Double cheeseburger in paper with crinkle fries", cap="Double cheeseburger meal", credit="y", pos=(6, 6, 1, 1)),
]

REVIEW = dict(
    text="A great place to grab a quick bite. Food and service are just excellent. I had the hamburger with pastrami, and it was absolutely great. The fries were also very good. The gentleman behind the counter was genuinely friendly. This place is 1000% better than all those franchises in the area.",
    who="Google reviewer",
    where="five stars, January 2024",
)


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def data_svg(name):
    return "data:image/svg+xml;base64," + b64(os.path.join(ROOT, "assets", name))


# ---- Drawn placeholder tiles, in the colors of the dessert menu and the cups ----
SVG_OPEN = '<svg class="pz" viewBox="0 0 200 200" aria-hidden="true">'
TILES = {
    # a Sno-White paper cup with a swirl of soft serve and a straw: shakes
    "shake": SVG_OPEN + '<path d="M70 70h60l-8 110H78z" fill="#1b3f8f"/><path d="M72 92h56l-2 14H74z" fill="#fbfbfd"/>'
             '<path d="M78 70c-10-8-6-22 6-20-2-10 10-16 16-8 4-10 18-8 20 2 10-2 16 10 8 18 6 6 2 16-6 16H84c-8 0-12-4-6-8z" fill="#fff5d6"/>'
             '<path d="M118 60l12-40" stroke="#d12b2b" stroke-width="6" stroke-linecap="round"/><circle cx="100" cy="40" r="7" fill="#d12b2b"/>'
             '<text x="100" y="150" text-anchor="middle" font-family="Pacifico,cursive" font-size="16" fill="#fbfbfd">Sno-White</text></svg>',
    # a slush cup with a dome lid
    "slush": SVG_OPEN + '<path d="M66 80h68l-8 100H74z" fill="#d12b2b"/><path d="M62 80h76v10H62z" fill="#fbfbfd"/><path d="M70 80c0-30 60-30 60 0z" fill="#1b3f8f"/>'
             '<path d="M104 70l10-50" stroke="#fff5d6" stroke-width="6" stroke-linecap="round"/><path d="M80 110h40M82 130h36M86 150h28" stroke="#fbfbfd" stroke-width="4" stroke-linecap="round" opacity=".7"/></svg>',
    # a dipped soft-serve cone
    "cone": SVG_OPEN + '<path d="M70 96h60l-24 84a6 6 0 0 1-12 0z" fill="#d9a65a"/><path d="M76 110l48-14M80 126l40-12M86 142l28-8M90 158l20-6M84 96l22 70M116 96l-22 70" stroke="#b07d33" stroke-width="2.4" stroke-linecap="round" fill="none"/>'
            '<path d="M64 94c-8-8-4-22 8-20-8-10 0-24 12-20-4-12 12-20 20-10 8-10 24-2 20 10 12-4 20 10 12 20 12-2 16 12 8 20z" fill="#fff5d6"/>'
            '<path d="M70 70c-4-10 8-18 16-10 0-12 20-14 24-2 10-8 22 2 16 12z" fill="#5a2a1a"/><circle cx="100" cy="42" r="7" fill="#d12b2b"/></svg>',
    # a burger
    "burger": SVG_OPEN + '<path d="M44 90c0-30 112-30 112 0z" fill="#d9a65a"/><circle cx="76" cy="74" r="2.2" fill="#fff5d6"/><circle cx="100" cy="68" r="2.2" fill="#fff5d6"/><circle cx="124" cy="76" r="2.2" fill="#fff5d6"/>'
              '<path d="M40 92h120v8H40z" fill="#5fa84a"/><path d="M44 100h112v14H44z" fill="#d12b2b"/><path d="M40 114h120v10l-12 8-12-8H64l-12 8-12-8z" fill="#f2b705"/>'
              '<path d="M46 124h108v18H46z" fill="#5a2a1a"/><path d="M44 142h112c0 16-112 16-112 0z" fill="#d9a65a"/></svg>',
    "burger2": SVG_OPEN + '<path d="M44 78c0-30 112-30 112 0z" fill="#d9a65a"/><circle cx="76" cy="62" r="2.2" fill="#fff5d6"/><circle cx="100" cy="56" r="2.2" fill="#fff5d6"/><circle cx="124" cy="64" r="2.2" fill="#fff5d6"/>'
               '<path d="M40 80h120v8H40z" fill="#5fa84a"/><path d="M44 88h112v10H44z" fill="#7cbf5a"/><path d="M40 98h120v8l-12 8-12-8H64l-12 8-12-8z" fill="#f2b705"/>'
               '<path d="M46 108h108v14H46z" fill="#5a2a1a"/><path d="M44 122h112v8H44z" fill="#d12b2b"/><path d="M46 130h108v14H46z" fill="#5a2a1a"/><path d="M44 144h112c0 16-112 16-112 0z" fill="#d9a65a"/></svg>',
    # a boat of crinkle fries
    "fries": SVG_OPEN + '<g stroke="#d9a65a" stroke-width="12" stroke-linecap="round" fill="none"><path d="M70 120q6-10 0-20t0-20 0-20"/><path d="M90 116q6-10 0-20t0-20 0-22"/><path d="M110 116q6-10 0-20t0-20 0-22"/><path d="M130 120q6-10 0-20t0-20 0-20"/></g>'
             '<path d="M50 110h100l-10 70H60z" fill="#d12b2b"/><path d="M50 110h100v10H50z" fill="#fbfbfd"/><text x="100" y="158" text-anchor="middle" font-family="Pacifico,cursive" font-size="18" fill="#fff5d6">Sno-White</text></svg>',
    # chicken strips in a boat
    "strips": SVG_OPEN + '<g fill="#d9a65a" stroke="#b07d33" stroke-width="3"><path d="M60 110c-10-30 10-60 24-50 12 10 2 40-6 56z"/><path d="M90 108c-4-34 20-58 32-44 10 12-6 40-14 52z"/><path d="M122 112c0-30 26-44 34-30 6 12-12 30-20 38z"/></g>'
              '<path d="M44 112h112l-10 68H54z" fill="#1b3f8f"/><path d="M44 112h112v10H44z" fill="#fbfbfd"/><circle cx="150" cy="150" r="16" fill="#fbfbfd"/><circle cx="150" cy="150" r="10" fill="#d12b2b"/></svg>',
    # onion rings stacked
    "rings": SVG_OPEN + '<g fill="none" stroke="#d9a65a" stroke-width="14"><ellipse cx="100" cy="140" rx="46" ry="18"/><ellipse cx="92" cy="110" rx="42" ry="17"/><ellipse cx="106" cy="80" rx="40" ry="16"/></g>'
             '<g fill="none" stroke="#b07d33" stroke-width="2" stroke-dasharray="3 5"><ellipse cx="100" cy="140" rx="46" ry="18"/><ellipse cx="92" cy="110" rx="42" ry="17"/><ellipse cx="106" cy="80" rx="40" ry="16"/></g></svg>',
    # kids: a small burger, a corn dog and a cup
    "kids": SVG_OPEN + '<path d="M30 110c0-22 70-22 70 0z" fill="#d9a65a"/><path d="M28 112h74v8H28z" fill="#5fa84a"/><path d="M30 120h70v12H30z" fill="#5a2a1a"/><path d="M28 132h74c0 12-74 12-74 0z" fill="#d9a65a"/>'
            '<rect x="126" y="40" width="22" height="80" rx="11" fill="#d9a65a"/><path d="M137 120v50" stroke="#b07d33" stroke-width="5" stroke-linecap="round"/><path d="M132 60c4 10 8 20 4 40" stroke="#f2b705" stroke-width="4" stroke-linecap="round" fill="none"/>'
            '<path d="M70 150h40l-5 40H75z" fill="#1b3f8f"/><path d="M96 150l8-30" stroke="#d12b2b" stroke-width="5" stroke-linecap="round"/></svg>',
}


def tile_svg(kind, label):
    """Labeled placeholder tile: a drawn cup, cone, burger or boat of fries in the menu's colors."""
    return (
        '<div class="tile" role="img" aria-label="%s, made to order">%s'
        '<span class="tile-label">%s</span></div>' % (html.escape(label), TILES.get(kind, TILES["shake"]), html.escape(label))
    )


def strip_tiles():
    out = []
    for f, alt in STRIP + STRIP:  # doubled for a seamless loop
        out.append('<img loading="lazy" src="%sphotos/strip/%s" alt="%s" width="480" height="480">' % (ASSET_BASE, f, html.escape(alt)))
    return "".join(out)


def story_photos():
    return "".join('<img loading="lazy" src="%sphotos/%s" alt="%s" title="%s">' % (ASSET_BASE, p["photo"], html.escape(p["alt"]), CREDIT[p["credit"]]) for p in STORY_PHOTOS)


def menu_cards():
    out = []
    for i, m in enumerate(MENU):
        if m.get("photo"):
            media = '<img loading="lazy" src="%s" alt="%s" title="%s">' % (
                ASSET_BASE + "photos/" + m["photo"], html.escape(m["alt"]), CREDIT[m["credit"]])
        else:
            media = tile_svg(m["tile"], m["name"])
        out.append(
            '<article class="card" data-i="%d">'
            '<div class="card-media">%s<span class="price">%s</span></div>'
            '<div class="card-body"><h3>%s</h3><p>%s</p></div></article>'
            % (i, media, html.escape(m["price"]), html.escape(m["name"]), html.escape(m["desc"]))
        )
    return "\n".join(out)


def gallery_cards():
    out = []
    for i, g in enumerate(GALLERY):
        c, r, cs, rs = g["pos"]
        cls = {(2, 2): "s22", (2, 1): "s21", (1, 2): "s12"}.get((cs, rs), "")
        out.append(
            '<figure class="%s" style="--i:%d;--a:%d / %d / span %d / span %d"><img loading="lazy" src="%s" alt="%s" title="%s">'
            '<figcaption>%s</figcaption></figure>'
            % (cls, i, r, c, rs, cs, ASSET_BASE + "photos/" + g["photo"], html.escape(g["alt"]), CREDIT[g["credit"]], html.escape(g["cap"]))
        )
    return "\n".join(out)


def hours_rows():
    return "\n".join('<div class="hrow%s"><span>%s</span><span>%s</span></div>' % (" fri" if d == "Friday" else "", d, h) for d, h in SITE["hours"])


def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "FastFoodRestaurant",
        "name": SITE["name"],
        "image": SITE_URL + "assets/og-card.jpg",
        "logo": SITE_URL + "assets/sno-white-mark.png",
        "url": SITE_URL,
        "telephone": SITE["phone_tel"],
        "servesCuisine": ["Burgers", "Pastrami", "Fast Food", "Ice Cream", "Milkshakes"],
        "priceRange": "$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["street"],
            "addressLocality": SITE["locality"],
            "addressRegion": SITE["region"],
            "postalCode": SITE["postal"],
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
        "hasMap": SITE["reviews_read_url"],
        "acceptsReservations": "False",
        "hasDriveThroughService": "True",
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"], "opens": "10:00", "closes": "22:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "14:00", "closes": "22:00"},
        ],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": SITE["rating"], "reviewCount": SITE["review_count"], "bestRating": "5"},
        "sameAs": [SITE["facebook"], SITE["yelp"]],
    }
    return json.dumps(data, indent=2)


def main():
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    rep = {
        "SITE_URL": SITE_URL,
        "ASSET_BASE": ASSET_BASE,
        "OG_IMAGE": SITE_URL + "assets/og-card.jpg",
        "FAVICON": SITE_URL + "assets/favicon.png",
        "HERO_IMG": ASSET_BASE + "photos/hero-storefront.jpg",
        "MARK": data_svg("sno-white-mark.svg"),
        "SCRIPT": data_svg("sno-white-script.svg"),
        "LOGO_FULL": data_svg("sno-white-wordmark.svg"),
        "STRIP_TILES": strip_tiles(),
        "STORY_PHOTOS": story_photos(),
        "MENU_CARDS": menu_cards(),
        "BAND_BG": ASSET_BASE + "photos/counter-wide.jpg",
        "VISIT_PHOTO": ASSET_BASE + "photos/from-the-road.jpg",
        "GALLERY_CARDS": gallery_cards(),
        "HOURS_ROWS": hours_rows(),
        "JSONLD": jsonld(),
        "REVIEW_TEXT": html.escape(REVIEW["text"]),
        "REVIEW_WHO": html.escape(REVIEW["who"]),
        "REVIEW_WHERE": html.escape(REVIEW["where"]),
    }
    for k, v in SITE.items():
        if isinstance(v, str):
            rep[k.upper()] = html.escape(v, quote=True)
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: rep[m.group(1)], tpl)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", OUT, len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
