import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import uuid

# ===== Config =====
IST = pytz.timezone("Asia/Kolkata")

# ===== Functions =====
def calculate_personal_year(dob: datetime, target_date: datetime) -> int:
    """Return Personal Year number using DOB and target date."""
    birth_month = dob.month
    birth_day = dob.day
    year_sum = sum(int(d) for d in f"{birth_month}{birth_day}{target_date.year}")
    while year_sum > 9:
        year_sum = sum(int(d) for d in str(year_sum))
    return year_sum

def get_monthly_predictions(personal_year: int) -> pd.DataFrame:
    """Generate dummy monthly predictions (replace with your Lal Kitab + Lo Shu logic)."""
    data = []
    for month in range(1, 13):
        pred = f"Month {month}: Prediction for PY {personal_year}"
        remedy = f"Suggested upay for month {month}"
        data.append({"Month": month, "Prediction": pred, "Remedy": remedy})
    return pd.DataFrame(data)

def get_partner_compatibility(py1: int, py2: int) -> str:
    """Dummy partner compatibility logic (replace with your full numerology rules)."""
    score = abs(py1 - py2)
    if score == 0:
        return "Highly Compatible — Same Personal Year vibes!"
    elif score in [1, 2]:
        return "Generally Compatible — Minor adjustments needed."
    else:
        return "Challenging — Different cycles, extra effort needed."

def generate_report_html(name: str, py: int, df: pd.DataFrame,
                         compatibility: str, session_id: str, timestamp: str) -> str:
    """Return HTML string for print/PDF."""
    html = f"""
    <html>
    <head><meta charset="UTF-8"><title>Numerology Report</title></head>
    <body>
        <h2>Numerology Report for {name}</h2>
        <p><b>Personal Year:</b> {py}</p>
        <h3>Monthly Predictions & Remedies</h3>
        {df.to_html(index=False)}
    """
    if compatibility:
        html += f"<h3>Partner Compatibility</h3><p>{compatibility}</p>"
    html += f"""
        <hr>
        <small>Session ID: {session_id} | Generated at: {timestamp}</small>
    </body></html>
    """
    return html

# ===== Streamlit UI =====
st.title("🔢 Numerology Predictions Dashboard")

# --- User Input ---
name = st.text_input("🪪 Your Name")
dob_input = st.date_input("📅 Your Date of Birth")

# Partner compatibility toggle
include_partner = st.checkbox("Include Partner Compatibility Module")
partner_name = partner_dob = None
if include_partner:
    partner_name = st.text_input("Partner Name")
    partner_dob = st.date_input("Partner Date of Birth")

# --- Core Logic ---
today = datetime.now(IST)

if dob_input and name:
    personal_year = calculate_personal_year(dob_input, today)
    st.subheader(f"📅 Personal Year: {personal_year}")

    # Monthly Predictions
    df_pred = get_monthly_predictions(personal_year)
    st.markdown("### 📆 Monthly Predictions & Remedies")
    st.dataframe(df_pred, use_container_width=True)

    # Partner compatibility if toggled
    compatibility_result = ""
    if include_partner and partner_dob:
        partner_py = calculate_personal_year(partner_dob, today)
        compatibility_result = get_partner_compatibility(personal_year, partner_py)
        st.markdown("### ❤️ Partner Compatibility")
        st.info(f"{partner_name} → {compatibility_result}")

    # Footer with Audit Info
    session_id = uuid.uuid4().hex[:8].upper()
    timestamp_ist = today.strftime("%Y-%m-%d %H:%M:%S %Z")
    st.markdown("---")
    st.caption(f"**Session ID:** {session_id} | **Generated at:** {timestamp_ist}")

    # Print/PDF-ready Report
    if st.button("🖨️ Generate Print/PDF View"):
        html_report = generate_report_html(name, personal_year, df_pred,
                                           compatibility_result, session_id, timestamp_ist)
        st.markdown("### 📄 Report Preview")
        st.components.v1.html(html_report, height=500, scrolling=True)

else:
    st.warning("Please enter your name and Date of Birth to proceed.")

# ----------------------------
# BABY NAME POOLS
# ----------------------------
girl_names = ["Anaya", "Ira", "Siya", "Aanya", "Myra", "Pari", "Diya", "Kiara", "Riya", "Aarohi"]
boy_names  = ["Aarav", "Vihaan", "Vivaan", "Reyansh", "Advik", "Devansh", "Arjun", "Kabir", "Atharv", "Yuvraj"]

