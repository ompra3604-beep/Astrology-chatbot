"""
Astrology Chatbot using Streamlit + Google Gemini API
"""

import streamlit as st
from google import genai

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Astrology Chatbot",
    page_icon="🔮",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #12001f, #2b1055);
    color: white;
}

.title {
    text-align: center;
    color: gold;
    font-size: 42px;
    font-weight: bold;
    text-shadow: 0px 0px 12px gold;
}

.subtitle {
    text-align: center;
    color: #d9b3ff;
    margin-bottom: 20px;
}

.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

hr {
    border: 1px solid #5a3d8a;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI CONFIG ---------------- #

# Store API key in Streamlit Secrets:
# .streamlit/secrets.toml
#
# GEMINI_API_KEY = "your_api_key"
# API_KEY = st.secrets["GEMINI_API_KEY"]
API_KEY = "AIzaSyBEAJ_adW7EAPHOz_fdIskMQDpOZgEyI6c"
# from google import genai
API_KEY = "YOUR_API_KEY"
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SYSTEM PROMPT ---------------- #

SYSTEM_PROMPT = """
You are a professional Astrology Expert AI.

You specialize in:
- Zodiac signs
- Daily horoscope
- Birth charts
- Compatibility readings
- Planetary influence
- Numerology basics

Your tone should be:
- Warm
- Mystical
- Positive
- Helpful
- Conversational

If needed, ask users for:
- Birth date
- Birth time
- Birth place

Always give practical and uplifting guidance.
"""

# ---------------- RESPONSE FUNCTION ---------------- #

def get_astrology_response(user_input):

    try:

        prompt = f"""
        {SYSTEM_PROMPT}

        User Question:
        {user_input}

        Astrology Response:
        """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        # return response.text
        return response.candidates[0].content.parts[0].text

    except Exception as e:
        return f"""
🔮 The cosmic energies are disturbed...

Error:
{str(e)}

Please try again later.
"""

# ---------------- UI HEADER ---------------- #

st.markdown('<div class="title">🔮 Astrology Chatbot 🔮</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Your Personal Cosmic Guide ✨</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- CHAT HISTORY ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ---------------- #

user_prompt = st.chat_input(
    "Ask about zodiac signs, horoscope, love compatibility..."
)

if user_prompt:

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("🔮 Reading the stars..."):

            bot_response = get_astrology_response(user_prompt)

            st.markdown(bot_response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("✨ Astrology Menu")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.subheader("🌟 Features")

    st.markdown("""
    ✅ Daily Horoscope  
    ✅ Zodiac Readings  
    ✅ Love Compatibility  
    ✅ Birth Chart Guidance  
    ✅ Planetary Insights  
    """)

    st.markdown("---")

    st.subheader("💫 Quick Questions")

    quick_questions = [
        "What does Mercury retrograde mean?",
        "Tell me about Leo personality",
        "Best zodiac compatibility for Virgo",
        "Today's horoscope for Aries"
    ]

    for q in quick_questions:
        if st.button(q):
            st.session_state.messages.append(
                {"role": "user", "content": q}
            )

            response = get_astrology_response(q)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

            st.rerun()