import streamlit as st
from datetime import datetime

# --- Core Numerology Functions ---
def name_to_number(name: str) -> int:
    mapping = {
        'A':1,'J':1,'S':1,
        'B':2,'K':2,'T':2,
        'C':3,'L':3,'U':3,
        'D':4,'M':4,'V':4,
        'E':5,'N':5,'W':5,
        'F':6,'O':6,'X':6,
        'G':7,'P':7,'Y':7,
        'H':8,'Q':8,'Z':8,
        'I':9,'R':9
    }
    total = sum(mapping.get(ch.upper(), 0) for ch in name if ch.isalpha())
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

def dob_to_life_path(dob_str: str) -> int:
    y, m, d = map(int, dob_str.split('/'))
    digits = list(str(y) + str(m) + str(d))
    total = sum(int(dig) for dig in digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

# --- Lal Kitab Remedies (sample; expand as needed) ---
lal_kitab_remedies = {
    1: "Offer water to the rising Sun daily 🌞",
    2: "Keep a silver coin in your wallet for harmony 🪙",
    3: "Donate yellow items on Thursdays 🌼",
    4: "Avoid black clothing on Saturdays ⚫",
    5: "Feed birds daily 🐦",
    6: "Offer sweets to young girls on Fridays 🍬",
    7: "Keep a piece of coconut in your room 🥥",
    8: "Donate black sesame seeds on Saturdays ⚫",
    9: "Help the needy without expectation 🤝"
}

# --- Name Pools ---
girl_names = ["Anaya", "Ira", "Siya", "Aanya", "Myra", "Pari", "Diya", "Kiara", "Riya", "Aarohi"]
boy_names  = ["Aarav", "Vihaan", "Vivaan", "Reyansh", "Advik", "Devansh", "Arjun", "Kabir", "Atharv", "Yuvraj"]

def suggest_names_by_gender(life_path: int, gender: str):
    if gender == "Girl":
        pool = girl_names
    elif gender == "Boy":
        pool = boy_names
    else:
        pool = girl_names + boy_names
    return [n for n in pool if name_to_number(n) == life_path]

# --- Streamlit App ---
st.title("🔢 Numerology Pro – Full Report Mode")

full_name = st.text_input("Enter Full Name")
dob = st.text_input("Enter Date of Birth (YYYY/MM/DD)")

gender = st.radio("👶 Select Baby Gender", ["Girl", "Boy", "Any"], index=0)

if st.button("Generate Full Report"):
    if full_name and dob:
        life_path = dob_to_life_path(dob)
        name_num = name_to_number(full_name)

        st.subheader("📜 Numerology Report")
        st.write(f"**Name Number:** {name_num}")
        st.write(f"**Life Path Number:** {life_path}")

        # Lal Kitab Remedy
        remedy = lal_kitab_remedies.get(life_path, "No remedy found — update your remedy list.")
        st.markdown(f"### 🔮 Lal Kitab Remedy for Life Path {life_path}:")
        st.info(remedy)

        # Baby Names
        st.markdown(f"### 👶 Lucky Baby Names (Life Path {life_path}):")
        suggestions = suggest_names_by_gender(life_path, gender)
        if suggestions:
            selected_name = st.selectbox("Select from suggestions", suggestions)
            st.success(f"Selected: {selected_name} → {name_to_number(selected_name)}")
        else:
            st.warning("No matching names found — try changing gender or expanding name pool.")

        # Compatibility Checker
        if st.checkbox("🔍 Check Existing Name Compatibility"):
            existing_name = st.text_input("Enter existing name to check:")
            if existing_name:
                st.info(f"Name {existing_name} has number {name_to_number(existing_name)}")

        # Name Correction
        if st.checkbox("✏️ Suggest Name Correction"):
            desired_num = st.number_input("Enter desired name number", 1, 9, value=life_path)
            st.write("Try modifying letters to match target number:", desired_num)

        # IST Timestamp
        st.caption(f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST")
    else:
        st.error("Please fill in both name and DOB fields.")
        months.append((month_num, year_for_month, meanings.get(pm,"—")))
    return months

# --- UI ---
st.set_page_config(page_title="Numerology Pro – Full Report", page_icon="🔮", layout="wide")
st.title("🔮 Numerology Pro – Full Report Mode")

col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name (for checking)")
with col2:
    dob = st.date_input(
        "Date of Birth",
        value=date(2024, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

life_path = digit_sum(sum(int(d) for d in dob.strftime("%d%m%Y")))
report_content = [f"## 🧬 Life Path: {life_path}"]

# Baby Names
if st.checkbox("👶 Suggest Lucky Baby Names"):
    lucky = suggest_names(life_path)
    sec = [f"### 🎯 Lucky Baby Names (Life Path {life_path}):"]
    sec.extend([f"- {n} → {name_to_number(n)}" for n in lucky])
    report_content.extend(sec)
    st.markdown("\n".join(sec))

# Existing Name
if st.checkbox("📝 Check Existing Name Compatibility"):
    if full_name:
        name_num = name_to_number(full_name)
        result = f"**{full_name} → {name_num}**"
        if name_num == life_path:
            result += " ✅ Perfectly compatible"
        elif abs(name_num - life_path) in [1,2]:
            result += " ⚖️ Moderately compatible"
        else:
            result += " ❌ Not compatible"
        report_content.append(result)
        st.markdown(result)
        rems = lal_kitab_remedies(dob, life_path, name_num)
        report_content.append("**Lal Kitab Remedies:**")
        report_content.extend([f"- {r}" for r in rems])
        for r in rems:
            st.write(f"- {r}")

# Naam Sudhaar
if st.checkbox("✏️ Suggest Name Correction"):
    if full_name:
        sugg = naam_sudhaar(full_name, life_path)
        if sugg:
            sec = ["### ✨ Harmonized Name Suggestions:"]
            sec.extend([f"- {s} → {life_path}" for s in sugg])
            report_content.extend(sec)
            st.markdown("\n".join(sec))

# Lal Kitab Remedies (DOB)
if st.checkbox("🧿 Show Lal Kitab Remedies (DOB Based)"):
    dob_rems = lal_kitab_remedies(dob, life_path)
    sec = ["### **Lal Kitab Remedies:**"]
    sec.extend([f"- {r}" for r in dob_rems])
    report_content.extend(sec)
    for r in dob_rems:
        st.write(f"- {r}")

# Yearly & Monthly Predictions
if st.checkbox("📅 Show Yearly & Monthly Predictions"):
    year, p_year = yearly_cycle(life_path)
    sec = [f"### 📆 Personal Year {year}: {p_year}"]
    months = monthly_cycles(p_year)
    sec.append("#### 🗓 Monthly Predictions:")
    for mnum, ynum, meaning in months:
        sec.append(f"- {mnum}/{ynum}: {meaning}")
    report_content.extend(sec)
    st.markdown("\n".join(sec))

# Report Mode
if st.checkbox("📄 Show Session Report"):
    st.subheader("📜 Session Report")
    st.markdown("\n".join(report_content))
    st.info("Copy this report into Word/Google Docs for PDF or print output.")
