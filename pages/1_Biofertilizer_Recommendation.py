import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="EcoRoot AI — Unified Engine",
    page_icon="🧪",
    layout="wide"
)

if "lang" not in st.session_state:
    st.session_state.lang = "English"

with st.sidebar:
    st.markdown("### ⚙️ Language / ভাষা")
    st.session_state.lang = st.radio(
        "Select Language",
        ["English", "বাংলা"],
        index=0 if st.session_state.lang == "English" else 1,
        label_visibility="collapsed"
    )

UI = {
    "English": {
        "title": "🧪 Unified Biofertilizer & Crop Compatibility Engine",
        "sub": "5-Step Deterministic Screening + Gemini 3.8 Agronomist Formulation",
        "s1": "Step 1: Crops & Kitchen Waste",
        "target_cat": "Filter Target Crop Category",
        "target_crops": "Select Target Crop(s) (Select 2+ across any category to check co-planting)",
        "scrap_cat": "Crop Waste Source Category (Optional)",
        "scrap_crops": "Select Crop Residue / Waste",
        "kitchen_mat": "Select Available Kitchen & Garden Materials",
        "other_in": "Describe any additional waste (e.g., banana peel, egg shells, meat)",
        "s2": "Step 2: Biohazard and Safety Check",
        "safe_ok": "Biohazard Screening Passed: No meat, dairy, oils, or non-biodegradables detected.",
        "safe_err": "BIOHAZARD DETECTED ({items}): Attracts pathogens and pests. Execution halted immediately! Remove hazardous items to proceed.",
        "s3": "Step 3: Companion Crop & Soil pH Analysis",
        "no_crop": "Select at least one target crop in Step 1 to run compatibility checks.",
        "conflict_hdr": "Antagonistic Crop Conflict Detected!",
        "rescue_msg": "Rescue Strategy Triggered: Use root partitioning (separate beds/grow-bags) and targeted spot-feeding rather than shared trench fertilization.",
        "no_conflict": "No known allelopathic or pest conflicts among selected crops.",
        "ph_overlap": "Calculated Mathematical Soil pH Intersection: {low:.1f} – {high:.1f}",
        "ph_disjoint": "Zero pH Overlap! Selected crops cannot share soil ({low:.1f} vs {high:.1f}). Rescue Strategy: Grow in partitioned containers with separate pH-buffered feeds.",
        "s4": "Step 4: Soil pH Calibration ",
        "soil_mode": "Select Soil pH Calibration Method",
        "modes": [
            "Tested Soil pH (Known Value)",
            "Interactive Vinegar & Baking Soda Triage",
            "Unverified Soil (Safe-Mode Baseline: pH 6.5 + 1:10 Buffer)"
        ],
        "ph_num": "Enter Tested Soil pH",
        "vinegar_q": "1. Add vinegar to soil sample: Does it fizz?",
        "soda_q": "2. Add baking soda + water to soil sample: Does it fizz?",
        "yes_no": ["No", "Yes"],
        "triage_alk": "Triage Result: Alkaline Soil (~pH 7.8). Recipe will emphasize mild organic acidifiers.",
        "triage_acid": "Triage Result: Acidic Soil (~pH 5.2). Recipe will avoid acidic citrus/tea mixes.",
        "triage_neut": "Triage Result: Neutral Soil (~pH 6.5). Balanced nutrient release.",
        "safemode_info": "Safe-Mode Baseline Active: Defaulting to pH 6.5 with a mandatory 1:10 water dilution buffer.",
        "ph_warn_low": "Soil pH ({ph}) is below the target crop window ({low:.1f}–{high:.1f}).",
        "ph_warn_high": "Soil pH ({ph}) is above the target crop window ({low:.1f}–{high:.1f}).",
        "ph_match": "Soil pH ({ph}) matches the target crop window ({low:.1f}–{high:.1f}).",
        "s5": "Step 5: Visual Action Card",
        "gen_btn": "⚡ Generate Verified Action Card",
        "no_scrap": "Select at least one crop residue or kitchen scrap in Step 1.",
        "spinner": "Formulating 3-step recipe via Gemini 3.8...",
        "badge_safe": "STATUS BADGE: VERIFIED SAFE & COMPATIBLE",
        "badge_rescue": "STATUS BADGE: RESCUE MODE (PARTITIONING + 1:10 BUFFER REQUIRED)"
    },
    "বাংলা": {
        "title": "🧪 সমন্বিত জৈব সার ও ফসল সামঞ্জস্যতা ইঞ্জিন",
        "sub": "৫-ধাপের নিরাপত্তা যাচাই + Gemini 3.8 কৃষিবিদ ফর্মুলেশন",
        "s1": "ধাপ ১: ফসল ও জৈব-বর্জ্য ইনপুট",
        "target_cat": "লক্ষ্য ফসলের বিভাগ ফিল্টার করুন",
        "target_crops": "লক্ষ্য ফসল নির্বাচন করুন (সহ-চাষ যাচাই করতে একাধিক বাছুন)",
        "scrap_cat": "ফসলের বর্জ্যের বিভাগ (ঐচ্ছিক)",
        "scrap_crops": "বর্জ্য হিসেবে ব্যবহৃত ফসল বাছুন",
        "kitchen_mat": "রান্নাঘর ও বাগানের উপলব্ধ উপাদান বাছুন",
        "other_in": "অন্য কোনো বর্জ্য থাকলে লিখুন (যেমন: কলার খোসা, ডিমের খোসা)",
        "s2": "ধাপ ২: নিরাপত্তা গার্ডরেইল ও তাৎক্ষণিক বিরতি",
        "safe_ok": "নিরাপত্তা যাচাই সফল: কোনো মাংস, দুগ্ধজাত পদার্থ, তেল বা প্লাস্টিক পাওয়া যায়নি।",
        "safe_err": "জৈব-ঝুঁকি শনাক্ত হয়েছে ({items}): এটি রোগজীবাণু ও পোকামাকড় আকর্ষণ করে। প্রক্রিয়া তাৎক্ষণিকভাবে বন্ধ করা হলো!",
        "s3": "ধাপ ৩: মাল্টি-ক্রপ সামঞ্জস্যতা ও pH ছেদ ইঞ্জিন",
        "no_crop": "সামঞ্জস্যতা যাচাই করতে ধাপ ১-এ অন্তত একটি লক্ষ্য ফসল নির্বাচন করুন।",
        "conflict_hdr": "ফসলের মধ্যে বিরোধপূর্ণ সম্পর্ক শনাক্ত হয়েছে!",
        "rescue_msg": "বিকল্প কৌশল (Rescue Strategy): আলাদা বেড বা গ্রো-ব্যাগ (Partitioning) ব্যবহার করুন এবং প্রতিটি গাছের গোড়ায় আলাদাভাবে সার দিন (Spot-feeding)।",
        "no_conflict": "নির্বাচিত ফসলগুলোর মধ্যে কোনো ক্ষতিকর প্রতিযোগিতা পাওয়া যায়নি।",
        "ph_overlap": "সহ-চাষের গাণিতিক মাটির pH সীমা: {low:.1f} – {high:.1f}",
        "ph_disjoint": "অসামঞ্জস্যপূর্ণ মাটির pH! নির্বাচিত ফসলগুলোর pH চাহিদা মেলে না ({low:.1f} বনাম {high:.1f})। বিকল্প কৌশল: আলাদা পাত্রে চাষ করুন।",
        "s4": "ধাপ ৪: মাটির pH নির্ণয় ও সেফ-মোড বেসলাইন",
        "soil_mode": "মাটির pH নির্ধারণের পদ্ধতি বেছে নিন",
        "modes": [
            "পরীক্ষিত মাটির pH (জানা মান)",
            "ঘরোয়া ভিনেগার ও বেকিং সোডা পরীক্ষা",
            "অজানা মাটি (সেফ-মোড বেসলাইন: pH 6.5 + ১:১০ বাফার)"
        ],
        "ph_num": "পরীক্ষিত মাটির pH লিখুন",
        "vinegar_q": "১. মাটিতে ভিনেগার দিলে কি বুদবুদ (fizz) ওঠে?",
        "soda_q": "২. মাটিতে বেকিং সোডা ও জল দিলে কি বুদবুদ ওঠে?",
        "yes_no": ["না (No)", "হ্যাঁ (Yes)"],
        "triage_alk": "পরীক্ষার ফলাফল: ক্ষারীয় মাটি (~pH 7.8)। হালকা অম্লীয় জৈব উপাদানে জোর দেওয়া হবে।",
        "triage_acid": "পরীক্ষার ফলাফল: অম্লীয় মাটি (~pH 5.2)। অতিরিক্ত সাইট্রাস বা চাপাতা বর্জ্য এড়ানো হবে।",
        "triage_neut": "পরীক্ষার ফলাফল: নিরপেক্ষ মাটি (~pH 6.5)। সুষম পুষ্টি প্রদান করবে।",
        "safemode_info": "সেফ-মোড বেসলাইন সক্রিয়: pH 6.5 এবং বাধ্যতামূলক ১:১০ জলের অনুপাত নির্ধারণ করা হয়েছে।",
        "ph_warn_low": "মাটির pH ({ph}) নির্ধারিত সীমার ({low:.1f}–{high:.1f}) চেয়ে কম।",
        "ph_warn_high": "মাটির pH ({ph}) নির্ধারিত সীমার ({low:.1f}–{high:.1f}) চেয়ে বেশি।",
        "ph_match": "মাটির pH ({ph}) নির্ধারিত সীমার ({low:.1f}–{high:.1f}) মধ্যে আছে।",
        "s5": "ধাপ ৫: ভিজ্যুয়াল অ্যাকশন কার্ড",
        "gen_btn": "⚡ অ্যাকশন কার্ড তৈরি করুন",
        "no_scrap": "রেসিপি তৈরির আগে ধাপ ১-এ অন্তত একটি বর্জ্য উপাদান নির্বাচন করুন।",
        "spinner": "Gemini 3.8-এর মাধ্যমে ৩-ধাপের রেসিপি তৈরি হচ্ছে...",
        "badge_safe": "স্ট্যাটাস ব্যাজ: নিরাপদ এবং সামঞ্জস্যপূর্ণ",
        "badge_rescue": "স্ট্যাটাস ব্যাজ: রেসকিউ মোড (পার্টিশনিং + ১:১০ বাফার আবশ্যক)"
    }
}

