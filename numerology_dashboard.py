import streamlit as st
from datetime import date, datetime

# Title
st.title("🔢 Numerology Dashboard")

# Date of Birth Input (with backdate support)
user_dob = st.date_input(
    "📅 Your Date of Birth",
    value=date(1990, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today()
)

# IST Timestamp Logging
ist_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
st.write(f"🕒 Logged at (IST): {ist_now}")

# Lusho Grid Placeholder
def generate_lusho_grid(dob):
    digits = [int(d) for d in dob.strftime("%d%m%Y") if d.isdigit()]
    grid = {str(i): digits.count(i) for i in range(1, 10)}
    return grid

# Display Lusho Grid
grid = generate_lusho_grid(user_dob)
st.subheader("🔲 Lusho Grid")
for num in range(1, 10):
    st.write(f"{num}: {'●' * grid[str(num)] if grid[str(num)] else '—'}")

# Lal Kitab Remedies (basic example)
def get_remedies(dob):
    year = dob.year
    if year % 9 == 0:
        return ["🪔 Wear copper on Tuesday", "🌿 Offer jaggery to monkeys"]
    elif year % 4 == 0:
        return ["🪙 Keep silver with you", "🧂 Avoid salty food on Thursdays"]
    else:
        return ["🧘 Practice meditation daily", "📿 Chant your root number mantra"]

# Display Remedies
st.subheader("🧿 Suggested Remedies")
for remedy in get_remedies(user_dob):
    st.write(f"- {remedy}")

# Optional Compatibility Checker
if st.checkbox("🔗 Enable Compatibility Checker (Optional)"):
    partner_dob = st.date_input(
        "Partner's Date of Birth",
        value=date(1990, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    def check_compatibility(dob1, dob2):
        sum1 = sum([int(d) for d in dob1.strftime("%d%m%Y")])
        sum2 = sum([int(d) for d in dob2.strftime("%d%m%Y")])
        return abs(sum1 - sum2) % 9

    compatibility_score = check_compatibility(user_dob, partner_dob)
    st.write(f"💞 Compatibility Score: {compatibility_score}/9")

# Daily/Monthly Logs (Placeholder)
st.subheader("📘 Logs")
st.write("✅ Daily and monthly remedy logs will be auto-generated and exportable in future versions.")

# Footer
st.caption("Built with clarity, control, and modularity by Navinn 🧠")
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
