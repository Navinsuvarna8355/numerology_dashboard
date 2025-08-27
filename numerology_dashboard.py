import streamlit as st
from collections import Counter
import datetime
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Numerology Dashboard", layout="wide")
st.title("🔮 Numerology Dashboard")

# Manual Inputs
col1, col2 = st.columns(2)
with col1:
    dob = st.text_input("Enter DOB (DDMMYYYY)", max_chars=8)
with col2:
    name = st.text_input("Enter Full Name")

partner_name = st.text_input("Enter Partner's Name (for Compatibility Check)")
submitted = st.button("🔍 Analyze")

# ------------------ CORE FUNCTIONS ------------------
def extract_digits(dob, name):
    digits = list(dob)
    name_digits = [str(ord(char.lower()) - 96) for char in name if char.isalpha()]
    return digits + name_digits

def generate_lusho_grid(digits):
    count = Counter(digits)
    return {str(i): count.get(str(i), 0) for i in range(1, 10)}

def display_lusho_grid(grid):
    layout = [
        [grid['1'], grid['2'], grid['3']],
        [grid['4'], grid['5'], grid['6']],
        [grid['7'], grid['8'], grid['9']]
    ]
    st.markdown("### 🧮 Lusho Grid (3x3 Format)")
    for row in layout:
        st.write(f"| {' | '.join(str(val) if val > 0 else ' ' for val in row)} |")

def lal_kitab_remedies(missing):
    remedies = {
        '1': "Offer water to rising sun, wear copper.",
        '2': "Keep silver, avoid milk at night.",
        '3': "Feed birds, avoid yellow on Thursdays.",
        '4': "Donate mustard oil, avoid black on Saturdays.",
        '5': "Keep green items, avoid lies.",
        '6': "Donate curd, avoid luxury obsession.",
        '7': "Keep religious books, avoid alcohol.",
        '8': "Feed black dogs, avoid ego.",
        '9': "Donate red clothes, avoid aggression."
    }
    return {num: remedies[num] for num in missing}

def career_suggestions(grid):
    mapping = {
        '1': "Leadership, Politics, Entrepreneurship",
        '2': "Counseling, Diplomacy, Healing",
        '3': "Writing, Teaching, Performing Arts",
        '4': "Engineering, Law, Real Estate",
        '5': "Marketing, Travel, Sales",
        '6': "Design, Hospitality, Caregiving",
        '7': "Research, Spirituality, Psychology",
        '8': "Finance, Management, Strategy",
        '9': "Philanthropy, Public Service, Coaching"
    }
    return {num: mapping[num] for num, val in grid.items() if val >= 2}

def compatibility_score(name1, name2):
    def name_sum(name): return sum([ord(c.lower()) - 96 for c in name if c.isalpha()])
    total = name_sum(name1) + name_sum(name2)
    return total % 9 or 9

def compare_grids(grid1, grid2):
    shared = [num for num in grid1 if grid1[num] > 0 and grid2[num] > 0]
    user_only = [num for num in grid1 if grid1[num] > 0 and grid2[num] == 0]
    partner_only = [num for num in grid2 if grid2[num] > 0 and grid1[num] == 0]
    return shared, user_only, partner_only

def growth_tracker(dob):
    today = datetime.datetime.today()
    try:
        birth = datetime.datetime.strptime(dob, "%d%m%Y")
        age = today.year - birth.year
        personal_year = (sum(map(int, str(today.year))) + sum(map(int, dob))) % 9 or 9
        return age, personal_year
    except:
        return None, None

def generate_log(name, dob, grid, missing, remedies, career, age, personal_year, score=None, partner=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = {
        "Timestamp": timestamp,
        "Name": name,
        "DOB": dob,
        "Age": age,
        "Personal Year": personal_year,
        "Lusho Grid": grid,
        "Missing Numbers": missing,
        "Remedies": remedies,
        "Career Suggestions": career,
    }
    if partner:
        log["Partner Name"] = partner
        log["Compatibility Score"] = score
    return pd.DataFrame([log])

# ------------------ OUTPUT ------------------
if submitted:
    if len(dob) == 8 and name:
        digits = extract_digits(dob, name)
        grid = generate_lusho_grid(digits)
        missing = [num for num, val in grid.items() if val == 0]
        remedies = lal_kitab_remedies(missing)
        career = career_suggestions(grid)
        age, personal_year = growth_tracker(dob)

        st.subheader("📊 Lusho Grid")
        display_lusho_grid(grid)

        st.subheader("❌ Missing Numbers")
        st.write(missing)

        st.subheader("🧘 Lal Kitab Remedies")
        st.write(remedies)

        st.subheader("📋 Remedy Habit Tracker")
        for num in missing:
            remedy = remedies[num]
            st.checkbox(f"{num}: {remedy}", key=f"remedy_{num}")

        st.subheader("💼 Career Suggestions")
        st.write(career)

        st.subheader("❤️ Compatibility Checker")
        if partner_name:
            score = compatibility_score(name, partner_name)
            st.write(f"Compatibility Score with {partner_name}: {score}/9")

            partner_digits = extract_digits(dob, partner_name)
            partner_grid = generate_lusho_grid(partner_digits)
            shared, user_only, partner_only = compare_grids(grid, partner_grid)

            st.markdown("### 🔗 Compatibility Grid Comparison")
            st.write(f"🔸 Shared Numbers: {shared}")
            st.write(f"🟦 Only in Your Grid: {user_only}")
            st.write(f"🟥 Only in Partner's Grid: {partner_only}")
        else:
            st.info("Enter partner's name to check compatibility.")

        st.subheader("📈 Personal Growth Tracker")
        if age:
            st.write(f"Age: {age} years")
            st.write(f"Current Personal Year: {personal_year}")
        else:
            st.error("Invalid DOB format. Please use DDMMYYYY.")

        st.subheader("📦 Exportable Log (Preview)")
        log_df = generate_log(name, dob, grid, missing, remedies, career, age, personal_year, score if partner_name else None, partner_name if partner_name else None)
        st.dataframe(log_df)
    else:
        st.warning("Please enter valid DOB (DDMMYYYY) and Name before analyzing.")