t = UI[st.session_state.lang]

CROPS_DB = {
    "Cereals": {"Rice (Paddy)": (5.5, 6.5), "Wheat": (6.0, 7.0), "Maize": (5.8, 6.8), "Millets": (5.5, 7.0), "Barley": (6.0, 7.5)},
    "Pulses": {"Lentil (Masur)": (6.0, 7.0), "Chickpea (Gram)": (6.0, 7.5), "Mung Bean": (6.2, 7.2), "Urad (Maskalai)": (6.0, 7.0), "Pigeon Pea": (5.5, 7.0)},
    "Oilseeds": {"Mustard": (6.0, 7.5), "Groundnut": (5.8, 6.5), "Sesame": (5.5, 7.0), "Linseed": (6.0, 7.0)},
    "Fibre Crops": {"Jute": (6.0, 7.0), "Cotton": (5.8, 7.0), "Hemp": (6.0, 7.5)},
    "Vegetables": {
        "Potato": (5.0, 6.0), "Tomato": (6.0, 6.8), "Brinjal": (5.5, 6.5),
        "Bitter Gourd": (6.0, 6.7), "Bottle Gourd": (6.0, 7.0), "Radish": (6.0, 7.0),
        "Carrot": (6.0, 6.8), "Cauliflower": (6.0, 7.0), "Onion": (6.0, 7.0),
        "Cucumber": (5.8, 6.8), "Beans": (6.0, 6.8), "Cabbage": (6.2, 7.2)
    },
    "Fruits": {"Apple": (5.8, 6.8), "Banana": (5.5, 6.5), "Guava": (5.0, 7.0), "Mango": (5.5, 7.0), "Litchi": (5.5, 6.5), "Papaya": (6.0, 6.8)},
    "Plantation & Spices": {"Tea": (4.5, 5.5), "Sugarcane": (6.0, 7.5), "Ginger": (5.5, 6.5), "Turmeric": (5.5, 6.5), "Cardamom": (5.0, 6.0)}
}

