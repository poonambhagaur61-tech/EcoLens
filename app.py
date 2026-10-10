import cv2
import numpy as np
import streamlit as st

from PIL import Image, ImageOps
from transformers import pipeline
from html import escape


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EcoLens",
    page_icon="🌿",
    layout="centered"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(s: str):
    flat = " ".join(
        line.strip()
        for line in s.splitlines()
        if line.strip()
    )

    st.markdown(
        flat,
        unsafe_allow_html=True
    )


# ============================================================
# DESIGN TOKENS
# ============================================================

MOSS = "#2F4A3A"
FERN = "#5E8C61"
MIST = "#E9F0EB"
LEAF = "#FFFFFF"
BARK = "#4A3B33"
ROSEHIP = "#C0394B"


# ============================================================
# CUSTOM CSS
# ============================================================

html(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Source+Serif+4:wght@400;600&display=swap'
    );

    html, body, [class*="css"], .stMarkdown, p, label {{
        font-family:
            'Source Serif 4',
            Georgia,
            serif;
        color: {BARK};
    }}

    h1, h2, h3, .eco-title {{
        font-family:
            'Bricolage Grotesque',
            system-ui,
            sans-serif !important;
        color: {MOSS} !important;
        letter-spacing: -0.02em;
    }}

    .stApp {{
        background: {MIST};
    }}

    #MainMenu,
    footer {{
        visibility: hidden;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 2rem;
        max-width: 760px;
    }}


    /* HERO */

    .eco-hero {{
        padding: 1.5rem 0 1rem 0;
    }}

    .eco-title {{
        font-size: clamp(3rem, 12vw, 4.5rem);
        font-weight: 800;
        line-height: 1;
        margin: 0;
    }}

    .eco-sub {{
        font-size: 1.15rem;
        margin-top: .6rem;
        max-width: 34em;
    }}


    /* TABS */

    .stTabs [data-baseweb="tab-list"] {{
        gap: .25rem;
        border-bottom: 2px solid {MOSS}22;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-weight: 700;
        color: {MOSS};
        padding: .6rem 1rem;
    }}

    .stTabs [aria-selected="true"] {{
        color: {ROSEHIP};
    }}

    .stTabs [data-baseweb="tab-highlight"] {{
        background: {ROSEHIP};
    }}


    /* UPLOADER */

    [data-testid="stFileUploader"] section {{
        background: {LEAF};
        border: 2px dashed {FERN};
        border-radius: 14px;
        padding: 1.6rem;
    }}

    [data-testid="stFileUploader"] section:hover {{
        border-color: {ROSEHIP};
    }}

    .stButton > button,
    [data-testid="stFileUploader"] button {{
        background: {MOSS};
        color: #fff;
        border: 0;
        border-radius: 10px;
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-weight: 700;
    }}

    .stButton > button:hover {{
        background: {FERN};
        color: #fff;
    }}

    :focus-visible {{
        outline: 3px solid {ROSEHIP} !important;
        outline-offset: 2px;
    }}


    /* PANELS */

    .eco-panel {{
        background: {LEAF};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
    }}

    .eco-panel h3 {{
        margin: 0 0 .7rem 0;
        font-size: 1.15rem;
    }}

    .eco-verdict {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: {MOSS};
        margin: 0;
    }}

    .eco-note {{
        font-size: .95rem;
        opacity: .85;
        margin-top: .3rem;
    }}


    /* STAT BARS */

    .bar-row {{
        display: flex;
        align-items: center;
        gap: .8rem;
        margin: .45rem 0;
    }}

    .bar-label {{
        width: 7.5rem;
        font-weight: 600;
    }}

    .bar-track {{
        flex: 1;
        height: 12px;
        background: {MIST};
        border-radius: 99px;
        overflow: hidden;
    }}

    .bar-fill {{
        height: 100%;
        background: {FERN};
        border-radius: 99px;
    }}

    .bar-val {{
        width: 3rem;
        text-align: right;
        font-variant-numeric: tabular-nums;
    }}


    /* PALETTE */

    .swatches {{
        display: flex;
        border-radius: 12px;
        overflow: hidden;
        height: 64px;
    }}

    .swatches div {{
        flex: 1;
    }}

    .hexes {{
        display: flex;
        gap: .5rem;
        margin-top: .5rem;
        flex-wrap: wrap;
    }}

    .hexes span {{
        font-size: .9rem;
        background: {MIST};
        border-radius: 6px;
        padding: .15rem .5rem;
    }}

    .hexes i {{
        display: inline-block;
        width: .8em;
        height: .8em;
        border-radius: 50%;
        margin-right: .35em;
    }}


    /* CENTERED AI RESULT */

    .ai-result {{
        background: {LEAF};
        border: 2px solid {FERN};
        border-radius: 18px;
        padding: 2rem 1rem;
        margin: 1.5rem 0;
        text-align: center;
    }}

    .ai-icon {{
        font-size: 3rem;
        text-align: center;
        margin-bottom: .3rem;
    }}

    .ai-title {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        color: {MOSS};
        text-align: center;
        margin: 0;
        text-transform: uppercase;
    }}

    .ai-confidence {{
        font-family:
            'Source Serif 4',
            Georgia,
            serif;
        font-size: 1rem;
        color: {BARK};
        text-align: center;
        margin-top: .6rem;
    }}


    /* LOW CONFIDENCE RESULT */

    .ai-warning {{
        background: {LEAF};
        border-left: 6px solid {ROSEHIP};
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }}

    .ai-warning-title {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: {ROSEHIP};
    }}

    .ai-description {{
        font-size: 1rem;
        margin-top: .5rem;
    }}


    /* MISSION */

    .mission-card {{
        background: {LEAF};
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }}

    .mission-title {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        color: {MOSS};
    }}


    /* TREE / SOIL / HABITAT INFO */

    .tree-card {{
        background: {LEAF};
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
        border-top: 6px solid {FERN};
    }}

    .tree-name {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: {MOSS};
        line-height: 1.1;
    }}

    .tree-sci {{
        font-style: italic;
        opacity: .8;
        margin-bottom: .8rem;
    }}

    .tree-fact {{
        display: flex;
        flex-direction: column;
        padding: .55rem 0;
        border-top: 1px solid {MIST};
    }}

    .tree-key {{
        font-family:
            'Bricolage Grotesque',
            sans-serif;
        font-weight: 700;
        color: {MOSS};
        font-size: .95rem;
    }}

    .eco-list {{
        margin: .4rem 0 0 1.2rem;
        padding: 0;
    }}

    .eco-list li {{
        margin-bottom: .4rem;
    }}

    .sugg-row {{
        display: flex;
        gap: .6rem;
        margin: .45rem 0;
    }}


    /* CROP CHIPS (soil card) */

    .crop-chips {{
        display: flex;
        flex-wrap: wrap;
        gap: .4rem;
        margin-top: .3rem;
    }}

    .crop-chips span {{
        background: {MIST};
        color: {MOSS};
        border-radius: 99px;
        padding: .15rem .7rem;
        font-size: .9rem;
        font-weight: 600;
    }}

    .stProgress > div > div > div > div {{
        background-color: {FERN};
    }}

    [data-testid="stProgress"] [role="progressbar"] > div,
    [data-testid="stProgress"] [role="progressbar"] > div > div {{
        background-color: {FERN} !important;
    }}

    [data-testid="stProgress"] [role="progressbar"] {{
        background-color: {MOSS}22 !important;
    }}

    </style>
    """
)


# ============================================================
# IMAGE HELPERS
# ============================================================

def load_image(file) -> Image.Image:

    img = ImageOps.exif_transpose(
        Image.open(file)
    )

    return img.convert("RGB")


def show_image(img, caption):

    try:

        st.image(
            img,
            caption=caption,
            width="stretch"
        )

    except TypeError:

        st.image(
            img,
            caption=caption,
            use_container_width=True
        )


# ============================================================
# OPENCV IMAGE ANALYSIS
# ============================================================

@st.cache_data(show_spinner=False)
def analyze(rgb: np.ndarray, k: int):

    h, w = rgb.shape[:2]

    scale = 400 / max(h, w)

    if scale < 1:

        rgb = cv2.resize(
            rgb,
            (
                int(w * scale),
                int(h * scale)
            ),
            interpolation=cv2.INTER_AREA
        )

    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    hue = hsv[..., 0]
    sat = hsv[..., 1]
    val = hsv[..., 2]

    colorful = (
        (sat > 40) &
        (val > 40)
    )

    green = (
        (hue >= 35) &
        (hue <= 85) &
        colorful
    ).mean()

    sky = (
        (hue >= 90) &
        (hue <= 130) &
        colorful
    ).mean()

    earth = (
        (hue >= 8) &
        (hue <= 30) &
        colorful
    ).mean()

    texture = min(
        cv2.Canny(gray, 100, 200).mean() / 255 * 6,
        1.0
    )

    brightness = val.mean() / 255

    # Dominant colours
    pixels = rgb.reshape(-1, 3).astype(np.float32)

    if len(pixels) > 20000:

        pixels = pixels[
            np.random.default_rng(0).choice(
                len(pixels),
                20000,
                replace=False
            )
        ]

    criteria = (
        cv2.TERM_CRITERIA_EPS +
        cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0
    )

    _, labels, centers = cv2.kmeans(
        pixels,
        k,
        None,
        criteria,
        3,
        cv2.KMEANS_PP_CENTERS
    )

    order = np.argsort(
        -np.bincount(
            labels.flatten(),
            minlength=k
        )
    )

    palette = [
        "#%02x%02x%02x" %
        tuple(int(c) for c in centers[i])
        for i in order
    ]

    return {
        "green": green,
        "sky": sky,
        "earth": earth,
        "texture": texture,
        "brightness": brightness,
        "palette": palette,
        "size": (w, h)
    }


# ============================================================
# NATURAL SCENE VERDICT
# ============================================================

def verdict(r):

    if r["green"] > 0.35:

        return (
            "Lush greenery",
            "Plenty of leaves, grass or moss in this frame."
        )

    if r["sky"] > 0.35:

        return (
            "Open sky or water",
            "Mostly blue tones, so this is likely sky, "
            "sea or a pond."
        )

    if r["earth"] > 0.30:

        return (
            "Soil, bark or stone",
            "Warm brown tones point to earth, wood or rock."
        )

    if r["texture"] > 0.6:

        return (
            "Detailed texture",
            "Lots of fine detail, like a close-up "
            "of petals, fur or bark."
        )

    return (
        "Mixed scene",
        "No single natural element dominates this image."
    )


# ============================================================
# STAT BAR
# ============================================================

def bar(label, value):

    pct = int(round(value * 100))

    return (
        f'<div class="bar-row">'
        f'<span class="bar-label">{label}</span>'
        f'<div class="bar-track">'
        f'<div class="bar-fill" style="width:{pct}%"></div>'
        f'</div>'
        f'<span class="bar-val">{pct}%</span>'
        f'</div>'
    )


# ============================================================
# OPEN-SOURCE CLIP MODEL
# ============================================================

@st.cache_resource
def load_nature_model():

    # For better species accuracy (slower, bigger download), use:
    # model="openai/clip-vit-large-patch14"
    return pipeline(
        "zero-shot-image-classification",
        model="openai/clip-vit-base-patch32"
    )


# ============================================================
# NATURE CATEGORIES
# ============================================================

NATURE_LABELS = [

    "a photo of a tree",
    "a photo of a plant",
    "a photo of a flower",
    "a photo of a leaf",
    "a photo of grass",

    "a photo of a bird",
    "a photo of a butterfly",
    "a photo of an insect",

    "a photo of a lake",
    "a photo of a pond",
    "a photo of a river",
    "a photo of the sea",

    "a photo of soil",
    "a photo of rocks",
    "a photo of a forest",

    "a photo of a natural landscape"
]


# ============================================================
# TREE SPECIES (second-stage identification)
# ============================================================

TREE_SPECIES = [
    "Oak", "Maple", "Pine", "Birch", "Palm", "Banyan", "Neem",
    "Mango", "Eucalyptus", "Willow", "Cedar", "Bamboo", "Coconut",
    "Peepal", "Apple", "Cherry blossom", "Olive", "Cypress",
    "Beech", "Elm", "Ash", "Poplar", "Spruce", "Fir", "Acacia",
    "Teak", "Gulmohar", "Jacaranda", "Magnolia", "Ginkgo"
]

SPECIES_LABELS = {
    f"a photo of a {name.lower()} tree": name
    for name in TREE_SPECIES
}

PLANT_CATEGORIES = ["tree", "plant", "leaf", "forest"]


# ============================================================
# TREE KNOWLEDGE BASE
# ============================================================

TREE_INFO = {
    "Oak": {
        "sci": "Quercus",
        "region": "Northern Hemisphere (Europe, Asia, North America)",
        "size": "20-40 m tall; can live 300+ years",
        "spot": "Lobed leaves and acorns with little caps; deeply ridged bark.",
        "fact": "A single mature oak can support hundreds of insect species, which in turn feed birds."
    },
    "Maple": {
        "sci": "Acer",
        "region": "Northern temperate regions, especially North America and East Asia",
        "size": "10-45 m tall depending on species",
        "spot": "Opposite leaves, often with 3-5 pointed lobes; paired winged seeds.",
        "fact": "Sap from sugar maples is boiled down into maple syrup, and the leaves turn brilliant red in autumn."
    },
    "Pine": {
        "sci": "Pinus",
        "region": "Northern Hemisphere",
        "size": "15-45 m tall; evergreen",
        "spot": "Long needles grouped in bundles of 2-5; woody cones; scaly, plated bark.",
        "fact": "Pines produce sticky resin that seals wounds and protects the tree from insects."
    },
    "Birch": {
        "sci": "Betula",
        "region": "Cool northern regions of Europe, Asia and North America",
        "size": "15-25 m tall",
        "spot": "Thin white or silvery bark that peels in papery strips; small toothed leaves.",
        "fact": "Birches are pioneer trees, among the first to grow back after fire or clearing."
    },
    "Palm": {
        "sci": "Arecaceae (palm family)",
        "region": "Tropical and subtropical regions",
        "size": "5-30 m tall",
        "spot": "Single unbranched trunk topped with a crown of large fan or feather-shaped fronds.",
        "fact": "Palms are not true wood: they are closer to grasses and have no growth rings."
    },
    "Banyan": {
        "sci": "Ficus benghalensis",
        "region": "Indian subcontinent",
        "size": "20-30 m tall; the crown can spread over a huge area",
        "spot": "Thick aerial roots hanging from branches; large, leathery oval leaves.",
        "fact": "Aerial roots grow down and thicken into new trunks, so one tree can look like a small forest. It is India's national tree."
    },
    "Neem": {
        "sci": "Azadirachta indica",
        "region": "Indian subcontinent",
        "size": "15-20 m tall; fast-growing and drought-tolerant",
        "spot": "Compound leaves with serrated leaflets; small white fragrant flowers; yellow olive-like fruit.",
        "fact": "Neem has been used in traditional medicine and as a natural insect repellent for centuries."
    },
    "Mango": {
        "sci": "Mangifera indica",
        "region": "South Asia",
        "size": "15-30 m tall; dense evergreen crown",
        "spot": "Long glossy dark-green leaves with reddish new growth; fruit hanging on long stalks.",
        "fact": "Some mango trees live and fruit for over 100 years."
    },
    "Eucalyptus": {
        "sci": "Eucalyptus",
        "region": "Native to Australia, planted worldwide",
        "size": "Often 30-50 m tall; very fast-growing",
        "spot": "Peeling, patchy bark; narrow curved leaves with a strong menthol scent when crushed.",
        "fact": "Its leaves are rich in oils and are the main food of koalas."
    },
    "Willow": {
        "sci": "Salix",
        "region": "Temperate regions, usually near water",
        "size": "10-25 m tall",
        "spot": "Long narrow leaves; flexible drooping branches; often growing beside rivers and ponds.",
        "fact": "Willow bark contains salicin, the compound that inspired the development of aspirin."
    },
    "Cedar": {
        "sci": "Cedrus",
        "region": "Himalayas and the Mediterranean",
        "size": "30-40 m tall; evergreen",
        "spot": "Clusters of short needles on small knobs; barrel-shaped upright cones; layered branches.",
        "fact": "Cedar wood is aromatic and naturally resists moths and rot."
    },
    "Bamboo": {
        "sci": "Bambusoideae",
        "region": "Asia, Africa and the Americas",
        "size": "Up to 30 m tall",
        "spot": "Hollow, jointed green stems (culms) with slim lance-shaped leaves.",
        "fact": "Bamboo is technically a grass, and some species can grow almost a metre in a single day."
    },
    "Coconut": {
        "sci": "Cocos nucifera",
        "region": "Tropical coastlines",
        "size": "20-30 m tall",
        "spot": "Slender curved trunk topped by huge feathery fronds and clusters of large green or brown nuts.",
        "fact": "Coconuts can float across oceans and sprout on distant shores."
    },
    "Peepal": {
        "sci": "Ficus religiosa",
        "region": "Indian subcontinent and Southeast Asia",
        "size": "20-30 m tall; long-lived",
        "spot": "Heart-shaped leaves with a long drip-tip; leaves flutter in the slightest breeze.",
        "fact": "Sacred in Hinduism, Buddhism and Jainism, and a favourite shelter and food source for birds."
    },
    "Apple": {
        "sci": "Malus domestica",
        "region": "Originally Central Asia, now grown worldwide",
        "size": "4-12 m tall",
        "spot": "Oval toothed leaves; pink-white blossoms in spring; round fruit in autumn.",
        "fact": "There are thousands of apple varieties, and most need pollen from a different variety to produce fruit."
    },
    "Cherry blossom": {
        "sci": "Prunus (ornamental cherries)",
        "region": "Japan and East Asia",
        "size": "5-12 m tall",
        "spot": "Clouds of pink or white flowers in spring; shiny bark with horizontal lines.",
        "fact": "The blossoms last only one to two weeks, which is why the Japanese festival of hanami is so treasured."
    },
    "Olive": {
        "sci": "Olea europaea",
        "region": "Mediterranean basin",
        "size": "8-15 m tall; very long-lived",
        "spot": "Narrow silvery-green leaves; gnarled, twisted trunk; small oval fruit.",
        "fact": "Some olive trees are believed to be over 1,000 years old."
    },
    "Cypress": {
        "sci": "Cupressus",
        "region": "Mediterranean, Asia and North America",
        "size": "20-40 m tall; often tall and narrow",
        "spot": "Tiny scale-like leaves pressed against the twig; small round woody cones.",
        "fact": "Cypress wood is durable and aromatic, and some trees live for many centuries."
    },
    "Beech": {
        "sci": "Fagus",
        "region": "Europe, Asia and North America",
        "size": "25-35 m tall",
        "spot": "Smooth, grey elephant-like bark; oval leaves with wavy edges; spiky husks holding beechnuts.",
        "fact": "Its dense canopy casts such deep shade that little grows beneath it."
    },
    "Elm": {
        "sci": "Ulmus",
        "region": "Temperate Northern Hemisphere",
        "size": "20-35 m tall",
        "spot": "Leaves with a lopsided base and double-toothed edge; flat round papery seeds.",
        "fact": "Dutch elm disease wiped out millions of elms in the 20th century."
    },
    "Ash": {
        "sci": "Fraxinus",
        "region": "Europe, Asia and North America",
        "size": "20-35 m tall",
        "spot": "Compound leaves with 5-11 leaflets in opposite pairs; diamond-patterned bark; winged seeds.",
        "fact": "Ash wood is tough yet springy, which is why it was used for tool handles and baseball bats."
    },
    "Poplar": {
        "sci": "Populus",
        "region": "Northern Hemisphere",
        "size": "20-30 m tall; very fast-growing",
        "spot": "Triangular or heart-shaped leaves on flat stalks that tremble in the wind.",
        "fact": "Many poplars release fluffy cotton-like seeds that drift in early summer."
    },
    "Spruce": {
        "sci": "Picea",
        "region": "Cold northern and mountain regions",
        "size": "20-60 m tall; evergreen",
        "spot": "Stiff, four-sided needles that roll between your fingers; cones hang downward.",
        "fact": "Spruce is a classic Christmas tree and its wood is used for musical instruments."
    },
    "Fir": {
        "sci": "Abies",
        "region": "Cool northern and mountain regions",
        "size": "15-60 m tall; evergreen",
        "spot": "Flat, soft needles that cannot be rolled; cones stand upright on the branches.",
        "fact": "Fir cones fall apart on the tree, so you will rarely find a whole one on the ground."
    },
    "Acacia": {
        "sci": "Acacia",
        "region": "Africa, Australia and Asia",
        "size": "5-25 m tall",
        "spot": "Feathery compound leaves; often thorny; fluffy yellow flower clusters.",
        "fact": "Many acacias enrich the soil with nitrogen and some host ants that defend them from browsing animals."
    },
    "Teak": {
        "sci": "Tectona grandis",
        "region": "South and Southeast Asia",
        "size": "30-40 m tall",
        "spot": "Very large rough leaves; sheds leaves in the dry season; small white flower clusters.",
        "fact": "Teak timber is naturally oily and water-resistant, prized for boats and furniture."
    },
    "Gulmohar": {
        "sci": "Delonix regia",
        "region": "Native to Madagascar, planted across the tropics",
        "size": "10-15 m tall with a wide umbrella crown",
        "spot": "Fern-like leaves and brilliant red-orange flowers in summer; long dark seed pods.",
        "fact": "Also called the flame tree, its summer blooms can cover the whole canopy in scarlet."
    },
    "Jacaranda": {
        "sci": "Jacaranda mimosifolia",
        "region": "South America",
        "size": "10-20 m tall",
        "spot": "Fern-like leaves and clusters of trumpet-shaped purple-blue flowers.",
        "fact": "When it blooms, the flowers carpet the ground in purple."
    },
    "Magnolia": {
        "sci": "Magnolia",
        "region": "Americas and East Asia",
        "size": "5-30 m tall",
        "spot": "Large glossy leaves and big, fragrant cup-shaped flowers.",
        "fact": "Magnolias are among the most ancient flowering plants and were pollinated by beetles before bees evolved."
    },
    "Ginkgo": {
        "sci": "Ginkgo biloba",
        "region": "China",
        "size": "20-35 m tall",
        "spot": "Fan-shaped leaves with a notch in the middle; turn bright gold in autumn.",
        "fact": "Ginkgo is a living fossil: its lineage dates back more than 200 million years."
    },
}


def tree_card_html(species, info):

    rows = [
        ("🌍 Native to", info["region"]),
        ("📏 Size", info["size"]),
        ("🔍 How to spot it", info["spot"]),
        ("💡 Did you know?", info["fact"]),
    ]

    items = "".join(
        f'<div class="tree-fact">'
        f'<span class="tree-key">{escape(k)}</span>'
        f'<span>{escape(v)}</span>'
        f'</div>'
        for k, v in rows
    )

    return (
        '<div class="tree-card">'
        f'<div class="tree-name">{escape(species)} tree</div>'
        f'<div class="tree-sci">{escape(info["sci"])}</div>'
        f'{items}'
        '</div>'
    )


def tree_mission_steps(species):

    return [
        f"Find a {species.lower()} tree near you. Parks, streets and gardens are good places to look.",
        "Study the leaves: their shape, edges and how they attach to the twig.",
        "Touch the bark and describe it as smooth, rough, flaking or ridged.",
        "Look for flowers, fruit, seeds or cones.",
        "Sit quietly for 5 minutes and count the creatures that visit."
    ]


TREE_SUGGESTIONS = [
    ("🎨", "Make a leaf or bark rubbing with paper and a crayon."),
    ("📐", "Measure the trunk by wrapping a string around it at chest height."),
    ("📅", "Photograph the same tree every season to see how it changes."),
    ("🌱", "Plant a native tree or join a local planting drive."),
    ("🤲", "Look, don't harm: skip picking bark or breaking branches."),
]


def list_html(items, ordered=True):

    tag = "ol" if ordered else "ul"

    body = "".join(
        f"<li>{escape(i)}</li>"
        for i in items
    )

    return f'<{tag} class="eco-list">{body}</{tag}>'


# ============================================================
# HABITAT KNOWLEDGE BASE (ponds, lakes, rivers, sea, forest)
# ============================================================

HABITAT_INFO = {
    "pond": {
        "icon": "💧",
        "intro": "A small, still body of freshwater, shallow enough for sunlight to reach the bottom.",
        "rows": [
            ("📏 Approximate depth",
             "Usually 0.5-3 m, and many ponds are under 2 m. The level rises and falls with rain and season."),
            ("🌸 Flowers and plants",
             "Water lily, lotus, water hyacinth, iris, marsh marigold, reeds, cattails and floating duckweed."),
            ("🐸 Creatures",
             "Frogs and tadpoles, dragonflies, damselflies, pond skaters, water beetles, snails, "
             "small fish such as minnows and carp, ducks, herons, kingfishers and turtles."),
            ("🌳 Trees nearby",
             "Willow, alder, poplar and bamboo in cooler areas; coconut palm, banyan and peepal in the tropics."),
            ("💡 Did you know?",
             "Studies in Europe found that small ponds often host more freshwater species than larger lakes or rivers."),
        ],
        "tips": [
            "Look for ripples and count how many different insects skim the surface.",
            "Check the leaves of floating plants for frog spawn or tiny eggs.",
            "Sit still for 5 minutes: dragonflies and birds return when you stop moving.",
            "Clear water with lots of insects usually means a healthy pond.",
            "Keep any litter out of the water, and do not remove plants or animals.",
        ],
        "water": True,
    },
    "lake": {
        "icon": "🏞️",
        "intro": "A large, deep body of still water, big enough to have its own waves and temperature layers.",
        "rows": [
            ("📏 Approximate depth",
             "Typically 5 to over 100 m. The deepest, Lake Baikal in Russia, is about 1,640 m."),
            ("🌸 Flowers and plants",
             "Water lily, lotus, pondweed, reeds, bulrush and irises along the shore."),
            ("🐟 Creatures",
             "Perch, pike, trout and carp, plus ducks, geese, swans, herons, otters, frogs, turtles and dragonflies."),
            ("🌳 Trees nearby",
             "Willow, alder, birch, poplar and cypress along the shoreline."),
            ("💡 Did you know?",
             "Lake Baikal holds roughly a fifth of the world's unfrozen surface fresh water."),
        ],
        "tips": [
            "Scan the shoreline with your eyes first, then the open water, for birds.",
            "Look for rings on the surface where fish are feeding.",
            "Notice how plants change from reeds at the edge to open water further out.",
        ],
        "water": True,
    },
    "river": {
        "icon": "🌊",
        "intro": "Flowing freshwater that carries sediment and nutrients from high ground to the sea.",
        "rows": [
            ("📏 Approximate depth",
             "From under 0.5 m in shallow riffles to several metres in pools. Large rivers can be tens of metres deep in places."),
            ("🌸 Flowers and plants",
             "Water crowfoot, watercress, reeds, irises and tall riverbank grasses."),
            ("🐟 Creatures",
             "Trout, minnows, otters, kingfishers, dippers, mayflies, freshwater crabs and turtles."),
            ("🌳 Trees nearby",
             "Willow, alder, poplar, ash and arjuna trees, whose roots hold the banks together."),
            ("💡 Did you know?",
             "Mayfly larvae are a sign of clean water because they cannot survive in heavy pollution."),
        ],
        "tips": [
            "Watch how fast the water moves in the middle compared with the edges.",
            "Look under overhanging branches for fish and kingfishers.",
            "Check which side of the bank is eroded and which has collected sand or stones.",
        ],
        "water": True,
    },
    "sea": {
        "icon": "🌅",
        "intro": "Salt water that covers most of the planet and shapes the coast.",
        "rows": [
            ("📏 Approximate depth",
             "Coastal shallows are 0-200 m. The average ocean depth is about 3,700 m and the deepest point is nearly 11,000 m."),
            ("🌸 Flowers and plants",
             "Seagrass, seaweed and kelp offshore; sea thrift, sea lavender and beach morning glory on the shore."),
            ("🦀 Creatures",
             "Crabs, shellfish, starfish, jellyfish, many fish, seagulls, sandpipers, sea turtles and dolphins."),
            ("🌳 Trees nearby",
             "Coconut palm, mangrove, casuarina and sea almond in warm regions; windswept pines on dunes elsewhere."),
            ("💡 Did you know?",
             "Marine algae produce a large share of Earth's oxygen, often estimated at around half."),
        ],
        "tips": [
            "Walk the tide line and note three things the sea left behind.",
            "Look in rock pools for crabs, snails and anemones.",
            "Check the tide times first and watch for strong waves.",
        ],
        "water": True,
    },
    "forest": {
        "icon": "🌲",
        "intro": "A habitat dominated by trees, with layers from canopy to leaf litter.",
        "rows": [
            ("📏 Canopy height",
             "Usually 10-50 m above the ground, depending on the forest and climate."),
            ("🌸 Flowers and plants",
             "Ferns, mosses, orchids, bluebells and wildflowers in sunny clearings, plus fungi on the ground."),
            ("🦉 Creatures",
             "Deer, squirrels, foxes, owls, woodpeckers, beetles, ants and butterflies."),
            ("🌳 Trees you may meet",
             "Oak, beech, pine and maple in temperate forests; teak, mango and banyan in tropical ones."),
            ("💡 Did you know?",
             "Scientists have found that trees can exchange nutrients through networks of underground fungi."),
        ],
        "tips": [
            "Look at each layer in turn: canopy, branches, shrubs, ground.",
            "Turn over a fallen log gently and put it back to see who lives underneath.",
            "Close your eyes for a minute and count the different sounds you hear.",
        ],
        "water": False,
    },
}


def habitat_card_html(name, info):

    rows = "".join(
        f'<div class="tree-fact">'
        f'<span class="tree-key">{escape(k)}</span>'
        f'<span>{escape(v)}</span>'
        f'</div>'
        for k, v in info["rows"]
    )

    return (
        '<div class="tree-card">'
        f'<div class="tree-name">{info["icon"]} {escape(name)}</div>'
        f'<div class="tree-sci">{escape(info["intro"])}</div>'
        f'{rows}'
        '</div>'
    )


# ============================================================
# CATEGORY ICONS (replaces the fixed leaf icon)
# ============================================================

CATEGORY_ICONS = {
    "tree": "🌳",
    "plant": "🪴",
    "flower": "🌸",
    "leaf": "🍃",
    "grass": "🌾",
    "bird": "🐦",
    "butterfly": "🦋",
    "insect": "🐞",
    "lake": "🏞️",
    "pond": "🪷",
    "river": "🌊",
    "sea": "🌅",
    "soil": "🪱",
    "rocks": "🪨",
    "forest": "🌲",
    "natural landscape": "⛰️",
}


# ============================================================
# SOIL TYPES (second-stage identification)
# ============================================================

SOIL_LABELS = {
    "a photo of dark black cotton soil": "Black soil",
    "a photo of red soil": "Red soil",
    "a photo of grey-brown alluvial silt soil": "Alluvial soil",
    "a photo of reddish-orange laterite soil with gravel": "Laterite soil",
    "a photo of pale sandy soil": "Sandy soil",
    "a photo of sticky wet clay soil": "Clay soil",
    "a photo of dark crumbly loam garden soil": "Loamy soil",
    "a photo of dry cracked desert soil": "Desert soil",
    "a photo of dark spongy peat soil": "Peaty soil",
}


SOIL_INFO = {
    "Black soil": {
        "intro": "Also called Regur or black cotton soil. Dark, clay-rich and formed from weathered basalt rock.",
        "region": "Deccan Plateau: Maharashtra, Gujarat, Madhya Pradesh, Karnataka, Telangana and Andhra Pradesh.",
        "crops": ["Cotton", "Soybean", "Sugarcane", "Jowar", "Wheat", "Groundnut", "Pulses", "Citrus fruits"],
        "texture": "Very fine clay. Holds moisture for a long time, swells when wet and develops deep cracks when dry.",
        "fertility": "High in calcium, magnesium and potash, but low in nitrogen and organic matter.",
        "fact": "It is called black cotton soil because cotton grows so well in it. Its dark colour comes from minerals in the basalt, not from humus.",
        "improve": "Add compost or green manure and avoid working it when waterlogged.",
    },
    "Red soil": {
        "intro": "Gets its red colour from iron oxide. Usually formed from granite and other ancient crystalline rocks.",
        "region": "Tamil Nadu, Karnataka, Andhra Pradesh, Odisha, Jharkhand and Chhattisgarh.",
        "crops": ["Ragi (finger millet)", "Groundnut", "Pulses", "Potato", "Tobacco", "Cotton (with irrigation)", "Mango", "Cashew"],
        "texture": "Light, porous and well-drained, ranging from sandy to loamy.",
        "fertility": "Low in nitrogen, phosphorus, humus and lime, so it needs fertiliser or manure.",
        "fact": "The same iron that colours the soil red is what rust is made of.",
        "improve": "Mix in compost and farmyard manure, and mulch to hold moisture.",
    },
    "Alluvial soil": {
        "intro": "Fertile silt and sand deposited by rivers over thousands of years.",
        "region": "Indo-Gangetic plain (Punjab to West Bengal), Brahmaputra valley, river deltas and coastal plains, including parts of Gujarat.",
        "crops": ["Rice", "Wheat", "Sugarcane", "Maize", "Jute", "Pulses", "Oilseeds", "Vegetables"],
        "texture": "Fine, soft and loamy. Light grey to pale brown, and it holds water well.",
        "fertility": "Very fertile, rich in potash and lime, though often short of nitrogen.",
        "fact": "Alluvial soil is the most widespread soil type in India and supports a large share of its food production.",
        "improve": "Rotate crops and add nitrogen-rich manure or legumes.",
    },
    "Laterite soil": {
        "intro": "Forms in hot, rainy regions where heavy rain washes nutrients out of the rock. Rich in iron and aluminium.",
        "region": "Western Ghats, Kerala, Konkan coast, Karnataka, Odisha and the hills of Assam and Meghalaya.",
        "crops": ["Cashew", "Tea", "Coffee", "Rubber", "Coconut", "Tapioca", "Areca nut"],
        "texture": "Coarse, gravelly and acidic. Becomes very hard like brick when it dries.",
        "fertility": "Low in nutrients and humus because they are washed away (leaching).",
        "fact": "The name comes from the Latin word 'later', meaning brick. It has been cut into building blocks for centuries.",
        "improve": "Add lime to reduce acidity and plenty of organic matter.",
    },
    "Sandy soil": {
        "intro": "Made of large, loose mineral particles. Warms up quickly and drains fast.",
        "region": "Rajasthan, Kutch and north Gujarat, coastal beaches, river banks and dry regions worldwide.",
        "crops": ["Bajra (pearl millet)", "Groundnut", "Watermelon", "Muskmelon", "Guar", "Carrot", "Date palm"],
        "texture": "Gritty and loose. It will not hold a shape when squeezed.",
        "fertility": "Low. Water and nutrients drain away quickly.",
        "fact": "Drip irrigation and mulching can turn sandy land into productive farms, as in parts of Israel and Rajasthan.",
        "improve": "Add lots of compost and clay-rich material, and use drip irrigation.",
    },
    "Clay soil": {
        "intro": "Made of very tiny particles that pack tightly together.",
        "region": "River basins, floodplains and low-lying areas around the world.",
        "crops": ["Rice (paddy)", "Wheat", "Sugarcane", "Cabbage", "Broccoli", "Chickpea"],
        "texture": "Sticky when wet, hard and cracked when dry. Rolls into a smooth ribbon.",
        "fertility": "Rich in nutrients but drains slowly and can become waterlogged.",
        "fact": "Clay has been used for pots, bricks and tiles for thousands of years.",
        "improve": "Add compost and coarse organic matter to open up the soil, and avoid walking on it when wet.",
    },
    "Loamy soil": {
        "intro": "A balanced mix of sand, silt and clay. Often considered the ideal soil for growing.",
        "region": "River valleys and fertile plains worldwide, and well-kept gardens everywhere.",
        "crops": ["Vegetables", "Wheat", "Maize", "Sugarcane", "Tomato", "Fruit trees", "Flowers"],
        "texture": "Dark, crumbly and soft. Holds a shape when squeezed but breaks apart easily.",
        "fertility": "High. Holds moisture and nutrients while still draining well.",
        "fact": "A healthy loam can hold millions of microbes in a single teaspoon.",
        "improve": "Top up with compost each season to keep it healthy.",
    },
    "Desert soil": {
        "intro": "Dry, light-coloured soil with very little organic matter, found where rainfall is low.",
        "region": "Thar Desert in Rajasthan, Kutch, the Sahara and the Arabian Peninsula.",
        "crops": ["Bajra", "Guar (cluster bean)", "Moth bean", "Barley", "Date palm", "Cumin (with irrigation)"],
        "texture": "Sandy or gravelly with a salty crust in places. Drains almost instantly.",
        "fertility": "Low in humus, but can be productive when irrigated because minerals are plentiful.",
        "fact": "Desert crops like bajra and guar are naturally adapted to survive on very little water.",
        "improve": "Use drip irrigation, windbreaks and mulch to cut water loss.",
    },
    "Peaty soil": {
        "intro": "Dark, spongy soil made of partly decayed plants that built up in waterlogged areas.",
        "region": "Kuttanad in Kerala, the Sundarbans, and cool wet regions such as Ireland, Scotland and Canada.",
        "crops": ["Rice (Kuttanad)", "Potato", "Blueberry", "Cranberry", "Vegetables"],
        "texture": "Soft, light and wet. Very high in organic matter.",
        "fertility": "Rich in organic matter but usually acidic and needs drainage and liming.",
        "fact": "Peat stores huge amounts of carbon, and peatlands hold more than all the world's forests.",
        "improve": "Drain carefully, add lime, and avoid over-draining since dry peat breaks down quickly.",
    },
}


SOIL_SUGGESTIONS = [
    ("✋", "Do the squeeze test: moist soil that holds a shape has more clay."),
    ("🪱", "Count earthworms in a spadeful of soil. More worms usually means healthier soil."),
    ("🍂", "Add leaf litter or compost to feed the soil instead of leaving it bare."),
    ("🧪", "For accurate results, get a lab soil test. In India, the Soil Health Card scheme offers this for farmers."),
    ("🤲", "Dig gently and put the soil back as you found it."),
]


def soil_mission_steps(soil_type):

    return [
        f"Find a spot with {soil_type.lower()} and dig a small handful from the top 10 cm.",
        "Squeeze it: does it crumble (sandy), hold its shape (loamy) or stay sticky (clay)?",
        "Rub a pinch between your fingers: gritty means sand, floury means silt, sticky means clay.",
        "Look closely for roots, worms, insects or tiny fungi threads.",
        "Put the soil back where you found it."
    ]


def soil_card_html(name, info):

    chips = "".join(
        f"<span>{escape(c)}</span>"
        for c in info["crops"]
    )

    rows = [
        ("📍 Where it is found", info["region"]),
        ("🧱 Texture and water", info["texture"]),
        ("🧪 Fertility", info["fertility"]),
        ("🛠️ How to improve it", info["improve"]),
        ("💡 Did you know?", info["fact"]),
    ]

    items = "".join(
        f'<div class="tree-fact">'
        f'<span class="tree-key">{escape(k)}</span>'
        f'<span>{escape(v)}</span>'
        f'</div>'
        for k, v in rows
    )

    return (
        '<div class="tree-card">'
        f'<div class="tree-name">🪱 {escape(name)}</div>'
        f'<div class="tree-sci">{escape(info["intro"])}</div>'
        '<div class="tree-fact">'
        '<span class="tree-key">🌾 Crops that grow well</span>'
        f'<div class="crop-chips">{chips}</div>'
        '</div>'
        f'{items}'
        '</div>'
    )


# ============================================================
# FLOWER SPECIES (second-stage identification)
# ============================================================

FLOWER_SPECIES = [
    "Rose", "Lotus", "Marigold", "Sunflower", "Jasmine", "Hibiscus",
    "Tulip", "Daisy", "Orchid", "Water lily", "Lavender", "Dahlia",
    "Chrysanthemum", "Daffodil", "Lily", "Bougainvillea", "Frangipani",
    "Zinnia", "Poppy", "Cosmos", "Carnation", "Petunia", "Iris",
    "Gerbera", "Periwinkle"
]

FLOWER_LABELS = {
    f"a photo of a {name.lower()} flower": name
    for name in FLOWER_SPECIES
}


FLOWER_INFO = {
    "Rose": {
        "icon": "🌹",
        "sci": "Rosa",
        "intro": "One of the most loved flowers in the world, grown for beauty, perfume and oil.",
        "region": "Native to Asia, with some species from Europe and North America. Grown worldwide.",
        "bloom": "Spring to autumn; many garden varieties bloom repeatedly.",
        "spot": "Layered velvety petals, thorny stems and toothed compound leaves.",
        "uses": "Gardens, bouquets, rose water, perfume, gulkand and rose oil.",
        "care": "Needs 6+ hours of sun, well-drained soil and regular pruning.",
        "fact": "Fossils show roses are around 35 million years old.",
    },
    "Lotus": {
        "icon": "🪷",
        "sci": "Nelumbo nucifera",
        "intro": "A sacred water plant whose flowers rise above the surface on tall stalks.",
        "region": "India, East Asia and Australia; grows in ponds and slow rivers.",
        "bloom": "Summer, with flowers opening in the morning and closing at night.",
        "spot": "Large pink or white flower, round leaves held above water that bead water off.",
        "uses": "Religious offerings, edible seeds and roots, and traditional medicine.",
        "care": "Needs still, shallow water, full sun and rich muddy soil.",
        "fact": "Lotus leaves stay clean because of a self-cleaning surface effect named after the plant.",
    },
    "Marigold": {
        "icon": "🏵️",
        "sci": "Tagetes erecta",
        "intro": "A bright orange and yellow flower used widely in Indian festivals and garlands.",
        "region": "Native to Mexico and Central America, now grown across India.",
        "bloom": "Rainy season through winter.",
        "spot": "Dense ruffled pom-pom blooms in orange or yellow, with feathery strong-smelling leaves.",
        "uses": "Garlands, festival decoration, natural dyes and pest-repelling companion planting.",
        "care": "Easy to grow in full sun and ordinary soil.",
        "fact": "Gardeners plant marigolds beside vegetables because their scent helps deter some pests.",
    },
    "Sunflower": {
        "icon": "🌻",
        "sci": "Helianthus annuus",
        "intro": "A tall annual with a huge golden flower head, grown for seeds and oil.",
        "region": "Native to North America, now grown in Russia, Ukraine, India and many other countries.",
        "bloom": "Summer to early autumn.",
        "spot": "Large yellow rays around a brown disc, with a thick hairy stem and heart-shaped leaves.",
        "uses": "Sunflower oil, snack seeds and bird feed.",
        "care": "Needs full sun, deep soil and space to grow tall.",
        "fact": "A sunflower head is made up of up to thousands of tiny flowers.",
    },
    "Jasmine": {
        "icon": "🌸",
        "sci": "Jasminum",
        "intro": "A fragrant climbing shrub with small white star-shaped flowers.",
        "region": "Tropical and warm regions of Asia, including India, plus Africa and Australia.",
        "bloom": "Mostly summer evenings, depending on the species.",
        "spot": "Small white flowers with a strong sweet scent and thin glossy leaves.",
        "uses": "Garlands, hair adornment, perfume, tea and religious offerings.",
        "care": "Grows well in sun to part shade, with regular watering and support to climb.",
        "fact": "Jasmine flowers are often picked at night because their scent is strongest then.",
    },
    "Hibiscus": {
        "icon": "🌺",
        "sci": "Hibiscus rosa-sinensis",
        "intro": "A tropical shrub with big, showy trumpet-shaped flowers.",
        "region": "East Asia, widely grown across India and the tropics.",
        "bloom": "Almost all year in warm climates; each flower lasts about a day.",
        "spot": "Large red, pink or yellow flowers with a long central column of stamens.",
        "uses": "Worship, hair care, herbal tea (from roselle) and ornamental hedges.",
        "care": "Full sun, plenty of water and a warm climate.",
        "fact": "Each bloom lasts only a day, but the plant keeps producing new ones.",
    },
    "Tulip": {
        "icon": "🌷",
        "sci": "Tulipa",
        "intro": "A spring bulb flower with cup-shaped blooms in nearly every colour.",
        "region": "Central Asia and Turkey; famous in the Netherlands and Kashmir.",
        "bloom": "Early to mid spring.",
        "spot": "A single cup-shaped flower on a smooth upright stem with broad blue-green leaves.",
        "uses": "Ornamental gardens and cut flowers.",
        "care": "Plant bulbs in autumn in well-drained soil and a cool climate.",
        "fact": "In 17th century Holland, tulip bulbs became so valuable that their prices crashed in the first well-known speculative bubble.",
    },
    "Daisy": {
        "icon": "🌼",
        "sci": "Bellis perennis",
        "intro": "A small, cheerful flower common on lawns and meadows.",
        "region": "Europe and western Asia; now widespread in temperate regions.",
        "bloom": "Spring to autumn.",
        "spot": "White petals around a yellow centre, on a short stalk above a rosette of leaves.",
        "uses": "Ornamental, and the petals are edible in salads.",
        "care": "Easy in sun or partial shade with moderately moist soil.",
        "fact": "The name comes from 'day's eye' because the flower closes at night and opens at dawn.",
    },
    "Orchid": {
        "icon": "🌸",
        "sci": "Orchidaceae (orchid family)",
        "intro": "One of the largest plant families, with intricate flowers in many shapes.",
        "region": "Almost every continent; most diverse in the tropics, including north-east India.",
        "bloom": "Varies by species; blooms often last weeks to months.",
        "spot": "Symmetrical flower with a distinct lip-shaped petal, often on arching stems.",
        "uses": "Ornamental plants, cut flowers and vanilla, which comes from an orchid.",
        "care": "Bright indirect light, good airflow and a coarse bark-based mix.",
        "fact": "There are over 25,000 orchid species, and vanilla is the only orchid crop grown for food flavouring at large scale.",
    },
    "Water lily": {
        "icon": "🪷",
        "sci": "Nymphaea",
        "intro": "A floating pond flower with flat round leaves that rest on the water.",
        "region": "Worldwide in still fresh water, including India.",
        "bloom": "Summer, with flowers opening by day or night depending on the species.",
        "spot": "Flowers sit at or just above the surface, with round leaves split by a notch.",
        "uses": "Ornamental ponds, and shelter for fish and frogs.",
        "care": "Still water, full sun and soil planted in a pot under the pond.",
        "fact": "Unlike lotus, water lily leaves float on the surface instead of standing above it.",
    },
    "Lavender": {
        "icon": "💜",
        "sci": "Lavandula",
        "intro": "A fragrant purple herb loved by bees and perfumers.",
        "region": "Mediterranean region, now grown in many dry, sunny places.",
        "bloom": "Early to late summer.",
        "spot": "Spikes of small purple flowers above narrow silvery-green leaves.",
        "uses": "Essential oil, perfumes, sachets and cooking.",
        "care": "Full sun, dry well-drained soil and little watering.",
        "fact": "Its name comes from the Latin word for washing, because Romans used it in baths.",
    },
    "Dahlia": {
        "icon": "🌸",
        "sci": "Dahlia",
        "intro": "A tuberous plant with layered, geometric blooms in almost any colour.",
        "region": "Mexico and Central America; Mexico's national flower.",
        "bloom": "Mid summer until the first frost.",
        "spot": "Large, many-petalled flowers on tall stems with dark green divided leaves.",
        "uses": "Gardens and cut flowers.",
        "care": "Full sun, rich soil and staking for tall types.",
        "fact": "Dahlia tubers were once eaten by the Aztecs.",
    },
    "Chrysanthemum": {
        "icon": "🌼",
        "sci": "Chrysanthemum (Chrysanthemum x morifolium)",
        "intro": "A popular autumn flower with dense, layered petals.",
        "region": "East Asia, especially China and Japan; widely grown in India.",
        "bloom": "Autumn to early winter.",
        "spot": "Many-petalled round or shaggy heads with lobed, aromatic leaves.",
        "uses": "Garlands, decoration, and chrysanthemum tea in East Asia.",
        "care": "Full sun, regular watering and pinching back for bushier plants.",
        "fact": "It is the national flower of Japan and the symbol of its imperial family.",
    },
    "Daffodil": {
        "icon": "🌼",
        "sci": "Narcissus",
        "intro": "A bulb flower with a trumpet-shaped centre that heralds spring.",
        "region": "Europe and North Africa; grown in cool climates worldwide.",
        "bloom": "Late winter to spring.",
        "spot": "Yellow or white petals around a central trumpet, with long flat leaves.",
        "uses": "Ornamental gardens and cut flowers. All parts are toxic if eaten.",
        "care": "Plant bulbs in autumn in sun or part shade with well-drained soil.",
        "fact": "Animals usually avoid daffodils because they contain toxic compounds.",
    },
    "Lily": {
        "icon": "🌸",
        "sci": "Lilium",
        "intro": "A tall bulb plant with large, often fragrant trumpet-shaped flowers.",
        "region": "Temperate Northern Hemisphere, including Asia, Europe and North America.",
        "bloom": "Early to late summer.",
        "spot": "Six showy petals, prominent stamens and long narrow leaves up the stem.",
        "uses": "Ornamental gardens and cut flowers. Toxic to cats.",
        "care": "Sun for the flowers and cool, shaded roots in well-drained soil.",
        "fact": "True lilies grow from bulbs; many plants called lilies, such as water lilies, are unrelated.",
    },
    "Bougainvillea": {
        "icon": "💗",
        "sci": "Bougainvillea glabra",
        "intro": "A vigorous climber whose colourful 'petals' are actually leaf-like bracts.",
        "region": "South America; extremely common in Indian gardens and streets.",
        "bloom": "Mostly dry season, and it can bloom almost all year in warm regions.",
        "spot": "Papery pink, magenta, orange or white bracts around tiny white flowers, with thorny stems.",
        "uses": "Hedges, walls, balconies and ornamental landscaping.",
        "care": "Full sun, little water once established and light pruning.",
        "fact": "The bright parts are bracts, and the real flowers are the small white tubes inside.",
    },
    "Frangipani": {
        "icon": "🌸",
        "sci": "Plumeria",
        "intro": "A tropical tree with waxy, sweet-scented flowers, also called champa.",
        "region": "Central America and the Caribbean; widely planted in India and the tropics.",
        "bloom": "Summer to autumn.",
        "spot": "Five-petalled white, yellow or pink flowers with a yellow centre, on thick bare branches.",
        "uses": "Temple offerings, garlands, leis and perfume.",
        "care": "Full sun, very well-drained soil and little water.",
        "fact": "Frangipani flowers smell strongest at night, which helps attract moths.",
    },
    "Zinnia": {
        "icon": "🌸",
        "sci": "Zinnia elegans",
        "intro": "A colourful, easy annual that attracts butterflies and bees.",
        "region": "Mexico and Central America; common in Indian gardens.",
        "bloom": "Summer to autumn.",
        "spot": "Daisy-like or double flowers in bright colours on rough, hairy stems.",
        "uses": "Cut flowers and pollinator gardens.",
        "care": "Full sun and regular water; sow seeds directly in the soil.",
        "fact": "Zinnias were the first flowers grown in space, on the International Space Station.",
    },
    "Poppy": {
        "icon": "🌺",
        "sci": "Papaver",
        "intro": "A delicate flower with silky, paper-thin petals and a seed capsule.",
        "region": "Temperate Europe and Asia; some species are grown in India under licence.",
        "bloom": "Late spring to summer.",
        "spot": "Four crinkled petals, often red with a dark centre, and a round seed pod.",
        "uses": "Ornamental, and poppy seeds are used in cooking.",
        "care": "Full sun and poor, well-drained soil; seeds scatter easily.",
        "fact": "Red poppies are a symbol of remembrance for soldiers in many countries.",
    },
    "Cosmos": {
        "icon": "🌸",
        "sci": "Cosmos bipinnatus",
        "intro": "A light, airy flower that sways on tall thin stems.",
        "region": "Mexico; naturalised in many warm regions including parts of India.",
        "bloom": "Summer to autumn.",
        "spot": "Simple pink, white or orange petals with a yellow centre, and fine feathery leaves.",
        "uses": "Pollinator gardens and cut flowers.",
        "care": "Full sun and average soil; it grows well even without extra fertiliser.",
        "fact": "The name comes from the Greek word 'kosmos', meaning order or harmony.",
    },
    "Carnation": {
        "icon": "🌸",
        "sci": "Dianthus caryophyllus",
        "intro": "A long-lasting, ruffled flower with a spicy clove scent.",
        "region": "Mediterranean region; grown worldwide as a cut flower.",
        "bloom": "Late spring to summer.",
        "spot": "Frilly, fringed petals on slender stems with narrow blue-grey leaves.",
        "uses": "Bouquets, corsages and cut flowers.",
        "care": "Full sun and well-drained, slightly alkaline soil.",
        "fact": "Carnations can last for two weeks or more after being cut.",
    },
    "Petunia": {
        "icon": "🌸",
        "sci": "Petunia x hybrida",
        "intro": "A popular bedding plant that fills pots and hanging baskets with colour.",
        "region": "South America; grown worldwide in gardens.",
        "bloom": "Spring through autumn, or the cool season in warm climates like India.",
        "spot": "Funnel-shaped flowers in pink, purple, white or striped, with sticky hairy leaves.",
        "uses": "Hanging baskets, borders and containers.",
        "care": "Full sun, regular watering and deadheading old flowers.",
        "fact": "Petunias are related to tomatoes and tobacco.",
    },
    "Iris": {
        "icon": "💜",
        "sci": "Iris",
        "intro": "An elegant flower named after the Greek goddess of the rainbow.",
        "region": "Temperate Northern Hemisphere, including Europe, Asia and North America.",
        "bloom": "Spring to early summer.",
        "spot": "Three upright petals and three drooping 'falls' above sword-shaped leaves.",
        "uses": "Ornamental gardens, cut flowers and perfume from the dried roots of some species.",
        "care": "Full sun and well-drained soil; some types prefer wet edges of ponds.",
        "fact": "The name 'iris' means rainbow in Greek, for the many colours the flower comes in.",
    },
    "Gerbera": {
        "icon": "🌼",
        "sci": "Gerbera jamesonii",
        "intro": "A bold, daisy-like flower in vivid colours, popular in bouquets.",
        "region": "South Africa; widely grown in greenhouses including in India.",
        "bloom": "Spring to autumn, and almost year-round under cover.",
        "spot": "Large daisy-like head on a long leafless stalk above a rosette of leaves.",
        "uses": "Cut flowers and decorative pots.",
        "care": "Bright light, good drainage and not too much water on the crown.",
        "fact": "Gerbera is one of the most popular cut flowers in the world.",
    },
    "Periwinkle": {
        "icon": "🌸",
        "sci": "Catharanthus roseus",
        "intro": "A hardy flower known in India as sadabahar, meaning always in bloom.",
        "region": "Madagascar; naturalised across tropical regions including India.",
        "bloom": "Almost all year in warm climates.",
        "spot": "Five flat pink or white petals with a darker eye, on glossy dark leaves.",
        "uses": "Ornamental ground cover and a source of compounds used in cancer medicine.",
        "care": "Sun, little water and well-drained soil. Toxic if eaten.",
        "fact": "Medicines for some cancers were developed from compounds first found in this plant.",
    },
}


FLOWER_SUGGESTIONS = [
    ("📸", "Take close-ups of the petals, centre and leaves to compare shapes and colours."),
    ("🐝", "Watch the flower for 5 minutes and count the bees, butterflies or birds that visit."),
    ("📝", "Sketch the flower and label its petals, stamens and stem."),
    ("🌱", "Plant a few native flowers or seeds to support local pollinators."),
    ("🤲", "Look, don't pick: leave flowers on the plant so insects and seeds can do their work."),
]


def flower_mission_steps(flower):

    return [
        f"Find a {flower.lower()} or a similar flower in a garden, park or roadside.",
        "Count the petals and note their colour, shape and texture.",
        "Look at the centre of the flower and find the stamens or the middle disc.",
        "Smell it gently, if it is safe, and describe the scent in three words.",
        "Watch for visitors for 5 minutes: which insects or birds come by?"
    ]


def flower_card_html(name, info):

    rows = [
        ("🌍 Native to", info["region"]),
        ("📅 When it blooms", info["bloom"]),
        ("🔍 How to spot it", info["spot"]),
        ("🧺 Uses", info["uses"]),
        ("🌱 Care", info["care"]),
        ("💡 Did you know?", info["fact"]),
    ]

    items = "".join(
        f'<div class="tree-fact">'
        f'<span class="tree-key">{escape(k)}</span>'
        f'<span>{escape(v)}</span>'
        f'</div>'
        for k, v in rows
    )

    return (
        '<div class="tree-card">'
        f'<div class="tree-name">{info["icon"]} {escape(name)}</div>'
        f'<div class="tree-sci">Scientific name: {escape(info["sci"])}</div>'
        f'<p>{escape(info["intro"])}</p>'
        f'{items}'
        '</div>'
    )


# ============================================================
# CLEAN CLIP LABEL
# ============================================================

def clean_label(label):

    label = label.replace("a photo of a ", "")
    label = label.replace("a photo of an ", "")
    label = label.replace("a photo of the ", "")
    label = label.replace("a photo of ", "")

    return label.capitalize()


# ============================================================
# AI NATURE IDENTIFICATION
# ============================================================

def identify_nature(image):

    classifier = load_nature_model()

    # Stage 1: general category
    results = sorted(
        classifier(image, candidate_labels=NATURE_LABELS),
        key=lambda x: x["score"],
        reverse=True
    )

    best = results[0]
    category = clean_label(best["label"])
    reliable = best["score"] >= 0.30

    species = None
    soil_type = None
    flower = None

    # Stage 2a: tree species
    if reliable and category.lower() in PLANT_CATEGORIES:

        sp_results = sorted(
            classifier(
                image,
                candidate_labels=list(SPECIES_LABELS.keys())
            ),
            key=lambda x: x["score"],
            reverse=True
        )

        if sp_results[0]["score"] >= 0.20:
            species = SPECIES_LABELS[sp_results[0]["label"]]

    # Stage 2b: soil type
    elif reliable and category.lower() == "soil":

        soil_results = sorted(
            classifier(
                image,
                candidate_labels=list(SOIL_LABELS.keys())
            ),
            key=lambda x: x["score"],
            reverse=True
        )

        if soil_results[0]["score"] >= 0.20:
            soil_type = SOIL_LABELS[soil_results[0]["label"]]

    # Stage 2c: flower species
    elif reliable and category.lower() == "flower":

        fl_results = sorted(
            classifier(
                image,
                candidate_labels=list(FLOWER_LABELS.keys())
            ),
            key=lambda x: x["score"],
            reverse=True
        )

        if fl_results[0]["score"] >= 0.20:
            flower = FLOWER_LABELS[fl_results[0]["label"]]

    return category, species, soil_type, flower, reliable


# ============================================================
# DYNAMIC OUTDOOR MISSION
# ============================================================

def generate_mission(name, reliable):

    if not reliable:

        return (
            "🔎 Take another photo",

            "Move closer to the natural object "
            "and take a clearer photo in daylight.",

            "Spend 5 minutes observing something "
            "interesting around you."
        )

    name_lower = name.lower()

    if any(
        word in name_lower
        for word in ["tree", "plant", "flower", "leaf", "grass"]
    ):

        return (
            "🌳 Explore a plant",

            "Find another plant nearby and compare "
            "its leaves, colour and shape.",

            "Look for one insect or bird visiting the plant."
        )

    if "bird" in name_lower:

        return (
            "🐦 Go bird watching",

            "Spend 5 minutes observing birds around you.",

            "Notice how one bird moves, feeds or communicates."
        )

    if "butterfly" in name_lower:

        return (
            "🦋 Find another butterfly",

            "Look around flowers and plants for another butterfly.",

            "Observe its movement without disturbing it."
        )

    if "insect" in name_lower:

        return (
            "🐝 Find another insect",

            "Look around plants and flowers for another insect.",

            "Observe its movement without disturbing it."
        )

    if any(
        word in name_lower
        for word in ["lake", "pond", "river", "sea"]
    ):

        return (
            "💧 Explore the water",

            "Walk near the water and observe its surroundings.",

            "Find three different natural elements near the water."
        )

    if "forest" in name_lower:

        return (
            "🌲 Explore the forest",

            "Take a short walk and observe the different "
            "plants around you.",

            "Find three different shades of green."
        )

    if "soil" in name_lower:

        return (
            "🌱 Explore the ground",

            "Observe the soil and look for small signs of life.",

            "Look for leaves, insects, roots or tiny plants."
        )

    if "rock" in name_lower:

        return (
            "🪨 Explore natural textures",

            "Look for another rock or natural surface nearby.",

            "Compare its colour, shape and texture."
        )

    return (
        "🌿 Explore your surroundings",

        "Spend at least 5 minutes outside observing nature.",

        "Find one natural object you haven't noticed before."
    )


# ============================================================
# TOUCH GRASS SCORE
# ============================================================

def calculate_score(res, reliable):

    score = 30

    if reliable:
        score += 30

    if res["green"] > 0.20:
        score += 10

    if res["texture"] > 0.30:
        score += 10

    if res["brightness"] > 0.40:
        score += 10

    if (
        res["green"] > 0.10
        or res["sky"] > 0.10
        or res["earth"] > 0.10
    ):
        score += 10

    return min(score, 100)


# ============================================================
# HEADER
# ============================================================

html(
    """
    <div class="eco-hero">

        <p class="eco-title">
            EcoLens
        </p>

        <p class="eco-sub">
            Photograph a leaf, a pond or a patch of soil
            and see what it's made of:
            colours, greenery and texture.
        </p>

    </div>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Settings")

    k = st.slider(
        "Colours in palette",
        3,
        8,
        5
    )

    st.caption(
        "Image analysis runs in your session. "
        "No uploaded image is stored by EcoLens."
    )


