import streamlit as st
st.set_page_config(page_title="Veg2Grow AI", layout="wide")

st.title("Veg2Grow AI")
st.subheader("Explore vegetable-waste-based fertilizer options")
st.info("Educational prototype: recommendations "
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

#Crop and other details section
st.header("1. Select your crop")

category = st.selectbox("Crop category", list(crops.keys()))
crop = st.multiselect("Crop", crops[category])

st.header("2. Select available materials")
materials = ["vegetable scraps", "fruit peels", "dry leaves", "mature compost", "commercial biofertilizer", "Other"]
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
    soil_pH = None

#Recommended pH values for all crops listed
pH_ranges = {"Cereals": [6.0,7.5],
             "Pulses": [5.5,7.2],
             "Oilseeds": [5.3,7.5],
             "Vegetables": [6.0,7.0],
             "Fruits": [5.5,7.5],
             "Plantation spice": [4.0,7.5],
             "Fibre crops": [5.0,7.0],}

#Final result
st.header("3. Your ingredients information and the compatibility is below")
if st.button("Analyze my ingredients"):
    st.subheader("Your project profile")
    st.write("Crop category:", category)
    st.write("Selected Crop:", crop)
    st.write("Selected materials:", available)
    if other_material:
        st.write("Other material:", other_material)
    if soil_pH is not None and category in pH_ranges:
        low, high = pH_ranges[category]
        st.write("Soil pH:", soil_pH)
        if soil_pH < low:
            st.warning(f"Soil pH  {soil_pH} is below pH range.")
        elif soil_pH > high:
            st.warning(f"Soil pH {soil_pH} is above pH range.")
        else:
            st.success(f"Soil pH {soil_pH} is within pH range.")
    st.warning("No fertilizer formula generated. "
               "Next stage is checking crop compatibility, "
               "material property and verified scientific evidence")
    st.success("Input collected successfully. "
               "Next task is to build the evidence-based recommendation engine")

#Crop compatibility check
Incompatible_pairs = [({"Tomato","Potato"}, "Both share late blight disease and compete heavily for nightshade nutrients."),
                      ({"Onion", "Beans"}, "Onions release biochemicals that stunt N2 fixing bacteria in bean roots"),
                      ({"Tomato", "Cabbage"}, "Cabbage stunts tomato growth and competes for heavy Nitrogen"),
                      ({"Maize", ''})]
#test check gi1  k