ALL_CROP_PH = {crop: ph for cat in CROPS_DB.values() for crop, ph in cat.items()}

INCOMPATIBLE_PAIRS = [
    ({"Tomato", "Potato"}, "Both share late blight (Phytophthora infestans) and compete heavily for nightshade nutrients."),
    ({"Onion", "Beans"}, "Onions release root exudates that inhibit nitrogen-fixing Rhizobium bacteria on bean roots."),
    ({"Tomato", "Cabbage"}, "Heavy brassica nitrogen uptake stunts tomato fruiting and increases pest pressure."),
    ({"Maize", "Tomato"}, "Severe canopy shading and shared Helicoverpa fruitworm/earworm pest pressure.")
]

HAZARDOUS_KEYWORDS = [
    "cooked food", "meat", "chicken", "mutton", "pork", "beef", "fish", "bone",
    "oil", "ghee", "butter", "plastic", "dairy", "milk", "cheese", "paneer",
    "curd", "glass", "metal", "battery", "paint", "chemical", "feces", "pet waste"
]

st.title(t["title"])
st.caption(t["sub"])
st.divider()

# ==========================================
# STEP 1: CROP & BIO-WASTE INPUT LAYER
# ==========================================
st.subheader(t["s1"])
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        selected_cats = st.multiselect(
            t["target_cat"],
            list(CROPS_DB.keys()),
            default=["Vegetables"]
        )
        available_target_crops = [
            c for cat in selected_cats for c in CROPS_DB[cat].keys()
        ]
        target_crops = st.multiselect(
            t["target_crops"],
            available_target_crops,
            default=["Tomato"] if "Tomato" in available_target_crops else []
        )

