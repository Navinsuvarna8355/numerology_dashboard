import streamlit as st
from datetime import datetime, timedelta, date
import uuid

# ----------------------------
# App config
# ----------------------------
st.set_page_config(page_title="Numerology Pro – Full Report Mode", page_icon="🔮", layout="wide")

# ----------------------------
# Time helpers (IST without extra deps)
# ----------------------------
def ist_now():
    """Returns the current time in IST."""
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

def ist_now_str(fmt="%Y-%m-%d %H:%M:%S IST"):
    """Returns the current IST time as a formatted string."""
    return ist_now().strftime(fmt)

# ----------------------------
# Core numerology utilities
# ----------------------------
def digit_sum(n: int) -> int:
    """
    Calculates the single-digit sum of a number,
    retaining master numbers (11, 22, 33).
    """
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

PYTHAG_MAP = {
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

def name_to_number(name: str) -> int:
    """Calculates the numerological root of a name."""
    total = sum(PYTHAG_MAP.get(ch.upper(), 0) for ch in name if ch.isalpha())
    return digit_sum(total)

def life_path_from_date(d: date) -> int:
    """Calculates the life path number from a date of birth."""
    digits = f"{d.year}{d.month}{d.day}"
    total = sum(int(x) for x in digits)
    return digit_sum(total)

# ----------------------------
# Lo Shu grid (from DOB)
# ----------------------------
def loshu_missing_numbers_from_date(d: date) -> list[int]:
    """Finds the missing numbers in the Lo Shu grid for a given DOB."""
    digits = [int(ch) for ch in f"{d.day}{d.month}{d.year}"]
    present = set(digits)
    return [n for n in range(1, 10) if n not in present]

def name_contains_any_missing_digit(name: str, missing_nums: list[int]) -> bool:
    """Checks if a name's numerological digits contain any missing Lo Shu numbers."""
    nums_in_name = {PYTHAG_MAP.get(ch.upper(), 0) for ch in name if ch.isalpha()}
    return any(n in nums_in_name for n in missing_nums)

# ----------------------------
# Extended Lal Kitab remedies (1–33)
# ----------------------------
REMEDIES_1_33 = {
    1: ["🌞 Offer water to the rising Sun daily", "Take decisive, ethical actions"],
    2: ["🪙 Keep a silver coin in wallet", "Prioritize rest and hydration"],
    3: ["🌼 Donate yellow on Thursdays", "Teach or learn on a schedule"],
    4: ["🧹 Declutter weekly", "Avoid all-black on Saturdays"],
    5: ["🐦 Feed birds daily", "Practice breathwork or walks"],
    6: ["🍬 Offer sweets on Fridays", "Nurture harmony at home"],
    7: ["🥥 Keep a clean coconut; replace monthly", "Reflect and study with purpose"],
    8: ["⚖️ Donate black sesame on Saturdays", "Audit money weekly; be fair"],
    9: ["🤝 Serve without expectation", "Channel energy via disciplined fitness"],
    10: ["Lead small projects with humility", "Let results speak"],
    11: ["Nightly meditation", "Support a mentor/community"],
    12: ["Turn sacrifice into learning", "Avoid victim mindset"],
    13: ["Declutter + ship small improvements", "Respect structure/rules"],
    14: ["Moderate habits/spend/speech", "Avoid shortcuts"],
    15: ["Beautify a corner weekly", "Balance care with boundaries"],
    16: ["Daily gratitude", "Avoid ego battles and risky speculation"],
    17: ["Blend ambition with charity", "Track and celebrate ethical wins"],
    18: ["Serve the vulnerable", "Set healthy help boundaries"],
    19: ["Cultivate self-reliance", "Share credit generously"],
    20: ["Protect sleep", "Let timing mature; review calmly"],
    21: ["Co-create in teams", "Avoid dramatization; focus outcomes"],
    22: ["Plan community-impact project", "Ground vision with weekly ops"],
    23: ["Travel with purpose", "Verify information; write daily"],
    24: ["Dependable care routine", "Balance giving with self-respect"],
    25: ["Research then act", "Spiritual study with logic"],
    26: ["Lead ethically; mentor", "Transparent money practices"],
    27: ["Teach or volunteer weekly", "Empathy + disciplined study"],
    28: ["Pilot ventures with discipline", "Invite contrarian feedback"],
    29: ["Practice emotional boundaries", "Set deadlines for decisions"],
    30: ["Express then refine", "Teach what you learn"],
    31: ["Design lasting systems", "Protect focus and timelines"],
    32: ["Influence responsibly", "Choose long-term plays"],
    33: ["Guide compassionately", "Daily compassion; protect energy"],
}

def get_remedies(number: int) -> list[str]:
    """Retrieves remedies for a given number."""
    if number in REMEDIES_1_33:
        return REMEDIES_1_33[number]
    base = digit_sum(number)
    return REMEDIES_1_33.get(base, ["Act ethically, reflect daily, serve consistently."])

# ----------------------------
# Name pools and dual-filter
# ----------------------------
GIRL_NAMES = ["Anaya", "Ira", "Siya", "Aanya", "Myra", "Pari", "Diya", "Kiara", "Riya", "Aarohi"]
BOY_NAMES  = ["Aarav", "Vihaan", "Vivaan", "Reyansh", "Advik", "Devansh", "Arjun", "Kabir", "Atharv", "Yuvraj"]

FAVOURABLE_ROOTS = {1, 3, 5, 6}

def dual_filter_names(pool: list[str], missing_nums: list[int]) -> list[dict]:
    """
    Keeps names whose root is in {1,3,5,6} and which include at least one missing Lo Shu digit vibration.
    Returns list of dicts: {name, root, patched: bool}
    """
    out = []
    for nm in pool:
        root = name_to_number(nm)
        patched = name_contains_any_missing_digit(nm, missing_nums)
        if root in FAVOURABLE_ROOTS and patched:
            out.append({"name": nm, "root": root, "patched": patched})
    return out

def get_baby_name_pool(gender: str) -> list[str]:
    """Selects the correct name pool based on gender."""
    if gender == "Girl":
        return GIRL_NAMES
    if gender == "Boy":
        return BOY_NAMES
    return GIRL_NAMES + BOY_NAMES

# ----------------------------
# Naam Sudhaar (1-letter prefix/suffix to match Life Path)
# ----------------------------
def naam_sudhaar(name: str, target: int, max_suggestions: int = 20) -> list[str]:
    """Generates name suggestions by adding a single letter to match a target number."""
    suggestions = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seen = set()
    for ch in letters:
        cand1 = name + ch
        cand2 = ch + name
        for cand in (cand1, cand2):
            if cand not in seen and name_to_number(cand) == target:
                suggestions.append(cand)
                seen.add(cand)
            if len(suggestions) >= max_suggestions:
                return suggestions
    return suggestions

# ----------------------------
# Personal year and monthly themes
# ----------------------------
MONTH_MEANINGS = {
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

def personal_year(life_path: int, year: int) -> int:
    """Calculates the personal year number."""
    return digit_sum(life_path + digit_sum(year))

def personal_months(py: int, start_month: int, start_year: int) -> list[tuple]:
    """Calculates personal month numbers and themes for the next 12 months."""
    months = []
    for i in range(12):
        m = (start_month + i - 1) % 12 + 1
        y = start_year if m >= start_month else start_year + 1
        pm = digit_sum(py + m)
        months.append((m, y, pm, MONTH_MEANINGS.get(pm, "—")))
    return months

def get_compatibility_score(lp: int, other_num: int) -> int:
    """Calculates a simple compatibility score based on numerology alignment."""
    return max(0, 100 - 10 * abs(lp - other_num))

# ----------------------------
# HTML report generator
# ----------------------------
def generate_report_html(ctx: dict) -> str:
    """Generates a full HTML report from a context dictionary."""
    remedy_items = "".join(f"<li>{r}</li>" for r in ctx.get("remedies", []))
    missing_str = ", ".join(str(x) for x in ctx.get("missing_nums", [])) if ctx.get("missing_nums") else "None"

    baby_block = ""
    if ctx.get("baby_names"):
        items = "".join(
            f"<li>{bn['name']} → {bn['root']} "
            f"{' (patch ✔)' if bn['patched'] else ''}</li>"
            for bn in ctx["baby_names"]
        )
        baby_block = f"""
        <div class="report-section">
            <h2>Lucky baby names</h2>
            <p class="muted">Names with a favorable root (1, 3, 5, or 6) that also contain a missing Lo Shu digit.</p>
            <ul>{items}</ul>
        </div>
        """

    sudhaar_block = ""
    if ctx.get("sudhaar"):
        s_items = "".join(f"<li>{s} → {ctx['life_path']}</li>" for s in ctx["sudhaar"])
        sudhaar_block = f"""
        <div class="report-section">
            <h2>Harmonized name suggestions</h2>
            <p class="muted">Suggestions to align your name's numerological root with your Life Path number.</p>
            <ul>{s_items}</ul>
        </div>
        """

    months_block = ""
    if ctx.get("months"):
        m_items = "".join(f"<li>{m:02d}/{y}: {mean} (PM {pm})</li>" for (m, y, pm, mean) in ctx["months"])
        months_block = f"""
        <div class="report-section">
            <h2>Personal year and monthly themes</h2>
            <p class="muted">Year: {ctx['year']} • Personal Year: {ctx['pyear']}</p>
            <p>Understand the energetic theme of each month to plan accordingly.</p>
            <ul>{m_items}</ul>
        </div>
        """
    
    compat_block = ""
    if ctx.get("compat"):
        c_items = "".join(f"<li>{n} → {num} (score: {score}%)</li>" for n, num, score in ctx["compat"])
        compat_block = f"""
        <div class="report-section">
            <h2>Name checks & compatibility</h2>
            <p class="muted">A simple compatibility score based on alignment with your Life Path.</p>
            <ul>{c_items}</ul>
        </div>
        """

    html = f"""
    <!doctype html>
    <html><head>
    <meta charset="utf-8"/>
    <title>Numerology Report</title>
    <style>
        body {{ font-family: -apple-system, Segoe UI, Roboto, Arial; color:#111; margin:20px; font-size: 14px; line-height: 1.6; }}
        h1 {{ font-size: 24px; margin: 0 0 8px; }}
        h2 {{ font-size: 18px; margin: 18px 0 8px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
        .header {{ border-bottom:1px solid #e5e5e5; padding-bottom:8px; margin-bottom:14px; }}
        .meta {{ color:#555; font-size: 12px; }}
        .grid {{ display:flex; gap:12px; flex-wrap:wrap; }}
        .card {{ border:1px solid #eee; border-radius:8px; padding:10px 12px; background-color: #f9f9f9; }}
        ul {{ margin: 6px 0 12px 20px; }}
        li {{ margin-bottom: 4px; }}
        .footer {{ border-top:1px solid #e5e5e5; margin-top:18px; padding-top:6px; font-size:12px; color:#555; text-align: center; }}
        .pagebreak {{ page-break-before: always; }}
        .muted {{ color:#777; font-style: italic; font-size: 12px; }}
        .report-section {{ margin-bottom: 24px; }}
    </style>
    </head>
    <body>
        <div class="header">
        <h1>Numerology Report for {ctx.get('client_name', 'Client')}</h1>
        <div class="meta">{ctx.get('brand')} • Generated: {ctx.get('timestamp')} • Session: {ctx.get('session_id')}</div>
        </div>

        <div class="grid">
        <div class="card">
            <div><b>DOB:</b> {ctx.get('dob_str', '—')}</div>
            <div><b>Life Path:</b> {ctx.get('life_path', '—')}</div>
            <div><b>Name Number:</b> {ctx.get('name_num', '—')}</div>
            <div><b>Lo Shu missing:</b> {missing_str}</div>
        </div>
        </div>

        <div class="report-section">
            <h2>Lal Kitab aligned remedies</h2>
            <p class="muted">Personalized guidance based on your numerological profile.</p>
            <ul>{remedy_items}</ul>
        </div>

        {baby_block}
        {sudhaar_block}
        {compat_block}
        
        <div class="pagebreak"></div>
        {months_block}

        <div class="footer">Confidential • © {ctx.get('brand')}</div>
    </body></html>
    """
    return html

# ----------------------------
# UI
# ----------------------------
st.title("🔮 Numerology Pro – Full Report Mode")

col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name (for checking)")
with col2:
    dob = st.date_input("Date of Birth", value=date(1990,1,1), min_value=date(1900,1,1))

gender = st.radio("👶 Baby gender (for suggestions)", ["Girl", "Boy", "Any"], index=0)

if st.button("Generate Full Report", use_container_width=True):
    if not full_name:
        st.error("Please enter a full name.")
    else:
        try:
            # Core numbers
            lp = life_path_from_date(dob)
            nn = name_to_number(full_name)
            missing = loshu_missing_numbers_from_date(dob)
            sess_id = uuid.uuid4().hex[:8].upper()
            now_str = ist_now_str()
            
            # Additional report data
            baby_names_pool = get_baby_name_pool(gender)
            baby_suggestions = dual_filter_names(baby_names_pool, missing)
            name_corrections = naam_sudhaar(full_name, lp, max_suggestions=20)
            
            # Personal year and months
            current_year = ist_now().year
            py = personal_year(lp, current_year)
            months_data = personal_months(py, start_month=ist_now().month, start_year=current_year)

            # Context for HTML report
            ctx = {
                "brand": "Numerology Pro",
                "client_name": full_name,
                "dob_str": dob.strftime("%Y/%m/%d"),
                "life_path": lp,
                "name_num": nn,
                "missing_nums": missing,
                "remedies": get_remedies(lp),
                "baby_names": baby_suggestions,
                "sudhaar": name_corrections,
                "year": current_year,
                "pyear": py,
                "months": months_data,
                "session_id": sess_id,
                "timestamp": now_str,
                "compat": [] # To be filled in later if checkbox is used
            }

            st.subheader("📜 Report Summary")
            st.write(f"**Life Path:** {lp} | **Name Number:** {nn} | **Lo Shu missing digits:** {', '.join(map(str, missing)) if missing else 'None'}")
            st.caption(f"Session: {sess_id} • {now_str}")
            st.markdown("---")

            st.markdown("### 🔍 Check compatibility")
            other = st.text_input("Enter a name to check compatibility with", key="compat_name")
            if other:
                other_num = name_to_number(other)
                score = get_compatibility_score(lp, other_num)
                st.info(f"**{other}** → **{other_num}** | Compatibility score vs Life Path: **{score}%**")
                ctx["compat"].append((other, other_num, score))

            # Generate HTML report
            st.markdown("---")
            st.subheader("📄 Export & Preview")
            html_report = generate_report_html(ctx)
            st.download_button(
                "Download print-ready HTML",
                data=html_report.encode("utf-8"),
                file_name=f"{full_name.replace(' ','_')}_numerology_report.html",
                mime="text/html",
                use_container_width=True
            )
            st.markdown("Preview of the generated report:")
            st.components.v1.html(html_report, height=600, scrolling=True)

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}. Please check the input and try again.")def get_remedies(number: int) -> list[str]:
    if number in REMEDIES_1_33:
        return REMEDIES_1_33[number]
    base = digit_sum(number)
    return REMEDIES_1_33.get(base, ["Act ethically, reflect daily, serve consistently."])

# ----------------------------
# Name pools and dual-filter
# ----------------------------
GIRL_NAMES = ["Anaya", "Ira", "Siya", "Aanya", "Myra", "Pari", "Diya", "Kiara", "Riya", "Aarohi"]
BOY_NAMES  = ["Aarav", "Vihaan", "Vivaan", "Reyansh", "Advik", "Devansh", "Arjun", "Kabir", "Atharv", "Yuvraj"]

FAVOURABLE_ROOTS = {1, 3, 5, 6}

def dual_filter_names(pool: list[str], missing_nums: list[int]):
    """
    Keep names whose root in {1,3,5,6} and which include at least one missing Lo Shu digit vibration.
    Returns list of dicts: {name, root, patched: bool}
    """
    out = []
    for nm in pool:
        root = name_to_number(nm)
        patched = name_contains_any_missing_digit(nm, missing_nums)
        if root in FAVOURABLE_ROOTS and patched:
            out.append({"name": nm, "root": root, "patched": patched})
    return out

# ----------------------------
# Naam Sudhaar (1-letter prefix/suffix to match Life Path)
# ----------------------------
def naam_sudhaar(name: str, target: int, max_suggestions: int = 20):
    suggestions = []
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seen = set()
    for ch in letters:
        cand1 = name + ch
        cand2 = ch + name
        for cand in (cand1, cand2):
            if cand not in seen and name_to_number(cand) == target:
                suggestions.append(cand)
                seen.add(cand)
            if len(suggestions) >= max_suggestions:
                return suggestions
    return suggestions

# ----------------------------
# Personal year and monthly themes
# ----------------------------
MONTH_MEANINGS = {
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

def personal_year(life_path: int, year: int) -> int:
    return digit_sum(life_path + digit_sum(year))

def personal_months(py: int, start_month: int, start_year: int):
    months = []
    for i in range(12):
        m = (start_month + i - 1) % 12 + 1
        y = start_year if m >= start_month else start_year + 1
        pm = digit_sum(py + m)
        months.append((m, y, pm, MONTH_MEANINGS.get(pm, "—")))
    return months

# ----------------------------
# HTML report generator
# ----------------------------
def generate_report_html(ctx: dict) -> str:
    # ctx: {brand, client_name, dob_str, life_path, name_num, missing_nums, remedies,
    #       baby_names(list of dicts), compat (list of tuples), sudhaar(list),
    #       year, pyear, months(list), session_id, timestamp}
    remedy_items = "".join(f"<li>{r}</li>" for r in ctx["remedies"])
    missing_str = ", ".join(str(x) for x in ctx["missing_nums"]) if ctx["missing_nums"] else "None"

    baby_block = ""
    if ctx.get("baby_names"):
        items = "".join(
            f"<li>{bn['name']} → {bn['root']} "
            f"{' (patch ✔)' if bn['patched'] else ''}</li>"
            for bn in ctx["baby_names"]
        )
        baby_block = f"<h2>Lucky baby names</h2><ul>{items}</ul>"

    compat_block = ""
    if ctx.get("compat"):
        c_items = "".join(f"<li>{n} → {num} (score: {score}%)</li>" for n, num, score in ctx["compat"])
        compat_block = f"<h2>Name checks</h2><ul>{c_items}</ul>"

    sudhaar_block = ""
    if ctx.get("sudhaar"):
        s_items = "".join(f"<li>{s} → {ctx['life_path']}</li>" for s in ctx["sudhaar"])
        sudhaar_block = f"<h2>Harmonized name suggestions</h2><ul>{s_items}</ul>"

    months_block = ""
    if ctx.get("months"):
        m_items = "".join(f"<li>{m:02d}/{y}: {mean} (PM {pm})</li>" for (m, y, pm, mean) in ctx["months"])
        months_block = f"""
        <h2>Personal year and monthly themes</h2>
        <p>Year: {ctx['year']} • Personal Year: {ctx['pyear']}</p>
        <ul>{m_items}</ul>
        """

    html = f"""
    <!doctype html>
    <html><head>
    <meta charset="utf-8"/>
    <title>Numerology Report</title>
    <style>
      body {{ font-family: -apple-system, Segoe UI, Roboto, Arial; color:#111; margin:20px; }}
      h1 {{ font-size: 22px; margin: 0 0 8px; }}
      h2 {{ font-size: 18px; margin: 18px 0 8px; }}
      .header {{ border-bottom:1px solid #e5e5e5; padding-bottom:8px; margin-bottom:14px; }}
      .meta {{ color:#555; font-size: 12px; }}
      .grid {{ display:flex; gap:12px; flex-wrap:wrap; }}
      .card {{ border:1px solid #eee; border-radius:8px; padding:10px 12px; }}
      ul {{ margin: 6px 0 12px 20px; }}
      .footer {{ border-top:1px solid #e5e5e5; margin-top:18px; padding-top:6px; font-size:12px; color:#555; }}
      .pagebreak {{ page-break-before: always; }}
      .muted {{ color:#777; }}
    </style>
    </head>
    <body>
      <div class="header">
        <div class="meta">{ctx['brand']} • Generated: {ctx['timestamp']} • Session: {ctx['session_id']}</div>
      </div>
      <h1>{ctx['client_name']}</h1>
      <div class="grid">
        <div class="card">
          <div><b>DOB:</b> {ctx['dob_str']}</div>
          <div><b>Life Path:</b> {ctx['life_path']}</div>
          <div><b>Name Number:</b> {ctx['name_num']}</div>
          <div><b>Lo Shu missing:</b> {missing_str}</div>
        </div>
      </div>

      <h2>Lal Kitab aligned remedies</h2>
      <ul>{remedy_items}</ul>

      {baby_block}
      {sudhaar_block}

      <div class="pagebreak"></div>

      {months_block}
      {compat_block}

      <div class="footer">Confidential • © {ctx['brand']}</div>
    </body></html>
    """
    return html

# ----------------------------
# UI
# ----------------------------
st.title("🔮 Numerology Pro – Full Report Mode")

col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name (for checking)")
with col2:
    dob = st.date_input("Date of Birth", value=date(1990,1,1), min_value=date(1900,1,1))

gender = st.radio("👶 Baby gender (for suggestions)", ["Girl", "Boy", "Any"], index=0)

if st.button("Generate Full Report", use_container_width=True):
    if not full_name or not dob:
        st.error("Please enter full name and DOB.")
    else:
        try:
            # Core numbers
            lp = life_path_from_date(dob)
            nn = name_to_number(full_name)
            missing = loshu_missing_numbers_from_date(dob)
            sess_id = uuid.uuid4().hex[:8].upper()
            now_str = ist_now_str()

            st.subheader("📜 Numerology Report")
            st.write(f"• Life Path: {lp}")
            st.write(f"• Name Number: {nn}")
            st.write(f"• Lo Shu missing digits: {missing if missing else 'None'}")
            st.caption(f"Session: {sess_id} • {now_str}")

            # Remedies
            st.markdown("### 🔮 Lal Kitab Remedies")
            for r in get_remedies(lp):
                st.write(f"- {r}")

            # Baby names (dual-filter)
            st.markdown("### 👶 Dual-filter lucky baby names")
            pool = GIRL_NAMES if gender == "Girl" else BOY_NAMES if gender == "Boy" else GIRL_NAMES + BOY_NAMES
            suggestions = dual_filter_names(pool, missing)
            if suggestions:
                st.dataframe(
                    [{"Name": s["name"], "Root": s["root"], "Missing patch": "Yes" if s["patched"] else "No"}
                     for s in suggestions],
                    use_container_width=True
                )
                sel = st.selectbox("Pick a suggested name", [s["name"] for s in suggestions])
                st.success(f"Selected: {sel} → {name_to_number(sel)}")
            else:
                st.info("No matches in current pool. Expand pool or review DOB.")

            # Name correction
            st.markdown("### ✏️ Harmonized name suggestions (1-letter tweak to match Life Path)")
            tuned = naam_sudhaar(full_name, lp, max_suggestions=20)
            if tuned:
                st.write(", ".join(tuned))
            else:
                st.write("No single-letter prefix/suffix match found.")

            # Compatibility (toggle)
            compat_records = []
            if st.checkbox("🔍 Check existing/partner name compatibility"):
                other = st.text_input("Enter name to check")
                if other:
                    other_num = name_to_number(other)
                    # Simple score vs Life Path alignment
                    score = max(0, 100 - 10*abs(lp - other_num))
                    st.info(f"{other} → {other_num} | Compatibility score vs Life Path: {score}%")
                    compat_records.append((other, other_num, score))

            # Predictions
            st.markdown("### 📅 Personal year and monthly themes")
            cy = ist_now().year
            py = personal_year(lp, cy)
            st.write(f"Personal Year {cy}: {py}")
            months = personal_months(py, start_month=ist_now().month, start_year=cy)
            for m, y, pm, meaning in months:
                st.write(f"- {m:02d}/{y}: {meaning} (PM {pm})")

            # Report export
            st.markdown("---")
            st.subheader("📄 Export report")
            ctx = {
                "brand": "Numerology Pro",
                "client_name": full_name,
                "dob_str": dob.strftime("%Y/%m/%d"),
                "life_path": lp,
                "name_num": nn,
                "missing_nums": missing,
                "remedies": get_remedies(lp),
                "baby_names": suggestions,
                "compat": compat_records,
                "sudhaar": tuned,
                "year": cy,
                "pyear": py,
                "months": months,
                "session_id": sess_id,
                "timestamp": now_str
            }
            html_report = generate_report_html(ctx)
            st.download_button(
                "Download print-ready HTML",
                data=html_report.encode("utf-8"),
                file_name=f"{full_name.replace(' ','_')}_numerology_report.html",
                mime="text/html",
                use_container_width=True
            )
            st.markdown("Preview:")
            st.components.v1.html(html_report, height=600, scrolling=True)

        except Exception as e:
            st.error(f"Error: {e}")
```
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
