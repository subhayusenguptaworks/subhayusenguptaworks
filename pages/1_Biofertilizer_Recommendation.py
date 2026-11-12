import os
import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


st.set_page_config(page_title="Ecoroot AI", layout="wide")

st.title("Biofertilizer recommendations")
st.subheader("Explore vegetable-waste-based fertilizer options")
st.info("Educational prototype: recommendations require "
        "verified agricultural evidence and testing")

#Starters crop categories, not an exhaustive state list
crops = {"Cereals": ["Rice(Paddy)", "Wheat", "Maize", "Millets", "Barley"],
         "Pulses": ["Lentil(Masur)", "Chickpea(Gram)", "Mung Bean", "Urad(Maskalai)", "Pigeon Pea"],
         "Oilseeds": ["Mustard", "Groundnut", "Sesame", "Linseed"],
         "Fibre crops": ["Jute", "Cotton", "Hemp"],
         "Vegetables": ["Potato", "Tomato", "Brinjal", "Bitter Gourd", "Bottle Gourd", "Radish", "Carrot", "Cauliflower", "Onion", "Cucumber", "Beans", "Cabbage"],
         "Fruits": ["Apple", "Banana", "Guava", "Mango", "Litchi", "Papaya"],
         "Plantation spice": ["Tea", "Sugarcane", "Ginger"],
         "Turmeric": ["Cardamom", "Cinchona"]}

#Target crop details
st.header("1. Select target crop")
category = st.selectbox("Crop category", list(crops.keys()),key="crop_category_1")
crop = st.multiselect("Crop", crops[category],key="Target_crop")

#Crop and other details section
st.header("2. Select crop waste to be used as ingredient")
category_2 = st.selectbox("Crop category", list(crops.keys()),key="crop_category_2")
crop_2 = st.multiselect("Crop", crops[category_2],key="Ingredient_crop")

st.header("3. Select available materials")
materials = ["vegetable scraps", "fruit peels", "dry leaves", "Other"]
available = st.multiselect("Available materials", materials)
hazardous_items = ["cooked food", "meat", "oil", "plastic", "dairy", "bone", "fish"]

def check_safety(text):
    """Return a list of hazardous items found in the free-text description."""
    text = text.lower()
    return [item for item in hazardous_items if item in text]
if "Other" in available:
    other_material = st.text_input("Describe the other material")
    flagged = check_safety(other_material)
    if flagged:
        st.error(f"Biohazard: {', '.join(flagged)} will attract pathogens and pests. "
                 "Do not add this to the mix.")
    else:
        st.success("No hazardous items detected in your description.")
else:
    other_material = ""

soil_status = st.selectbox("Do you have soil status?", ["Yes", "No"])
if soil_status == "Yes":
    soil_pH = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
else:
    soil_pH = 6.5

#Recommended pH values for all crops listed
pH_ranges = {"Cereals": [6.0,7.5],
             "Pulses": [5.5,7.2],
             "Oilseeds": [5.3,7.5],
             "Vegetables": [6.0,7.0],
             "Fruits": [5.5,7.5],
             "Plantation spice": [4.0,7.5],
             "Fibre crops": [5.0,7.0],}

#Final result
st.header("4. Your ingredients information and the compatibility is below")
if st.button("Analyze my ingredients"):
    st.subheader("Your project profile")
    st.write("Target Crop category:", category)
    st.write("Selected Crop:", crop)
    st.write("Selected ingredient crop category:", category_2)
    st.write("Selected ingredient crop:", crop_2)
    st.write("Selected materials:", available)
    if other_material:
        st.write("Other material:", other_material)
    if soil_pH is not None and category in pH_ranges:
        low, high = pH_ranges[category]
        st.write("Soil pH:", soil_pH)
        if soil_pH < low:
            st.warning(f"Soil pH {soil_pH} is below pH range.")
        elif soil_pH > high:
            st.warning(f"Soil pH {soil_pH} is above pH range.")
        else:
            st.success(f"Soil pH {soil_pH} is within pH range.")

    # --- GEMINI API CALL REPLACEMENT ---
    if not crop:
        st.warning("Please select at least one target crop.")
    elif not crop_2 and not available:
        st.warning("Please select at least one waste ingredient or material.")
    else:
        with st.spinner("Generating evidence-based biofertilizer formulation..."):
            all_scraps = crop_2 + available
            if other_material:
                all_scraps.append(other_material)

            effective_ph = soil_pH if soil_pH is not None else 6.5

            prompt = f"""
            You are an expert organic agronomist.
            Generate a safe, home biofertilizer recipe using the following details:
            - Target Crop: {', '.join(crop)}
            - Available Scrap Feedstock: {', '.join(all_scraps)}
            - Soil pH: {effective_ph}

            Output strictly in this 3-step format:
            1. Clean: Washing, drying, or sorting guidelines to prevent mold and pests.
            2. Prepare: Method (steeping, aerobic fermentation, drying/grinding) and timeline.
            3. Feed: Volumetric dosage per pot, water dilution ratio (enforce standard 1:10 dilution buffer), and frequency.
            """

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            st.markdown("---")
            st.markdown("### Action Card: Clean $\\to$ Prepare $\\to$ Feed")
            st.info(response.text)