with col2:
    with st.container(border=True):
        scrap_cat = st.selectbox(t["scrap_cat"], list(CROPS_DB.keys()), index=4)
        scrap_crops = st.multiselect(t["scrap_crops"], list(CROPS_DB[scrap_cat].keys()))
        kitchen_materials = st.multiselect(
            t["kitchen_mat"],
            ["Vegetable Scraps", "Fruit Peels", "Dry Leaves", "Used Tea/Coffee Grounds", "Crushed Eggshells"]
        )
        other_material = st.text_input(t["other_in"])

# Collect all selected waste items first so Step 2 knows if input exists
all_scraps = scrap_crops + kitchen_materials
if other_material.strip():
    all_scraps.append(other_material.strip())

# ==========================================
# STEP 2: DETERMINISTIC SAFETY GUARDRAILS
# ==========================================
flagged_hazards = [
    kw for kw in HAZARDOUS_KEYWORDS if kw in other_material.lower()
]

# Only show a banner if a biohazard is actually triggered
if flagged_hazards:
    st.subheader(t["s2"])
    st.error(t["safe_err"].format(items=", ".join(flagged_hazards).upper()))
    st.stop()

# ==========================================
# STEP 3: MULTI-CROP COMPATIBILITY ENGINE
# ==========================================
rescue_required = False

if not target_crops:
    st.warning(t["no_crop"])
    st.stop()

selected_set = set(target_crops)
conflicts = [
    (pair, reason) for pair, reason in INCOMPATIBLE_PAIRS if pair.issubset(selected_set)
]

lows = [ALL_CROP_PH[c][0] for c in target_crops]
highs = [ALL_CROP_PH[c][1] for c in target_crops]
intersect_low = max(lows)
intersect_high = min(highs)
ph_disjoint = intersect_low > intersect_high

# Only show Step 3 alert boxes if there is a real crop conflict or pH mismatch
if conflicts or ph_disjoint:
    st.subheader(t["s3"])
    rescue_required = True
    if conflicts:
        st.error(f"⚠️ {t['conflict_hdr']}")
        for pair, reason in conflicts:
            st.markdown(f"- **{' + '.join(pair)}:** {reason}")
        st.warning(f"🛠️ **{t['rescue_msg']}**")
    if ph_disjoint:
        st.error(t["ph_disjoint"].format(low=intersect_low, high=intersect_high))

# ==========================================
# STEP 4: SOIL CALIBRATION & SAFE-MODE
# ==========================================
st.subheader(t["s4"])
with st.container(border=True):
    mode = st.radio(t["soil_mode"], t["modes"], horizontal=True)

    if mode == t["modes"][0]:
        soil_pH = st.number_input(t["ph_num"], min_value=3.0, max_value=10.0, value=6.5, step=0.1)
    elif mode == t["modes"][1]:
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            v_fizz = st.selectbox(t["vinegar_q"], t["yes_no"])
        with t_col2:
            s_fizz = st.selectbox(t["soda_q"], t["yes_no"])

        if v_fizz == t["yes_no"][1]:
            soil_pH = 7.8
            st.warning(t["triage_alk"])
        elif s_fizz == t["yes_no"][1]:
            soil_pH = 5.2
            st.warning(t["triage_acid"])
        else:
            soil_pH = 6.5
            st.caption(f"✓ {t['triage_neut']}")
    else:
        soil_pH = 6.5
        st.caption(f"ℹ️ {t['safemode_info']}")

    # Only show a big banner if soil pH is outside the target window
    soil_out_of_range = False
    if not ph_disjoint:
        if soil_pH < intersect_low:
            st.warning(t["ph_warn_low"].format(ph=soil_pH, low=intersect_low, high=intersect_high))
            rescue_required = True
            soil_out_of_range = True
        elif soil_pH > intersect_high:
            st.warning(t["ph_warn_high"].format(ph=soil_pH, low=intersect_low, high=intersect_high))
            rescue_required = True
            soil_out_of_range = True

