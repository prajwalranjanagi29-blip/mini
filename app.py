import streamlit as st
import pandas as pd
from datetime import datetime
import os
from utils.ai_mood import get_mood_explanation
from utils.pdf_export import export_moods_to_pdf
from utils.speech_to_text import transcribe_audio_file

CSV_FILE = "mood_logs.csv"

st.set_page_config(page_title="AI Mood Tracker", layout="centered")

# --- Login ---
st.sidebar.title("🔑 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    if username == "admin" and password == "admin123":
        st.session_state["logged_in"] = True
    else:
        st.sidebar.error("Invalid credentials")

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to continue.")
    st.stop()

# --- Load / create CSV ---
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "mood"])
    df.to_csv(CSV_FILE, index=False)

# --- Header ---
st.markdown("""
<h1 style='text-align:center;'>AI Mood Tracker</h1>
<p style='text-align:center;'>Log your moods with emoji, AI insights, voice input, and PDF reports.</p>
<hr>
""", unsafe_allow_html=True)

# --- Mood Input ---
st.subheader("📝 Add Mood")

# Emoji selector
emoji_dict = {
    "😊 Happy": "Happy",
    "😢 Sad": "Sad",
    "😡 Angry": "Angry",
    "😱 Anxious": "Anxious",
    "😴 Tired": "Tired",
    "😌 Relaxed": "Relaxed"
}
emoji_choice = st.selectbox("Select your mood emoji:", list(emoji_dict.keys()))
mood_text = emoji_dict[emoji_choice]

# Optional voice input
audio_file = st.file_uploader("Or upload a voice recording (wav/mp3)", type=["wav","mp3"])
if audio_file:
    mood_text = transcribe_audio_file(audio_file)
    st.info(f"Transcribed voice: {mood_text}")

# Save mood
if st.button("Save Mood"):
    new_row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "mood": mood_text}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("Mood saved successfully!")

    # AI Mood Explanation
    explanation = get_mood_explanation(mood_text)
    st.subheader("🤖 AI Mood Insight")
    st.write(explanation)

# --- View / Export ---
st.subheader("📚 Mood History")
st.dataframe(df[::-1], use_container_width=True)

if st.button("📄 Download PDF Report"):
    pdf_file = export_moods_to_pdf(CSV_FILE, "mood_report.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", data=f, file_name="mood_report.pdf")

# --- Clear Data ---
if st.button("❌ Clear All Data"):
    df = pd.DataFrame(columns=["timestamp", "mood"])
    df.to_csv(CSV_FILE, index=False)
    st.warning("All mood logs cleared!")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Developed with ❤️ using Streamlit</p>", unsafe_allow_html=True)
