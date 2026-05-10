import streamlit as st
from google import genai
import datetime

# Setup client with provided API key
API_KEY = "AIzaSyCSElHmYeDKEh0EF-msGmwsIN5eW35UISE"
client = genai.Client(api_key=API_KEY)

# Configure the Streamlit page
st.set_page_config(page_title="Astrology Chatbot", page_icon="✨")

st.title("✨ Cosmic Guide: Your Astrology Chatbot")
st.markdown("Ask me anything about your zodiac sign, horoscopes, or astrological charts!")

# Sidebar for personal details
with st.sidebar:
    st.header("🌌 Your Cosmic Blueprint")
    st.markdown("Enter your details for personalized readings:")
    user_name = st.text_input("Name", placeholder="E.g., Luna")
    birth_date = st.date_input(
        "Date of Birth", 
        value=None, 
        min_value=datetime.date(1900, 1, 1), 
        max_value=datetime.date.today()
    )
    birth_time = st.time_input("Time of Birth", value=None)
    birth_location = st.text_input("Place of Birth", placeholder="City, Country")
    zodiac_sign = st.selectbox(
        "Sun Sign (Optional)", 
        ["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    )

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your astrological question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare conversation history for the model
    # We construct a simple text prompt that includes the persona and the history
    system_prompt = "You are a mystical, wise, and knowledgeable astrologer. Answer the user's questions about astrology, zodiac signs, horoscopes, and cosmic events. Keep your tone mystical but helpful.\n"
    
    # Add personal details to the system prompt if they are provided
    user_context = []
    if user_name: user_context.append(f"Name: {user_name}")
    if birth_date: user_context.append(f"Date of Birth: {birth_date.strftime('%B %d, %Y')}")
    if birth_time: user_context.append(f"Time of Birth: {birth_time.strftime('%I:%M %p')}")
    if birth_location: user_context.append(f"Place of Birth: {birth_location}")
    if zodiac_sign: user_context.append(f"Sun Sign: {zodiac_sign}")
    
    if user_context:
        system_prompt += "\nThe user has provided the following personal details:\n"
        system_prompt += "\n".join(user_context)
        system_prompt += "\n\nUse these details to deeply personalize your astrological insights when answering their questions.\n\n"
    else:
        system_prompt += "\n\n"

    conversation_text = system_prompt
    for msg in st.session_state.messages:
        role_name = "User" if msg["role"] == "user" else "Astrologer"
        conversation_text += f"{role_name}: {msg['content']}\n"
    
    conversation_text += "Astrologer: "

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Generate response using the google-genai SDK
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=conversation_text
            )
            response_text = response.text
            message_placeholder.markdown(response_text)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Failed to communicate with the spirits: {e}")
