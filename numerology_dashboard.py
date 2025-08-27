import streamlit as st
import pandas as pd
from datetime import datetime

# --- IST Timestamp ---
ist_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# --- Configurable Parameters ---
missing_numbers = {
    2: "Keep a silver coin with you",
    3: "Chant Saraswati mantra daily",
    4: "Avoid wearing grey; use green",
    5: "Donate green vegetables on Wednesdays",
    6: "Feed cows or donate white items",
    7: "Meditate daily and avoid alcohol",
    8: "Help elderly or donate black sesame"
}

traits = {
    2: "Empathy",
    3: "Creativity",
    4: "Discipline",
    5: "Adaptability",
    6: "Harmony",
    7: "Spirituality",
    8: "Responsibility"
}

# --- UI Header ---
st.title("🔢 Numerology Dashboard")
st.caption(f"🕒 IST Timestamp: {ist_now}")

# --- Optional Modules ---
compat_enabled = st.checkbox("🔒 Enable Compatibility Module", value=False)
remedy_log_enabled = st.checkbox("🧘 Enable Remedy Tracker", value=True)

# --- View Selector ---
view = st.radio("📅 Select View", ["Daily", "Monthly"])

# --- Remedy Tracker ---
if remedy_log_enabled:
    st.subheader("🧘 Remedy Practice Log")
    remedy_logs = []

    for num, remedy in missing_numbers.items():
        practiced = st.checkbox(f"{traits[num]} ({num}): {remedy}", key=f"remedy_{num}")
        remedy_logs.append({
            "timestamp": ist_now,
            "view": view,
            "number": num,
            "trait": traits[num],
            "remedy": remedy,
            "status": "Practiced" if practiced else "Missed"
        })

    # --- Fallback Logic ---
    if not remedy_logs:
        st.warning("⚠️ No remedies logged. Please check your config or enable tracking.")
    else:
        df_log = pd.DataFrame(remedy_logs)
        st.subheader(f"📈 {view} Growth Tracker")
        for entry in remedy_logs:
            icon = "✅" if entry["status"] == "Practiced" else "❌"
            st.write(f"{entry['trait']} ({entry['number']}): {icon}")

        with st.expander("📜 View Audit Log"):
            st.dataframe(df_log)

# --- Compatibility Module ---
if compat_enabled:
    st.subheader("💞 Compatibility Checker")
    partner_dob = st.text_input("Enter Partner's DOB (DD-MM-YYYY)")
    st.write("🔍 Compatibility logic placeholder — respects privacy and is toggleable.")
