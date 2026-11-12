import streamlit as st
st.set_page_config(page_title="Eco root AI", layout="wide")

st.title("Eco root AI")
st.subheader("Turning Agricultural or Kitchen wastes into "
             "Sustainable Solutions.")

st.write("Welcome to Eco root AI. \n "
         "Explore agricultural waste based biofertilizer recommendations "
         "and Crop & pH compatibility.")
# Language selector
lang = st.sidebar.radio("Language / ভাষা", ["English", "বাংলা"])

if lang == "English":
    st.info("Select a feature from the left sidebar to begin.")
    st.markdown("""
    ### How Eco Root Works:
    1. **Input Crop & Scraps:** Select your target plants and available kitchen waste.
    2. **Biohazard Screening:** Real-time checks filter out harmful materials.
    3. **Compatibility & Soil Check:** Avoid antagonistic crops and match soil pH.
    4. **Action Card:** Get a practical 3-step recipe (*Clean → Prepare → Feed*).
    """)
else:
    st.info("শুরু করতে বাঁদিকের সাইডবার থেকে একটি ফিচার বেছে নিন।")
    st.markdown("""
    ### ইকো রুট কীভাবে কাজ করে:
    ১. **ফসল ও বর্জ্য নির্বাচন:** আপনার লক্ষ্য ফসল এবং রান্নাঘরের বর্জ্য বাছুন।
    ২. **নিরাপত্তা যাচাই:** ক্ষতিকর পদার্থ স্বয়ংক্রিয়ভাবে বাদ দেওয়া হয়।
    ৩. **মাটি ও ফসলের সামঞ্জস্য:** ক্ষতিকারক ফসলের মিশ্রণ এবং মাটির pH নির্ণয়।
    ৪. **নির্দেশিকা কার্ড:** ৩-ধাপের সহজ প্রস্তুত প্রণালী (*পরিষ্কার → প্রস্তুত → প্রয়োগ*)।
    """)