# ==========================================
# STEP 5: VISUAL ACTION CARD
# ==========================================
st.subheader(t["s5"])

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_ai_recipe(api_key: str, prompt_text: str) -> tuple[str, str]:
    """Call Gemini with a strict 8-second timeout and instant local fallback."""
    client = genai.Client(api_key=api_key, http_options={"timeout": 8})
    # Try active Flash models in order of speed
    for model_name in ["gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=prompt_text
            )
            if res and res.text:
                return res.text, f"Cloud AI ({model_name})"
        except Exception:
            continue
    return "", "Offline Engine"


if st.button(t["gen_btn"], type="primary", use_container_width=True):
    if not all_scraps:
        st.warning(t["no_scrap"])
    else:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        out_lang = "Bengali (বাংলা)" if st.session_state.lang == "বাংলা" else "English"
        rescue_note = (
            "Include root partitioning and spot-feeding rescue instructions for conflicting crops."
            if rescue_required else "Crops are compatible for shared bed application."
        )

        prompt = f"""
        You are an expert organic agronomist. Respond entirely in {out_lang}.
        Formulate a safe home biofertilizer recipe based on these verified parameters:
        - Target Crop(s): {', '.join(target_crops)}
        - Target pH Intersection Window: {intersect_low:.1f} to {intersect_high:.1f}
        - Calibrated Soil pH: {soil_pH}
        - Available Bio-Waste Feedstock: {', '.join(all_scraps)}
        - Co-Planting Note: {rescue_note}

        Format strictly into 3 concise sections with bullet points:
        ### 1. Clean (Sorting & Prep)
        - Specific washing, chopping, or sun-drying steps to prevent mold and pathogens.
        ### 2. Prepare (Formulation & pH Calibration)
        - Exact method (aerobic composting, liquid steeping, or dried powder), timeline, and how to adjust for the {soil_pH} soil pH.
        ### 3. Feed (Dosage, 1:10 Dilution & Schedule)
        - Exact volumetric dosage per plant/pot, mandatory 1:10 water dilution ratio, frequency, and {rescue_note}
        """

        with st.spinner(t["spinner"]):
            recipe_text, source_label = ("", "Offline Engine")
            if api_key:
                recipe_text, source_label = fetch_ai_recipe(api_key, prompt)

            # Instant deterministic fallback if API is offline or times out after 8s
            if not recipe_text:
                scraps_str = ", ".join(all_scraps)
                crops_str = ", ".join(target_crops)
                ph_tip = (
                    "Add 1 tbsp crushed eggshells per liter to buffer acidic soil."
                    if soil_pH < 6.0 else
                    "Add diluted citrus/tea steep to gently lower alkaline soil."
                    if soil_pH > 7.2 else
                    "Maintain neutral pH balance with aerated rainwater."
                )
                recipe_text = f"""
### 1. Clean (Sorting & Prep)
- Rinse **{scraps_str}** thoroughly to remove surface salts, stickers, and pesticide residues.
- Chop into <2 cm pieces to maximize microbial surface area and prevent anaerobic rot.

### 2. Prepare (Formulation & pH Calibration)
- Submerge chopped feedstock in chlorine-free water at a **1:3 waste-to-water ratio** in a breathable container.
- Ferment aerobically for **5–7 days**, stirring daily until sweet-earthy fermentation completes.
- **pH Calibration ({soil_pH}):** {ph_tip}

### 3. Feed (Dosage, 1:10 Dilution & Schedule)
- Strain liquid concentrate and apply a **mandatory 1:10 dilution** (100 mL concentrate per 1 L water).
- Apply **250–500 mL per plant** every **10–14 days** at the root zone for **{crops_str}**.
- **Strategy:** {rescue_note}
                """

            with st.container(border=True):
                if rescue_required:
                    st.warning(f"🛡️ **{t['badge_rescue']}**")
                else:
                    st.success(f"✅ **{t['badge_safe']}**")
                st.caption(f"⚡ Source: {source_label}")
                st.divider()
                st.markdown(recipe_text)