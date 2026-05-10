"""
Astrology Chatbot using Streamlit and Google Gemini API
"""
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Astrology Chatbot",
    page_icon="🔮",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    # Initialize Gemini client
    API_KEY = "AIzaSyCSElHmYeDKEh0EF-msGmwsIN5eW35UISE"
    st.session_state.client = genai.Client(api_key=API_KEY)
    st.session_state.model = "gemini-2.5-flash"

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #1a0a2e, #2d1b4e);
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .user-message {
        background: rgba(147, 112, 219, 0.3);
        border-left: 4px solid #9370DB;
    }
    .bot-message {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #FFD700;
    }
    .title {
        text-align: center;
        color: #FFD700;
        font-size: 2.5em;
        text-shadow: 0 0 10px #FFD700;
    }
    .subtitle {
        text-align: center;
        color: #DDA0DD;
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# Astrology system prompt
ASTROLOGY_PROMPT = """You are an expert Astrology Chatbot with deep knowledge of:
- Western Astrology (Zodiac signs, houses, aspects)
- Planetary positions and their meanings
- Birth chart interpretation
- Horoscope readings
- Zodiac sign characteristics
- Compatibility between signs

Provide insightful, accurate, and helpful astrology readings. Be warm and engaging while maintaining astrological accuracy.
When users ask about their zodiac sign or birth chart, ask for their birth date, time, and place if needed for detailed readings.
Always try to provide practical and positive guidance."""

def get_astrology_response(user_input):
    """Get response from Gemini API"""
    try:
        # Combine system prompt with user input
        full_prompt = f"{ASTROLOGY_PROMPT}\n\nUser: {user_input}\n\nAstrologer:"
        
        response = st.session_state.client.models.generate_content(
            model=st.session_state.model,
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"🔮 *The stars are currently obscured...* \n\nError: {str(e)}\n\nPlease try again later."

# Title
st.markdown('<p class="title">🔮 Astrology Chatbot 🔮</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Cosmic Guide to the Stars</p>', unsafe_allow_html=True)
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your zodiac sign, horoscope, or any astrology question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🔮 Consulting the stars..."):
            response = get_astrology_response(prompt)
            st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with quick actions
with st.sidebar:
    st.title("✨ Quick Actions")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🌟 About This Bot")
    st.markdown("""
    This astrology chatbot uses Google Gemini AI to provide:
    
    - Zodiac sign readings
    - Horoscope predictions
    - Birth chart insights
    - Compatibility analysis
    - Planetary guidance
    """)
    
    st.markdown("---")
    st.markdown("### 📅 Today's Horoscope")
    st.info("💫 Share your zodiac sign for a personalized daily reading!")
    