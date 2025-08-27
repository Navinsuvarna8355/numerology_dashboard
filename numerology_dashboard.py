import streamlit as st
import pandas as pd
from datetime import date

# --- Config ---
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

# --- UI ---
st.title("🔢 Missing Number Remedies & Growth Tracker")

# Optional compatibility toggle
compat_enabled = st.checkbox("Enable Compatibility Module (Optional)", value=False)

# View selector
view = st.radio("Select View", ["Daily", "Monthly"])
today = date.today().strftime("%Y-%m-%d")

# Remedy logger
st.subheader("🧘 Remedy Practice Log")
remedy_logs = []

for num, remedy in missing_numbers.items():
    practiced = st.checkbox(f"{traits[num]} ({num}): {remedy}", key=f"remedy_{num}")
    remedy_logs.append({
        "date": today,
        "number": num,
        "trait": traits[num],
        "remedy": remedy,
        "status": "Practiced" if practiced else "Missed"
    })

# Convert to DataFrame for audit
df_log = pd.DataFrame(remedy_logs)

# Display tracker
st.subheader(f"📈 {view} Growth Tracker")
for entry in remedy_logs:
    status_icon = "✅" if entry["status"] == "Practiced" else "❌"
    st.write(f"{entry['trait']} ({entry['number']}): {status_icon}")

# Optional: show full log
with st.expander("📜 View Audit Log"):
    st.dataframe(df_log)

# Optional compatibility logic
if compat_enabled:
    st.subheader("💞 Compatibility Checker")
    partner_dob = st.text_input("Enter Partner's DOB (DD-MM-YYYY)")
    st.write("🔒 Compatibility logic goes here (toggleable, respects privacy)")