# ============================================================
# INPUT
# ============================================================

tab_upload, tab_camera = st.tabs(
    [
        "Upload a photo",
        "Use camera"
    ]
)


with tab_upload:

    uploaded = st.file_uploader(
        "Drop a JPG or PNG here",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )


with tab_camera:

    snapped = st.camera_input(
        "Take a photo",
        label_visibility="collapsed"
    )


source = uploaded or snapped


# ============================================================
# NO IMAGE
# ============================================================

if source is None:

    html(
        """
        <div class="eco-panel">

            <h3>
                Nothing to look at yet
            </h3>

            Upload a photo or open the camera
            to get started.

            Close-ups in daylight work best.

        </div>
        """
    )


# ============================================================
# IMAGE PROVIDED
# ============================================================

else:

    # LOAD IMAGE

    try:

        image = load_image(source)

    except Exception:

        st.error(
            "That file couldn't be read as an image. "
            "Try a JPG or PNG."
        )

        st.stop()


    # OPENCV ANALYSIS

    with st.spinner("Looking closely..."):

        res = analyze(
            np.array(image),
            k
        )


    title, note = verdict(res)


    # ORIGINAL IMAGE

    show_image(image, "Your photo")


    # SCENE VERDICT

    html(
        f"""
        <div class="eco-panel">

            <p class="eco-verdict">
                {escape(title)}
            </p>

            <p class="eco-note">
                {escape(note)}
            </p>

        </div>
        """
    )


    # IMAGE STATISTICS

    html(
        '<div class="eco-panel">'
        '<h3>What’s in the frame</h3>'

        + bar("Greenery", res["green"])
        + bar("Sky or water", res["sky"])
        + bar("Earth tones", res["earth"])
        + bar("Texture", res["texture"])
        + bar("Brightness", res["brightness"])

        + "</div>"
    )


    # COLOUR PALETTE

    swatches = "".join(
        f'<div style="background:{c}"></div>'
        for c in res["palette"]
    )

    chips = "".join(
        f'<span>'
        f'<i style="background:{c}"></i>'
        f'{c}'
        f'</span>'
        for c in res["palette"]
    )

    html(
        f"""
        <div class="eco-panel">

            <h3>
                Colour palette
            </h3>

            <div class="swatches">
                {swatches}
            </div>

            <div class="hexes">
                {chips}
            </div>

        </div>
        """
    )


    # IMAGE DETAILS

    with st.expander("Image details"):

        st.write(
            f"Original size: "
            f"{res['size'][0]} × "
            f"{res['size'][1]} px"
        )

        st.caption(
            "OpenCV results describe visual properties "
            "such as colour and texture. They do not "
            "identify exact species."
        )


    # ========================================================
    # AI IDENTIFICATION
    # ========================================================

    st.markdown("## 🤖 AI Nature Identification")

    with st.spinner("AI is exploring your image..."):

        try:

            category, species, soil_type, flower, reliable = identify_nature(image)

            if reliable:

                icon = CATEGORY_ICONS.get(category.lower(), "🌿")

                if species:
                    headline = f"{species} tree"
                    subline = "Best match for this photo"
                    icon = "🌳"

                elif soil_type:
                    headline = soil_type
                    subline = "Best match for this soil"
                    icon = "🪱"

                elif flower:
                    headline = flower
                    subline = FLOWER_INFO[flower]["sci"]
                    icon = FLOWER_INFO[flower]["icon"]

                else:
                    headline = category
                    subline = (
                        "Species could not be determined"
                        if category.lower() in PLANT_CATEGORIES
                        else "Detected in your photo"
                    )

                html(
                    f"""
                    <div class="ai-result">
                        <div class="ai-icon">{icon}</div>
                        <div class="ai-title">{escape(headline)}</div>
                        <div class="ai-confidence">{escape(subline)}</div>
                    </div>
                    """
                )

            else:

                html(
                    """
                    <div class="ai-warning">
                        <div class="ai-warning-title">
                            ⚠️ Couldn't identify this one
                        </div>
                        <div class="ai-description">
                            Try a closer photo of the leaves or bark,
                            with better lighting and less background clutter.
                        </div>
                    </div>
                    """
                )

        except Exception as e:

            st.error(f"AI identification failed: {e}")

            category = "unknown"
            species = None
            soil_type = None
            flower = None
            reliable = False


    # ========================================================
    # ABOUT SECTION
    # ========================================================

    info = TREE_INFO.get(species) if species else None

    if reliable and info:

        st.markdown("## 🌳 About this tree")

        html(tree_card_html(species, info))

    elif reliable and soil_type:

        st.markdown(f"## 🪱 About {soil_type.lower()}")

        html(soil_card_html(soil_type, SOIL_INFO[soil_type]))

        st.caption(
            "Soil type is estimated from colour and texture in the photo. "
            "Wetness and lighting can change how soil looks, so confirm "
            "with a lab soil test before choosing crops."
        )

    elif reliable and flower:

        st.markdown(f"## 🌸 About {flower.lower()}")

        html(flower_card_html(flower, FLOWER_INFO[flower]))

    elif reliable and category.lower() == "flower":

        html(
            """
            <div class="eco-panel">
                <h3>Want the flower's name?</h3>
                Take a close-up of a single bloom in daylight, with the
                petals and centre clearly visible and a plain background,
                and the AI can suggest the flower and its scientific name.
            </div>
            """
        )

    elif reliable and category.lower() == "soil":

        html(
            """
            <div class="eco-panel">
                <h3>Want the soil type?</h3>
                Take a close-up of dry soil in daylight, with no plants or
                shadows in the frame, and the AI can suggest the soil type.
            </div>
            """
        )

    elif reliable and category.lower() in HABITAT_INFO:

        st.markdown(f"## 📖 About this {category.lower()}")

        html(
            habitat_card_html(
                category,
                HABITAT_INFO[category.lower()]
            )
        )

    elif reliable and category.lower() in PLANT_CATEGORIES:

        html(
            """
            <div class="eco-panel">
                <h3>Want a species name?</h3>
                Take a close-up of a single leaf, the bark or the
                flowers against a plain background. Close-ups help
                the AI tell similar trees apart.
            </div>
            """
        )


    # ========================================================
    # TOUCH GRASS MISSION
    # ========================================================

    st.markdown("## 🌱 Touch Grass Mission")

    if reliable and info:

        html(
            f"""
            <div class="mission-card">
                <div class="mission-title">
                    🌳 Meet the {escape(species)} tree
                </div>
                <p>Complete these steps outdoors:</p>
                {list_html(tree_mission_steps(species), ordered=True)}
                <p>📵 Put your phone away while completing the mission.</p>
            </div>
            """
        )

        sugg = "".join(
            f'<div class="sugg-row"><span>{icon}</span>'
            f'<span>{escape(text)}</span></div>'
            for icon, text in TREE_SUGGESTIONS
        )

        html(
            f"""
            <div class="eco-panel">
                <h3>💡 Suggestions</h3>
                {sugg}
            </div>
            """
        )

    elif reliable and soil_type:

        html(
            f"""
            <div class="mission-card">
                <div class="mission-title">
                    🪱 Get to know {escape(soil_type.lower())}
                </div>
                <p>Complete these steps outdoors:</p>
                {list_html(soil_mission_steps(soil_type), ordered=True)}
                <p>📵 Put your phone away while completing the mission.</p>
            </div>
            """
        )

        sugg = "".join(
            f'<div class="sugg-row"><span>{icon}</span>'
            f'<span>{escape(text)}</span></div>'
            for icon, text in SOIL_SUGGESTIONS
        )

        html(
            f"""
            <div class="eco-panel">
                <h3>💡 Suggestions</h3>
                {sugg}
            </div>
            """
        )

    elif reliable and flower:

        html(
            f"""
            <div class="mission-card">
                <div class="mission-title">
                    {FLOWER_INFO[flower]["icon"]} Meet the {escape(flower.lower())}
                </div>
                <p>Complete these steps outdoors:</p>
                {list_html(flower_mission_steps(flower), ordered=True)}
                <p>📵 Put your phone away while completing the mission.</p>
            </div>
            """
        )

        sugg = "".join(
            f'<div class="sugg-row"><span>{icon}</span>'
            f'<span>{escape(text)}</span></div>'
            for icon, text in FLOWER_SUGGESTIONS
        )

        html(
            f"""
            <div class="eco-panel">
                <h3>💡 Suggestions</h3>
                {sugg}
            </div>
            """
        )

    else:

        mission_title, mission_text, mission_extra = generate_mission(
            category,
            reliable
        )

        html(
            f"""
            <div class="mission-card">

                <div class="mission-title">
                    {escape(mission_title)}
                </div>

                <p>{escape(mission_text)}</p>

                <p>👀 {escape(mission_extra)}</p>

                <p>
                    📵 Put your phone away while
                    completing the mission.
                </p>

            </div>
            """
        )

        hab = HABITAT_INFO.get(category.lower()) if reliable else None

        if hab:

            tips = list(hab["tips"])

            if hab["water"]:
                tips.append("Stay a safe distance from the edge and never enter unknown water alone.")

            sugg = "".join(
                f'<div class="sugg-row"><span>💡</span>'
                f'<span>{escape(t)}</span></div>'
                for t in tips
            )

            html(
                f"""
                <div class="eco-panel">
                    <h3>Suggestions</h3>
                    {sugg}
                </div>
                """
            )


    # ========================================================
    # TOUCH GRASS SCORE
    # ========================================================

    st.markdown("### 🌿 Touch Grass Score")

    score = calculate_score(res, reliable)

    st.progress(
        score / 100,
        text=f"{score}/100"
    )

    if score >= 80:

        st.caption(
            "🌳 Excellent! This looks like a great "
            "opportunity to explore outside."
        )

    elif score >= 60:

        st.caption(
            "🌱 Nice discovery! Now explore "
            "a little more."
        )

    else:

        st.caption(
            "🚶 Take another photo outside "
            "and keep exploring."
        )