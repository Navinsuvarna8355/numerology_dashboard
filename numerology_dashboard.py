import streamlit as st
from datetime import datetime
import uuid

# ----------------------------
# CORE NUMEROLOGY UTILITIES
# ----------------------------
def digit_sum(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def name_to_number(name: str):
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
    return digit_sum(total)

def dob_to_life_path(dob_str: str):
    y, m, d = map(int, dob_str.split('/'))
    digits = list(str(y) + str(m) + str(d))
    total = sum(int(x) for x in digits)
    return digit_sum(total)

# ----------------------------
# LO SHU MISSING NUMBER LOGIC
# ----------------------------
def loshu_missing_numbers(dob_str: str):
    y, m, d = map(int, dob_str.split('/'))
    digits = [int(ch) for ch in f"{d}{m}{y}" if ch.isdigit()]
    present = set(digits)
    return [n for n in range(1, 10) if n not in present]

def name_contains_missing_digits(name: str, missing_nums: list):
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
    name_nums = {mapping.get(ch.upper(), 0) for ch in name if ch.isalpha()}
    return any(num in name_nums for num in missing_nums)

# ----------------------------
# EXTENDED LAL KITAB REMEDIES (1–33)
# ----------------------------
remedies_1_33 = {
    1: "🌞 Offer water to the rising Sun daily",
    2: "🪙 Keep a silver coin in your wallet",
    3: "🌼 Donate yellow on Thursdays",
    4: "⚫ Avoid black on Saturdays",
    5: "🐦 Feed birds daily",
    6: "🍬 Offer sweets to young girls on Fridays",
    7: "🥥 Keep a coconut in your room",
    8: "⚖️ Donate black sesame on Saturdays",
    9: "🤝 Help the needy without expectation",
    10: "Lead small projects with humility",
    11: "Meditate nightly; channel intuition",
    12: "Turn sacrifices into learning",
    13: "Declutter weekly; respect structure",
    14: "Moderation in habits and speech",
    15: "Nurture harmony at home",
    16: "Practice gratitude; avoid ego battles",
    17: "Combine ambition with charity",
    18: "Serve consistently without burnout",
    19: "Build self‑reliance; share credit",
    20: "Protect rest; act with patience",
    21: "Express creatively in teams",
    22: "Plan a community‑impact project",
    23: "Travel with purpose; verify info",
    24: "Balance care with self‑respect",
    25: "Research deeply before acting",
    26: "Lead ethically; mentor others",
    27: "Teach or volunteer weekly",
    28: "Start ventures with discipline",
    29: "Use emotional intelligence; decide firmly",
    30: "Express, then refine",
    31: "Design long‑lasting systems",
    32: "Influence responsibly; think long‑term",
    33: "Guide compassionately; protect your energy"
}

def get_remedy(num):
    return remedies_1_33.get(num, remedies_1_33.get(digit_sum(num), "No remedy found"))

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
