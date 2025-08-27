import streamlit as st
from datetime import datetime
import pytz

# --- Config Toggles ---
compat_enabled = st.sidebar.checkbox("Enable Compatibility Checker", value=False)
log_enabled = st.sidebar.checkbox("Enable Daily/Monthly Logs", value=True)
lusho_enabled = st.sidebar.checkbox("Enable Lusho Grid & Remedies", value=True)

# --- IST Timestamp ---
def get_ist_timestamp():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

# --- Life Path Calculator ---
def calculate_life_path(dob):
    digits = [int(d) for d in dob.strftime("%d%m%Y")]
    total = sum(digits)
    while total > 9 and total not in [11, 22]:
        total = sum([int(d) for d in str(total)])
    return total

# --- Lusho Grid Generator ---
def generate_lusho_grid(dob):
    digits = [int(d) for d in dob.strftime("%d%m%Y")]
    grid = {str(i): digits.count(i) for i in range(1, 10)}
    return grid

# --- Lal Kitab Remedies ---
def suggest_remedies(grid):
    missing = [num for num, count in grid.items() if count == 0]
    remedies = {
        "1": "Offer water to rising sun daily.",
        "2": "Keep a silver coin with you.",
        "3": "Chant Saraswati mantra daily.",
        "4": "Avoid wearing grey; use green.",
        "5": "Donate green vegetables on Wednesdays.",
        "6": "Feed cows or donate white items.",
        "7": "Meditate daily and avoid alcohol.",
        "8": "Help elderly or donate black sesame.",
        "9": "Donate red clothes or lentils on Tuesdays."
    }
    return {num: remedies[num] for num in missing}

# --- Logger ---
def log_event(label, dob, life_path, grid=None):
    if log_enabled:
        timestamp = get_ist_timestamp()
        entry = f"{timestamp} | {label} | DOB: {dob.strftime('%d-%m-%Y')} | Life Path: {life_path}"
        if grid:
            entry += f" | Lusho Grid: {grid}"
        with open(f"{label}_log.txt", "a") as f:
            f.write(entry + "\n")
        st.text(f"📁 Logged: {entry}")

# --- Main App ---
st.title("🔮 Numerology Dashboard")

user_name = st.text_input("Your Name", placeholder="Optional")
user_dob = st.date_input("Your Date of Birth")

if user_dob:
    user_lp = calculate_life_path(user_dob)
    st.write(f"🧮 Your Life Path Number: {user_lp}")
    log_event("User", user_dob, user_lp)

    if lusho_enabled:
        st.subheader("🧱 Lusho Grid & Remedies")
        user_grid = generate_lusho_grid(user_dob)
        st.write("🔢 Your Lusho Grid:", user_grid)

        remedies = suggest_remedies(user_grid)
        if remedies:
            st.warning("⚠️ Missing Numbers Detected:")
            for num, remedy in remedies.items():
                st.write(f"🔹 {num}: {remedy}")
        else:
            st.success("✅ No missing numbers. Balanced grid.")

        log_event("User", user_dob, user_lp, user_grid)

# --- Compatibility Module ---
if compat_enabled:
    st.subheader("💞 Compatibility Checker")

    partner_name = st.text_input("Partner's Name", placeholder="Optional")
    partner_dob = st.date_input("Partner's DOB", key="partner_dob")

    if partner_dob:
        partner_lp = calculate_life_path(partner_dob)
        st.write(f"🧮 {partner_name or 'Partner'}'s Life Path Number: {partner_lp}")
        log_event("Partner", partner_dob, partner_lp)

        # Compatibility Logic
        diff = abs(user_lp - partner_lp)
        if diff in [0, 1, 2]:
            st.success("✅ High Compatibility: Strong resonance and shared growth potential.")
        elif diff in [3, 4]:
            st.info("⚖️ Moderate Compatibility: Complementary traits, may need conscious effort.")
        else:
            st.warning("❌ Low Compatibility: Divergent paths, requires deep understanding.")

        # Lusho Grid Comparison
        if lusho_enabled:
            partner_grid = generate_lusho_grid(partner_dob)
            st.write("🔢 Partner's Lusho Grid:", partner_grid)

            overlap = {num: (user_grid[num], partner_grid[num]) for num in user_grid}
            st.write("🔄 Grid Overlap (You vs Partner):", overlap)

            synergy = [num for num in overlap if overlap[num][0] > 0 and overlap[num][1] > 0]
            conflict = [num for num in overlap if overlap[num][0] == 0 or overlap[num][1] == 0]

            st.info(f"💫 Synergistic Numbers: {synergy}")
            st.warning(f"⚠️ Conflict Zones: {conflict}")

            log_event("Partner", partner_dob, partner_lp, partner_grid)

# --- Footer ---
st.caption("🕒 IST Timestamp: " + get_ist_timestamp())
