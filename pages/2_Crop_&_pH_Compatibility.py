import streamlit as st

st.title("Crop and pH Compatibility")
st.subheader("Explore whether your crops are compatible to grow together.")
st.info("Educational prototype: checking requires "
        "input from user about crops(category and species).")

crops = {"Cereals": ["Rice(Paddy)", "Wheat", "Maize", "Millets", "Barley"],
         "Pulses": ["Lentil(Masur)", "Chickpea(Gram)", "Mung Bean", "Urad(Maskalai)", "Pigeon Pea"],
         "Oilseeds": ["Mustard", "Groundnut", "Sesame", "Linseed"],
         "Fibre crops": ["Jute", "Cotton", "Hemp"],
         "Vegetables": ["Potato", "Tomato", "Brinjal", "Bitter Gourd", "Bottle Gourd", "Radish", "Carrot",
                        "Cauliflower", "Onion", "Cucumber", "Beans", "Cabbage"],
         "Fruits": ["Apple", "Banana", "Guava", "Mango", "Litchi", "Papaya"],
         "Plantation spice": ["Tea", "Sugarcane", "Ginger"],
         "Turmeric": ["Cardamom", "Cinchona"]}

# Crop details section
st.header("1. Select your crop")

category = st.selectbox("Crop category", list(crops.keys()))
crop = st.multiselect("Crop", crops[category])

#Crop compatibility check
Incompatible_pairs = [({"Tomato","Potato"}, "Both share late blight disease and compete heavily for nightshade nutrients."),
                      ({"Onion", "Beans"}, "Onions release biochemicals that stunt N2 fixing bacteria in bean roots"),
                      ({"Tomato", "Cabbage"}, "Cabbage stunts tomato growth and competes for heavy Nitrogen"),
                      ({"Maize", "Tomato"}, "Competition for sunlight and growing space")]
def analyze_crop_compatibility(crop):
    selected_set = set(crop)
    warnings_found = []
    for pair, reason in Incompatible_pairs:
        if pair.issubset(selected_set):
            warnings_found.append((pair, reason))
    if warnings_found:
        st.warning("Crop compatibility issues found!")
        st.write("Transplant/Transfer recommended. ", selected_set, "should not be grown together")
        for pair, reason in warnings_found:
            crop_names = "+".join(sorted(pair))
            st.error(f"{crop_names}")
            st.write(reason)
    else:
        st.success("No known conflict was found in selected crops. "
                   "This does not guarantee crop compatibility.")

st.header("2.Crop compatibility results")
if st.button("Analyze compatibility"):
    analyze_crop_compatibility(crop)

#Soil pH Compatibility check