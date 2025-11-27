import streamlit as st
import pandas as pd
from datetime import datetime
import os
from utils.ai_mood import get_ai_mood_analysis
from utils.pdf_export import export_moods_to_pdf
from utils.speech_to_text import transcribe_audio_file

USERS_FILE = "users.csv"
LOG_FILE = "mood_logs.csv"

st.set_page_config(page_title="AI Mood Tracker", layout="centered")

# Initialize CSV files if they don't exist
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username","password"]).to_csv(USERS_FILE, index=False)
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["username","timestamp","mood","ai_analysis"]).to_csv(LOG_FILE, index=False)

# --- Session state for login ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# --- Sidebar: Login / Signup ---
st.sidebar.title("🔑 Login / Signup")
action = st.sidebar.selectbox("Choose action:", ["Login", "Signup"])
username_input = st.sidebar.text_input("Username")
password_input = st.sidebar.text_input("Password", type="password")

if st.sidebar.button(action):
    users_df = pd.read_csv(USERS_FILE)
    if action == "Signup":
        if username_input in users_df["username"].values:
            st.sidebar.error("Username already exists.")
        elif username_input.strip() == "" or password_input.strip() == "":
            st.sidebar.error("Username and password required.")
        else:
            users_df = pd.concat([users_df, pd.DataFrame([{"username": username_input, "password": password_input}])], ignore_index=True)
            users_df.to_csv(USERS_FILE, index=False)
            st.sidebar.success("Signup successful! Please login.")
    else:  # Login
        if ((users_df["username"] == username_input) & (users_df["password"] == password_input)).any():
            st.session_state["logged_in"] = True
            st.session_state["username"] = username_input
            st.sidebar.success(f"Logged in as {username_input}")
        else:
            st.sidebar.error("Invalid credentials.")

# Block access if not logged in
if not st.session_state["logged_in"]:
    st.warning("Please login or signup to continue.")
    st.stop()

# --- App Header ---
st.markdown("<h1 style='text-align:center;'>AI Mood Tracker</h1><hr>", unsafe_allow_html=True)
st.subheader("📝 Describe your mood")
st.write("Write a paragraph describing your feelings. AI will provide insights and suggestions.")

# --- Mood Input ---
mood_text = st.text_area("Your mood text:", height=200)

# Optional voice input
audio_file = st.file_uploader("Or upload a voice recording (wav/mp3)", type=["wav","mp3"])
if audio_file:
    mood_text = transcribe_audio_file(audio_file)
    st.info(f"Transcribed voice: {mood_text}")

# --- Analyze & Save Mood ---
if st.button("Analyze & Save"):
    if mood_text.strip() == "":
        st.error("Please enter your mood text.")
    else:
        ai_result = get_ai_mood_analysis(mood_text)
        new_row = {
            "username": st.session_state["username"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood_text,
            "ai_analysis": ai_result
        }
        logs_df = pd.read_csv(LOG_FILE)
        logs_df = pd.concat([logs_df, pd.DataFrame([new_row])], ignore_index=True)
        logs_df.to_csv(LOG_FILE, index=False)
        st.success("Mood saved successfully!")
        st.subheader("🤖 AI Analysis")
        st.write(ai_result)

# --- Display Mood History ---
st.subheader("📚 Your Mood History")
logs_df = pd.read_csv(LOG_FILE)
user_logs = logs_df[logs_df["username"] == st.session_state["username"]]
if len(user_logs) > 0:
    st.dataframe(user_logs[::-1], use_container_width=True)
else:
    st.info("No moods logged yet.")

# --- PDF Export ---
if st.button("📄 Download PDF Report"):
    pdf_file = export_moods_to_pdf(LOG_FILE, f"{st.session_state['username']}_mood_report.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", data=f, file_name=f"{st.session_state['username']}_mood_report.pdf")

# --- Clear User Data ---
if st.button("❌ Clear My Mood Data"):
    logs_df = logs_df[logs_df["username"] != st.session_state["username"]]
    logs_df.to_csv(LOG_FILE, index=False)
    st.warning("Your mood logs have been cleared.")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Developed with ❤️ using Streamlit & OpenAI</p>", unsafe_allow_html=True)
