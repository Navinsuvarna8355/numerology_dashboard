import streamlit as st
from datetime import datetime
from collections import Counter

# --- CONFIG ---
st.set_page_config(page_title="Lusho Grid Dashboard", layout="centered")

# --- FUNCTIONS ---
def extract_digits(dob):
    return [d for d in dob.strftime("%d%m%Y")]

def generate_lusho_grid(digits):
    counts = Counter(digits)
    grid = {str(i): counts.get(str(i), 0) for i in range(1, 10)}
    return grid

def display_lusho_chart(grid, title="Your Lusho Grid"):
    st.markdown(f"### 🔢 {title}")
    layout = [
        [("4", "Mind"), ("9", "Mind"), ("2", "Mind")],
        [("3", "Soul"), ("5", "Soul"), ("7", "Soul")],
        [("8", "Practical"), ("1", "Practical"), ("6", "Practical")]
    ]
    for row in layout:
        row_display = []
        for i, (num, plane) in enumerate(row):
            count = grid[num]
            color = "#FFA500" if i % 2 == 0 else "#FFFFFF"
            cell = f"""
            <div style='background-color:{color}; padding:10px; text-align:center; border:1px solid #ccc; width:80px'>
                <b>{num}</b><br>{'✔️' if count > 0 else '❌'}<br><small>{plane}</small>
            </div>
            """
            row_display.append(cell)
        st.markdown(f"<div style='display:flex; gap:5px'>{''.join(row_display)}</div>", unsafe_allow_html=True)

def display_missing_remedies(grid):
    st.markdown("### 🧘 Missing Number Remedies")
    missing = [num for num, count in grid.items() if count == 0]
    if not missing:
        st.success("No missing numbers! You're balanced across all planes.")
    else:
        for num in missing:
            st.warning(f"Number {num} is missing. Suggested remedy: {lal_kitab_remedy(num)}")

def lal_kitab_remedy(num):
    remedies = {
        "1": "Offer water to rising sun daily.",
        "2": "Keep a silver coin with you.",
        "3": "Chant Saraswati mantra daily.",
        "4": "Avoid wearing grey; use green.",
        "5": "Donate green vegetables on Wednesdays.",
        "6": "Feed cows or donate white sweets.",
        "7": "Meditate daily and avoid alcohol.",
        "8": "Help elderly or donate black sesame.",
        "9": "Practice forgiveness and donate red cloth."
    }
    return remedies.get(num, "No remedy found.")

def display_growth_tracker(grid, period="Daily"):
    st.markdown(f"### 📈 {period} Growth Tracker")
    for num, count in grid.items():
        status = "✅ Practiced" if count > 0 else "❌ Missed"
        st.text(f"Trait {num}: {status}")

def display_compatibility(user_grid, partner_grid):
    st.markdown("### ❤️ Compatibility Insights")
    shared = [num for num in user_grid if user_grid[num] > 0 and partner_grid[num] > 0]
    conflict = [num for num in user_grid if user_grid[num] == 0 and partner_grid[num] > 0]
    st.info(f"Shared strengths: {', '.join(shared) if shared else 'None'}")
    st.error(f"Conflicting traits: {', '.join(conflict) if conflict else 'None'}")

# --- MAIN UI ---
st.title("🔮 Lusho Grid Dashboard")

dob = st.date_input("Enter your Date of Birth", value=datetime(1990, 1, 1))
digits = extract_digits(dob)
user_grid = generate_lusho_grid(digits)

display_lusho_chart(user_grid)
display_missing_remedies(user_grid)

# Daily/Monthly toggle
period = st.radio("Select View", ["Daily", "Monthly"])
display_growth_tracker(user_grid, period)

# Optional Partner Compatibility
enable_partner = st.checkbox("Enable Partner Compatibility")
if enable_partner:
    partner_dob = st.date_input("Partner's Date of Birth", value=datetime(1990, 1, 1), key="partner_dob")
    partner_digits = extract_digits(partner_dob)
    partner_grid = generate_lusho_grid(partner_digits)
    display_lusho_chart(partner_grid, title="Partner's Lusho Grid")
    display_compatibility(user_grid, partner_grid)
