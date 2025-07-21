import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ✅ Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Streamlit UI config
st.set_page_config(page_title="🍳 ChefBuddy - by Alizah", page_icon="🍰", layout="centered")

# ✅ Custom styling
st.markdown("""
    <style>
        .main {
            background-color: #fff8f0;
            padding: 2rem;
            border-radius: 20px;
        }
        .stButton > button {
            background-color: #ff6f61;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Branding
st.title("🍳 ChefBuddy")
st.markdown("### by Alizah 💖")
st.markdown("Upload a food image **or** enter ingredients to get tasty, healthy recipe suggestions from ChefBuddy AI.")

# ✅ Inputs
user_name = st.text_input("👤 What's your name?", placeholder="e.g., Alizah")
uploaded_file = st.file_uploader("📸 Upload Food Image", type=["jpg", "jpeg", "png"])
ingredients = st.text_area("📝 Or type your ingredients (comma-separated)", placeholder="e.g., eggs, tomatoes, onion")
cuisine = st.selectbox("🌍 Choose preferred cuisine (optional)", ["Any", "Italian", "Pakistani", "Chinese", "Indian", "Mediterranean"])
calories = st.slider("🔥 Max Calories (Optional)", min_value=100, max_value=1000, step=50, value=500)

# ✅ Recipe generation
if uploaded_file or ingredients.strip():
    with st.spinner("👨\u200d🍳 ChefBuddy is thinking..."):
        prompt = f"""
        You're ChefBuddy, a friendly and creative AI chef helping {user_name or "a food lover"}.

        Analyze the following and generate:
        - Two creative recipe ideas
        - Cuisine type: {cuisine if cuisine != 'Any' else 'Surprise me'}
        - Max Calories per recipe: {calories}
        - Clear step-by-step cooking instructions
        - Estimated preparation time
        - Healthy substitutions
        - A fun cooking tip

        Ingredients: {ingredients if ingredients else "Image input only"}
        """

        try:
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="📷 Uploaded Image", use_container_width=True)
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)

            st.success("🍽️ ChefBuddy suggests:")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"⚠️ Gemini Error: {e}")

# ✅ Custom Footer
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: #888; font-size: 14px;'>
        Made with ❤️ by <strong>Alizah</strong> · Powered by Gemini AI · 🍽️ Stay hungry, stay curious!
    </div>
""", unsafe_allow_html=True)
