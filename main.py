import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="🍳 ChefBuddy - by Alizah",
    page_icon="🍰",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
        body, .main {
            background-color: #121212;
            color: #ffffff;
        }
        .stApp {
            background-color: #121212;
        }
        h2, h3, h4, h5, h6, p, div {
            color: white !important;
        }
        .stButton > button {
            background-color: #ff6f61;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stTextInput>div>div>input, 
        .stTextArea>div>textarea,
        .stSelectbox>div>div>div>div {
            background-color: #1e1e1e;
            color: white;
            border-radius: 10px;
            border: 1px solid #444;
        }
    </style>
""", unsafe_allow_html=True)

# --- Branding ---
st.markdown("""
    <h2 style='text-align: center; color: #ff914d;'>🍳 ChefBuddy</h2>
    <p style='text-align: center; font-size: 13px; color: #ccc; margin-top: -10px;'>by <strong>Alizah</strong></p>
""", unsafe_allow_html=True)

st.markdown("Upload a food image **or** enter ingredients to get tasty, healthy recipe suggestions from ChefBuddy AI.")

# --- Inputs ---
user_name = st.text_input("👤 Your Name", placeholder="e.g., Alizah")
uploaded_file = st.file_uploader("📸 Upload Food Image", type=["jpg", "jpeg", "png"])
ingredients = st.text_area("📝 Ingredients (comma-separated)", placeholder="e.g., eggs, tomatoes, onion")
cuisine = st.selectbox("🌍 Preferred Cuisine (optional)", ["Any", "Italian", "Pakistani", "Chinese", "Indian", "Mediterranean"])
calories = st.slider("🔥 Max Calories (optional)", min_value=100, max_value=1000, step=50, value=500)

# --- AI Suggestion Logic ---
if uploaded_file or ingredients.strip():
    with st.spinner("👨‍🍳 ChefBuddy is thinking..."):
        prompt = f"""
        You're ChefBuddy, a helpful and friendly AI chef assisting {user_name or "a food lover"}.

        Task:
        - Suggest 2 unique and delicious recipes
        - Cuisine: {cuisine if cuisine != 'Any' else 'Surprise me'}
        - Max calories per recipe: {calories}
        - Step-by-step cooking instructions
        - Prep time and cook time
        - Healthy substitutions if any
        - Fun cooking tip

        Ingredients: {ingredients if ingredients else "Based on image only"}
        """

        try:
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="📷 Uploaded Food Image", use_container_width=True)
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)

            st.success("🍽️ ChefBuddy suggests:")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"⚠️ Gemini Error: {e}")

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem; border-color: #333;">
    <div style='text-align: center; color: #aaa; font-size: 13px;'>
        Made with ❤️ by <strong>Alizah</strong> · Powered by Gemini AI · 🍴 Cook smart, eat well!
    </div>
""", unsafe_allow_html=True)