# ----------------------------
# DUAL FILTER NAME SUGGESTER
# ----------------------------
def suggest_names_dual_filter(pool: list, dob_str: str):
    lucky_roots = {1, 3, 5, 6}
    missing = loshu_missing_numbers(dob_str)
    results = []
    for nm in pool:
        root = name_to_number(nm)
        if root in lucky_roots and name_contains_missing_digits(nm, missing):
            results.append((nm, root))
    return results

# ----------------------------
# YEARLY & MONTHLY PREDICTIONS
# ----------------------------
month_meanings = {
    1:"New beginnings, initiatives",
    2:"Partnerships, patience",
    3:"Creativity, expression",
    4:"Hard work, stability",
    5:"Change, freedom",
    6:"Responsibility, harmony",
    7:"Reflection, learning",
    8:"Power, recognition",
    9:"Completion, service"
}

def yearly_cycle(life_path):
    cy = datetime.now().year
    return cy, digit_sum(life_path + digit_sum(cy))

def monthly_cycles(personal_year):
    now_month = datetime.now().month
    now_year = datetime.now().year
    result = []
    for i in range(12):
        m = (now_month + i - 1) % 12 + 1
        y = now_year if m >= now_month else now_year + 1
        pm = digit_sum(personal_year + m)
        result.append((m, y, month_meanings.get(pm, "—")))
    return result

# ----------------------------
# STREAMLIT APP
# ----------------------------
st.title("🔢 Numerology Pro – Full Report Mode")

full_name = st.text_input("Full Name")
dob = st.text_input("Date of Birth (YYYY/MM/DD)")
gender = st.radio("👶 Select Baby Gender", ["Girl", "Boy", "Any"], index=0)

if st.button("Generate Full Report"):
    if full_name and dob:
        try:
            life_path = dob_to_life_path(dob)
            name_num = name_to_number(full_name)
            missing_nums = loshu_missing_numbers(dob)
            session_id = uuid.uuid4().hex[:8]

            st.subheader("📜 Numerology Report")
            st.write(f"**Name Number:** {name_num}")
            st.write(f"**Life Path Number:** {life_path}")
            st.write(f"**Missing Numbers in Lo Shu Grid:** {missing_nums if missing_nums else 'None'}")
            st.write(f"**Session ID:** {session_id} | **IST Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Remedy
            st.markdown(f"### 🔮 Lal Kitab Remedy for {life_path}")
            st.info(get_remedy(life_path))

            # Baby Names
            st.markdown(f"### 👶 Dual‑Filter Lucky Baby Names:")
            name_pool = girl_names if gender == "Girl" else boy_names if gender == "Boy" else girl_names + boy_names
            dual_suggestions = suggest_names_dual_filter(name_pool, dob)
            if dual_suggestions:
                sel = st.selectbox("Select from dual‑filter suggestions", [f"{nm} → {rt}" for nm, rt in dual_suggestions])
                st.success(f"Selected: {sel}")
            else:
                st.warning("No matching names found.")

            # Compatibility
            compat_list = []
            if st.checkbox("🔍 Check Existing Name Compatibility"):
                other_name = st.text_input("Enter name to check:")
                if other_name:
                    other_num = name_to_number(other_name)
                    score = 100 - abs(name_num - other_num) * 10
                    compat_list.append((other_name, other_num, score))
                    st.info(f"{other_name} → {other_num} | Compatibility Score: {score}%")

            # Predictions
            year, personal_year = yearly_cycle(life_path)
            st.markdown(f"### 📅 Personal Year {            session_id = uuid.uuid4().hex[:8]

            st.subheader("📜 Numerology Report")
            st.write(f"**Name Number:** {name_num}")
            st.write(f"**Life Path Number:** {life_path}")
            st.write(f"**Missing Numbers in Lo Shu Grid:** {missing_nums if missing_nums else 'None'}")

            # Remedy
            st.markdown(f"### 🔮 Lal Kitab Remedy for {life_path}")
            st.info(get_remedy(life_path))

            # Baby Names
            st.markdown(f"### 👶 Dual‑Filter Lucky Baby Names:")
            name_pool = girl_names if gender == "Girl" else boy_names if gender == "Boy" else girl_names + boy_names
            dual_suggestions = suggest_names_dual_filter(name_pool, dob)
            if dual_suggestions:
                sel = st.selectbox("Select from dual‑filter suggestions", [f"{nm} → {rt}" for nm, rt in dual_suggestions])
                st.success(f"Selected: {sel}")
            else:
                st.warning("No matching names found.")

            # Compatibility
            compat_list = []
            if st.checkbox("🔍 Check Existing Name Compatibility"):
                other_name = st.text_input("Enter name to check:")
                if other_name:
                    other_num = name_to_number(other_name)
                    st.info(f"{other_name} → {other_num}")
                    compat_list.append((
