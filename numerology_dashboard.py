import streamlit as st
from collections import Counter
import datetime

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

def growth_tracker(dob):
    today = datetime.datetime.today()
    try:
        birth = datetime.datetime.strptime(dob, "%d%m%Y")
        age = today.year - birth.year
        personal_year = (sum(map(int, str(today.year))) + sum(map(int, dob))) % 9 or 9
        return age, personal_year
    except:
        return None, None

# ------------------ OUTPUT ------------------
if submitted:
    if len(dob) == 8 and name:
        digits = extract_digits(dob, name)
        grid = generate_lusho_grid(digits)
        missing = [num for num, val in grid.items() if val == 0]

        st.subheader("📊 Lusho Grid")
        st.write(grid)

        st.subheader("❌ Missing Numbers")
        st.write(missing)

        st.subheader("🧘 Lal Kitab Remedies")
        st.write(lal_kitab_remedies(missing))

        st.subheader("💼 Career Suggestions")
        st.write(career_suggestions(grid))

        st.subheader("❤️ Compatibility Checker")
        if partner_name:
            score = compatibility_score(name, partner_name)
            st.write(f"Compatibility Score with {partner_name}: {score}/9")
        else:
            st.info("Enter partner's name to check compatibility.")

        st.subheader("📈 Personal Growth Tracker")
        age, personal_year = growth_tracker(dob)
        if age:
            st.write(f"Age: {age} years")
            st.write(f"Current Personal Year: {personal_year}")
        else:
            st.error("Invalid DOB format. Please use DDMMYYYY.")
    else:
        st.warning("Please enter valid DOB (DDMMYYYY) and Name before analyzing.")
        if age:
            st.write(f"Age: {age} years")
            st.write(f"Current Personal Year: {personal_year}")
        else:
            st.error("Invalid DOB format. Please use DDMMYYYY.")
    else:
        st.warning("Please enter valid DOB (DDMMYYYY) and Name before analyzing.")
