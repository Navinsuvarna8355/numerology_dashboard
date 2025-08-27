import streamlit as st
from datetime import date, datetime

# --- Letter Map (Chaldean) ---
letter_map = {
    'A':1,'I':1,'J':1,'Q':1,'Y':1,
    'B':2,'K':2,'R':2,
    'C':3,'G':3,'L':3,'S':3,
    'D':4,'M':4,'T':4,
    'E':5,'H':5,'N':5,'X':5,
    'U':6,'V':6,'W':6,
    'O':7,'Z':7,
    'F':8,'P':8
}

# --- Utilities ---
def digit_sum(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def name_to_number(name):
    return digit_sum(sum(letter_map.get(ch.upper(), 0) for ch in name if ch.isalpha()))

def get_missing_numbers(dob):
    all_nums = set(str(i) for i in range(1, 10))
    dob_digits = set(d for d in dob.strftime("%d%m%Y"))
    return sorted(list(all_nums - dob_digits))

def lal_kitab_remedies(dob, life_path, name_num=None):
    remedies = []
    life_path_map = {
        1: "🌞 Offer water to the rising Sun daily",
        2: "🌙 Keep a silver coin in your wallet",
        3: "📿 Wear yellow on Thursdays",
        4: "🪔 Light mustard oil lamp under a peepal tree on Saturdays",
        5: "🪙 Donate green vegetables on Wednesdays",
        6: "🎁 Donate white clothes on Fridays",
        7: "📚 Read spiritual texts daily",
        8: "⚖️ Feed black dogs on Saturdays",
        9: "🍎 Donate red fruits on Tuesdays"
    }
    remedies.append(life_path_map.get(life_path, ""))
    missing_map = {
        '1': "🪔 Keep a copper coin in your pocket",
        '2': "🌿 Plant tulsi at home",
        '3': "📿 Chant ‘Om Namah Shivaya’ 108 times",
        '4': "💡 Keep a small piece of silver with you",
        '5': "🚶 Visit a holy place once a year",
        '6': "🥛 Donate milk on Mondays",
        '7': "📚 Meditate 15 mins daily",
        '8': "⚖️ Feed black dogs or crows on Saturdays",
        '9': "🍎 Donate red lentils or fruits on Tuesdays"
    }
    for m in get_missing_numbers(dob):
        remedies.append(missing_map[m])
    if name_num and name_num != life_path:
        remedies.append("🔮 Wear a copper bracelet for 43 days")
        remedies.append("🌿 Keep basil plant at home")
    return [r for r in remedies if r]

def suggest_names(life_path):
    sample_names = ["Aarav", "Vihaan", "Anaya", "Ira", "Vivaan", "Siya", "Reyansh", "Aanya", "Advik", "Myra", "Devansh", "Pari"]
    return [n for n in sample_names if name_to_number(n) == life_path]

def naam_sudhaar(name, life_path):
    alphabet = list(letter_map.keys())
    suggestions = []
    for letter in alphabet:
        if name_to_number(name + letter) == life_path:
            suggestions.append(name + letter)
        if name_to_number(letter + name) == life_path:
            suggestions.append(letter + name)
    return sorted(set(suggestions))

def yearly_cycle(life_path):
    current_year = datetime.now().year
    return current_year, digit_sum(life_path + digit_sum(current_year))

def monthly_cycles(personal_year):
    current_month = datetime.now().month
    current_year = datetime.now().year
    months = []
    meanings = {
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
    for i in range(12):
        month_num = (current_month + i - 1) % 12 + 1
        year_for_month = current_year if month_num >= current_month else current_year + 1
        pm = digit_sum(personal_year + month_num)
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
