import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="EcoRoot AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
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
    st.divider()

CONTENT = {
    "English": {
        "title": "🌱 EcoRoot AI",
        "sub": "Turning Agricultural & Kitchen Waste into Sustainable Solutions",
        "feat_header": "FEATURES AVAILABLE",
        "features": [
            "🛡️ Smart Ingredient Selection & Biohazard Screening",
            "✅ Verification of Usable Ingredient Matching",
            "🧪 Adaptive Soil pH Engine (Vinegar/Soda Triage)",
            "🌾 pH & Companion Compatibility Check",
            "📋 Custom Organic Recipe Formulation"
        ],
        "work_header": "HOW IT WORKS?",
        "steps": [
            ("Step 1: Crop & Bio-Waste Input Layer (Bilingual UI)",
             "Instant English/বাংলা toggle enabling users to input target crops, co-planting status, and available kitchen scraps."),
            ("Step 2: Deterministic Safety Guardrails & Early Exit",
             "Hard-coded pathogen/pest filter auto-rejecting meat, dairy, oil, and non-biodegradables; immediately halts execution on biohazard inputs."),
            ("Step 3: Multi-Crop Compatibility Engine",
             "Calculates mathematical tolerance intersections across co-planted crops and auto-triggers rescue strategies (partitioning, spot-feeding) for conflicting roots."),
            ("Step 4: Soil Calibration & Safe-Mode Baseline",
             "Maps tested soil pH or runs interactive vinegar/soda triage; defaults unverified soils to pH 6.5 with a mandatory 1:10 dilution buffer."),
            ("Step 5: Visual Action Card",
             "Renders the final status badge alongside a standardized 3-step biofertilizer recipe (Clean → Prepare → Feed) with exact dosage and dilution.")
        ],
        "cta": "🚀 Launch Unified EcoRoot Engine →"
    },
    "বাংলা": {
        "title": "🌱 ইকোরুট এআই (EcoRoot AI)",
        "sub": "কৃষি ও রান্নাঘরের বর্জ্য থেকে নিরাপদ ও টেকসই জৈব সার সমাধান",
        "feat_header": "উপলব্ধ বৈশিষ্ট্যসমূহ (FEATURES)",
        "features": [
            "🛡️ স্মার্ট উপাদান নির্বাচন ও জৈব-নিরাপত্তা যাচাই",
            "✅ ব্যবহারযোগ্য উপাদানের সঠিক সামঞ্জস্য যাচাই",
            "🧪 অ্যাডাপ্টিভ মাটির pH ইঞ্জিন (ভিনেগার/সোডা পরীক্ষা)",
            "🌾 ফসলের সহাবস্থান ও pH সামঞ্জস্যতা পরীক্ষা",
            "📋 কাস্টম জৈব সারের রেসিপি তৈরি"
        ],
        "work_header": "এটি কীভাবে কাজ করে?",
        "steps": [
            ("ধাপ ১: ফসল ও জৈব-বর্জ্য ইনপুট (দ্বিভাষিক ইন্টারফেস)",
             "বাংলা/English টগলের মাধ্যমে লক্ষ্য ফসল, সহ-চাষের অবস্থা এবং রান্নাঘরের বর্জ্য নির্বাচন।"),
            ("ধাপ ২: নিরাপত্তা গার্ডরেইল ও তাৎক্ষণিক বিরতি",
             "মাংস, দুগ্ধজাত পদার্থ, তেল এবং অপচনশীল বর্জ্য শনাক্ত হলে সাথে সাথে প্রক্রিয়া বন্ধ করে দেয়।"),
            ("ধাপ ৩: মাল্টি-ক্রপ সামঞ্জস্যতা ইঞ্জিন",
             "একাধিক ফসলের pH সহনশীলতার গাণিতিক ছেদ হিসাব করে এবং বিরোধপূর্ণ শিকড়ের জন্য বিকল্প কৌশল (পার্টিশনিং, স্পট-ফিডিং) বাতলে দেয়।"),
            ("ধাপ ৪: মাটির pH নির্ণয় ও সেফ-মোড বেসলাইন",
             "পরীক্ষিত pH অথবা ভিনেগার/বেকিং সোডা পরীক্ষার মাধ্যমে মাটির অবস্থা যাচাই; অজানা মাটির ক্ষেত্রে pH 6.5 এবং ১:১০ অনুপাতে জলের মিশ্রণ নিশ্চিত করে।"),
            ("ধাপ ৫: ভিজ্যুয়াল অ্যাকশন কার্ড",
             "চূড়ান্ত স্ট্যাটাস ব্যাজসহ ৩-ধাপের জৈব সার প্রস্তুত প্রণালী (পরিষ্কার → প্রস্তুত → প্রয়োগ), সঠিক মাত্রা ও প্রয়োগের সময়সূচি প্রদান করে।")
        ],
        "cta": "🚀 ইকোরুট ইঞ্জিন শুরু করুন →"
    }
}

t = CONTENT[st.session_state.lang]

st.title(t["title"])
st.markdown(f"##### {t['sub']}")
st.divider()

# Features Pill Grid (Matches Top Half of Poster)
st.subheader(t["feat_header"])
f_col1, f_col2 = st.columns(2)
for i, feat in enumerate(t["features"][:4]):
    with (f_col1 if i % 2 == 0 else f_col2):
        st.success(f"**{feat}**")
st.success(f"**{t['features'][4]}**")

st.divider()

# 5-Step Pipeline (Matches Bottom Half of Poster)
st.subheader(t["work_header"])
for step_title, step_desc in t["steps"]:
    with st.container(border=True):
        st.markdown(f"**{step_title}**")
        st.write(step_desc)

st.divider()

# Launch Button to the Unified Pipeline Page
st.page_link(
    "pages/1_Biofertilizer_Recommendation.py",
    label=t["cta"],
    use_container_width=True
)