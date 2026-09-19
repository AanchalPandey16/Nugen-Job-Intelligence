import html
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="Nugen Job Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Design tokens
#   ink      #0E1726   text / primary button
#   mist     #F2F4F8   page background
#   surface  #FFFFFF   panels
#   line     #E3E7EE   borders
#   match    #0E7C66   matched (deep green)
#   partial  #B7791F   partially matched (amber)
#   missing  #C2374F   missing (rose)
#   accent   #3D4FE0   brand / focus (indigo)
# Type: Sora (headlines, numbers)  +  DM Sans (interface, body)
# ---------------------------------------------------------------------------

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Sora:wght@500;600;700;800&display=swap');

:root {
    --ink: #0E1726;
    --ink-soft: #46536A;
    --ink-faint: #8792A6;
    --mist: #F2F4F8;
    --surface: #FFFFFF;
    --line: #E3E7EE;
    --accent: #3D4FE0;
    --accent-soft: #ECEEFF;
    --match: #0E7C66;
    --match-soft: #E3F4EF;
    --partial: #B7791F;
    --partial-soft: #FBF1DC;
    --missing: #C2374F;
    --missing-soft: #FBE8EC;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', system-ui, sans-serif;
}

.stApp {
    background:
        radial-gradient(1200px 500px at 85% -10%, #E4E8FF 0%, rgba(228,232,255,0) 60%),
        var(--mist);
    color: var(--ink);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.6rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header { visibility: hidden; }

/* ---------- Top bar ---------- */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 2px 26px 2px;
}
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 18px;
    letter-spacing: -0.3px;
    color: var(--ink);
}
.brand-mark {
    width: 34px; height: 34px;
    border-radius: 10px;
    background: var(--ink);
    display: grid; place-items: center;
}
.brand-mark svg { display: block; }
.status-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 7px 13px;
    border-radius: 999px;
    background: var(--surface);
    border: 1px solid var(--line);
    font-size: 12.5px; font-weight: 600; color: var(--ink-soft);
}
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--match); }

/* ---------- Hero ---------- */
.hero { padding: 6px 2px 30px 2px; max-width: 820px; }
.hero-title {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: clamp(30px, 4.6vw, 50px);
    line-height: 1.08;
    letter-spacing: -1.6px;
    color: var(--ink);
    margin: 0 0 16px 0;
}
.hero-sub {
    font-size: 17px;
    line-height: 1.6;
    color: var(--ink-soft);
    max-width: 640px;
    margin: 0;
}
.hero-steps {
    display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px;
}
.hero-step {
    display: inline-flex; align-items: center; gap: 9px;
    background: var(--surface);
    border: 1px solid var(--line);
    padding: 8px 14px 8px 8px;
    border-radius: 999px;
    font-size: 13px; font-weight: 600; color: var(--ink);
}
.hero-step b {
    width: 22px; height: 22px; border-radius: 50%;
    background: var(--accent-soft); color: var(--accent);
    display: grid; place-items: center;
    font-size: 11.5px; font-weight: 700;
}

/* ---------- Input panels ---------- */
.panel-head { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 8px; }
.panel-title { font-family: 'Sora', sans-serif; font-size: 15px; font-weight: 600; color: var(--ink); }
.panel-hint { font-size: 12.5px; color: var(--ink-faint); margin-bottom: 10px; }

div[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14.5px !important;
    line-height: 1.6 !important;
    padding: 16px 18px !important;
    box-shadow: 0 1px 2px rgba(14,23,38,0.04) !important;
    transition: border-color .15s ease, box-shadow .15s ease;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px rgba(61,79,224,0.14) !important;
}
div[data-testid="stTextArea"] textarea::placeholder { color: #A7B0C0 !important; }

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius: 14px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    transition: transform .15s ease, background .15s ease, border-color .15s ease;
}
.stButton > button[kind="primary"] {
    height: 54px;
    background: var(--ink);
    border: 1px solid var(--ink);
    color: #fff;
    font-size: 15.5px;
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"]:focus-visible,
.stButton > button[kind="secondary"]:focus-visible {
    outline: 3px solid rgba(61,79,224,0.35);
    outline-offset: 2px;
}
.stButton > button[kind="secondary"] {
    height: 40px;
    background: var(--surface);
    border: 1px solid var(--line);
    color: var(--ink-soft);
    font-size: 13.5px;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-soft);
}

/* ---------- Results ---------- */
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 22px; font-weight: 700; letter-spacing: -0.5px;
    color: var(--ink); margin: 40px 0 4px 0;
}
.section-sub { font-size: 14px; color: var(--ink-faint); margin-bottom: 18px; }

.score-card {
    background: var(--ink);
    color: #fff;
    border-radius: 24px;
    padding: 30px 32px;
    display: flex; align-items: center; gap: 32px; flex-wrap: wrap;
    box-shadow: 0 24px 48px -24px rgba(14,23,38,0.55);
    position: relative; overflow: hidden;
}
.score-card::after {
    content: "";
    position: absolute; right: -80px; top: -80px;
    width: 260px; height: 260px; border-radius: 50%;
    background: radial-gradient(circle, rgba(61,79,224,0.45), rgba(61,79,224,0));
    pointer-events: none;
}
.ring-wrap { position: relative; width: 148px; height: 148px; flex: 0 0 auto; }
.ring-wrap svg { transform: rotate(-90deg); }
.ring-center {
    position: absolute; inset: 0;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.ring-num { font-family: 'Sora', sans-serif; font-size: 38px; font-weight: 700; letter-spacing: -1.5px; line-height: 1; }
.ring-cap { font-size: 11.5px; color: #A9B4CB; margin-top: 4px; }
.score-body { flex: 1 1 320px; position: relative; z-index: 1; }
.verdict { font-family: 'Sora', sans-serif; font-size: 26px; font-weight: 700; letter-spacing: -0.7px; margin: 0 0 8px 0; }
.verdict-sub { color: #B9C3D8; font-size: 14.5px; line-height: 1.6; margin: 0 0 20px 0; max-width: 520px; }

.split-bar { display: flex; height: 10px; border-radius: 999px; overflow: hidden; background: rgba(255,255,255,0.12); }
.split-bar span { display: block; height: 100%; }
.split-legend { display: flex; gap: 20px; margin-top: 12px; flex-wrap: wrap; font-size: 13px; color: #C9D2E4; }
.split-legend i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 7px; }

.conf-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 22px;
    margin-top: 16px;
    display: flex; align-items: center; gap: 20px; flex-wrap: wrap;
}
.conf-label { font-size: 13.5px; font-weight: 600; color: var(--ink); min-width: 150px; }
.conf-label small { display: block; font-weight: 400; color: var(--ink-faint); font-size: 12px; margin-top: 2px; }
.conf-track { flex: 1 1 240px; height: 8px; background: var(--mist); border-radius: 999px; overflow: hidden; }
.conf-fill { height: 100%; background: var(--accent); border-radius: 999px; }
.conf-val { font-family: 'Sora', sans-serif; font-size: 20px; font-weight: 700; color: var(--ink); min-width: 56px; text-align: right; }

.skill-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 20px 22px 22px 22px;
    min-height: 210px;
    box-shadow: 0 1px 2px rgba(14,23,38,0.03);
}
.skill-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.skill-name { display: flex; align-items: center; gap: 9px; font-family: 'Sora', sans-serif; font-size: 14.5px; font-weight: 600; color: var(--ink); }
.skill-dot { width: 10px; height: 10px; border-radius: 3px; }
.skill-count {
    min-width: 30px; height: 30px; padding: 0 9px; border-radius: 999px;
    display: grid; place-items: center;
    font-family: 'Sora', sans-serif; font-weight: 700; font-size: 14px;
}
.chip {
    display: inline-block; padding: 6px 12px; margin: 0 6px 8px 0;
    border-radius: 10px; font-size: 13px; font-weight: 500;
}
.chip-empty { color: var(--ink-faint); font-size: 13px; }

.c-match .skill-dot { background: var(--match); }
.c-match .skill-count, .c-match .chip { background: var(--match-soft); color: var(--match); }
.c-partial .skill-dot { background: var(--partial); }
.c-partial .skill-count, .c-partial .chip { background: var(--partial-soft); color: var(--partial); }
.c-missing .skill-dot { background: var(--missing); }
.c-missing .skill-count, .c-missing .chip { background: var(--missing-soft); color: var(--missing); }

.next-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px 24px 14px 24px;
    margin-top: 16px;
}
.next-title { font-family: 'Sora', sans-serif; font-size: 16px; font-weight: 600; margin-bottom: 14px; color: var(--ink); }
.next-item {
    display: flex; gap: 14px; align-items: flex-start;
    padding: 13px 0; border-top: 1px solid var(--line);
    font-size: 14.5px; line-height: 1.55; color: var(--ink-soft);
}
.next-item:first-of-type { border-top: none; padding-top: 2px; }
.next-check {
    flex: 0 0 22px; height: 22px; margin-top: 1px; border-radius: 7px;
    border: 1.5px solid #C4CBDA;
}

div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    margin-top: 16px;
}
div[data-testid="stExpander"] summary { font-weight: 600; color: var(--ink-soft); }

.footer {
    text-align: center; color: var(--ink-faint); font-size: 12.5px;
    margin-top: 56px; padding-top: 22px; border-top: 1px solid var(--line);
}

@media (max-width: 720px) {
    .score-card { padding: 24px 22px; }
    .hero-sub { font-size: 15.5px; }
}
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""


def compact(markup: str) -> str:
    """Strip indentation/newlines so Markdown never turns HTML into a code block."""
    return "".join(line.strip() for line in markup.splitlines())


def render(markup: str) -> None:
    st.markdown(compact(markup), unsafe_allow_html=True)


def esc(value) -> str:
    return html.escape(str(value))


def to_percent(value):
    try:
        number = float(str(value).replace("%", "").strip())
    except (TypeError, ValueError):
        return None
    if 0 <= number <= 1:
        number *= 100
    return max(0.0, min(100.0, number))


def chips(items) -> str:
    if not items:
        return '<span class="chip-empty">Nothing here</span>'
    return "".join(f'<span class="chip">{esc(item)}</span>' for item in items)


def skill_card(title: str, items, css_class: str) -> str:
    return f"""
    <div class="skill-card {css_class}">
        <div class="skill-head">
            <div class="skill-name"><span class="skill-dot"></span>{title}</div>
            <div class="skill-count">{len(items)}</div>
        </div>
        <div>{chips(items)}</div>
    </div>
    """


def verdict_for(score: float):
    if score >= 80:
        return "Strong fit", "Most of the required skills are backed by evidence in the resume."
    if score >= 55:
        return "Promising fit", "The core is covered, but a few requirements need a closer look."
    if score >= 30:
        return "Partial fit", "Some requirements are covered. Several gaps remain."
    return "Weak fit", "The resume shows little evidence for the skills this role asks for."


SAMPLE_RESUME = (
    "Data Scientist with 3 years of experience.\n"
    "Skills: Python, SQL, pandas, scikit-learn, FastAPI\n"
    "Built and deployed a churn prediction API using FastAPI and scikit-learn.\n"
    "Wrote SQL pipelines on PostgreSQL for weekly reporting."
)
SAMPLE_JD = (
    "We are hiring a Machine Learning Engineer.\n"
    "Required: Python, SQL, FastAPI, Docker, model deployment, AWS.\n"
    "Nice to have: Kubernetes, CI/CD, MLflow."
)


def load_sample():
    st.session_state["resume"] = SAMPLE_RESUME
    st.session_state["job_description"] = SAMPLE_JD


def clear_inputs():
    st.session_state["resume"] = ""
    st.session_state["job_description"] = ""


st.session_state.setdefault("resume", "")
st.session_state.setdefault("job_description", "")

st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header + hero
# ---------------------------------------------------------------------------
render(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-mark">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9"></circle>
                    <path d="M15.5 8.5l-2 5-5 2 2-5z"></path>
                </svg>
            </div>
            Nugen Job Intelligence
        </div>
        <div class="status-pill"><span class="status-dot"></span>Domain aligned model</div>
    </div>

    <div class="hero">
        <h1 class="hero-title">See which skills a resume can actually prove.</h1>
        <p class="hero-sub">
            Paste a resume and a job description. Nugen reads both, then a rule check
            removes any skill the resume does not support.
        </p>
        <div class="hero-steps">
            <span class="hero-step"><b>1</b>Paste both texts</span>
            <span class="hero-step"><b>2</b>Nugen analyzes the match</span>
            <span class="hero-step"><b>3</b>Rules verify each skill</span>
        </div>
    </div>
    """
)

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    render(
        """
        <div class="panel-head"><div class="panel-title">Candidate resume</div></div>
        <div class="panel-hint">Paste the resume text or the key experience.</div>
        """
    )
    resume = st.text_area(
        "Candidate resume",
        key="resume",
        placeholder="Python, SQL, FastAPI, scikit-learn...\nDeployed a machine learning API to production...",
        height=300,
        label_visibility="collapsed",
    )
    st.caption(f"{len(resume.split())} words")

with col2:
    render(
        """
        <div class="panel-head"><div class="panel-title">Job description</div></div>
        <div class="panel-hint">Paste the role requirements or the full posting.</div>
        """
    )
    job_description = st.text_area(
        "Job description",
        key="job_description",
        placeholder="We need Python, SQL, FastAPI, Docker and model deployment...",
        height=300,
        label_visibility="collapsed",
    )
    st.caption(f"{len(job_description.split())} words")

st.write("")
b1, b2, b3 = st.columns([3, 1, 1], gap="small")
with b1:
    analyze = st.button("Analyze candidate", type="primary", use_container_width=True)
with b2:
    st.button("Try an example", on_click=load_sample, use_container_width=True)
with b3:
    st.button("Clear", on_click=clear_inputs, use_container_width=True)

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
if analyze:
    if not resume.strip() or not job_description.strip():
        st.warning("Add both a resume and a job description, then select Analyze candidate.")
    else:
        with st.spinner("Analyzing the resume and verifying each skill..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"resume": resume, "job_description": job_description},
                    timeout=60,
                )

                if response.status_code != 200:
                    st.error("The backend returned an error. Check the details below.")
                    st.code(response.text)
                else:
                    data = response.json()

                    matched = data.get("matched", []) or []
                    partial = data.get("partially_matched", []) or []
                    missing = data.get("missing", []) or []
                    recommendations = data.get("recommendations", []) or []
                    confidence = to_percent(data.get("confidence"))

                    total = len(matched) + len(partial) + len(missing)
                    score = ((len(matched) + 0.5 * len(partial)) / total * 100) if total else 0.0
                    verdict, verdict_text = verdict_for(score)

                    ring_color = (
                        "#3FD1A8" if score >= 70 else "#F2B84B" if score >= 40 else "#F0708A"
                    )
                    circumference = 2 * 3.14159265 * 62
                    dash = circumference * score / 100

                    pct = lambda n: (n / total * 100) if total else 0

                    render(
                        """
                        <div class="section-title">Candidate evaluation</div>
                        <div class="section-sub">Result after Nugen analysis and rule based validation.</div>
                        """
                    )

                    render(
                        f"""
                        <div class="score-card">
                            <div class="ring-wrap">
                                <svg width="148" height="148" viewBox="0 0 148 148">
                                    <circle cx="74" cy="74" r="62" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="12"></circle>
                                    <circle cx="74" cy="74" r="62" fill="none" stroke="{ring_color}" stroke-width="12"
                                            stroke-linecap="round" stroke-dasharray="{dash:.1f} {circumference:.1f}"></circle>
                                </svg>
                                <div class="ring-center">
                                    <div class="ring-num">{score:.0f}%</div>
                                    <div class="ring-cap">skill match</div>
                                </div>
                            </div>
                            <div class="score-body">
                                <div class="verdict">{verdict}</div>
                                <p class="verdict-sub">{verdict_text}</p>
                                <div class="split-bar">
                                    <span style="width:{pct(len(matched)):.1f}%;background:#3FD1A8"></span>
                                    <span style="width:{pct(len(partial)):.1f}%;background:#F2B84B"></span>
                                    <span style="width:{pct(len(missing)):.1f}%;background:#F0708A"></span>
                                </div>
                                <div class="split-legend">
                                    <span><i style="background:#3FD1A8"></i>{len(matched)} matched</span>
                                    <span><i style="background:#F2B84B"></i>{len(partial)} partial</span>
                                    <span><i style="background:#F0708A"></i>{len(missing)} missing</span>
                                </div>
                            </div>
                        </div>
                        """
                    )

                    if confidence is not None:
                        render(
                            f"""
                            <div class="conf-card">
                                <div class="conf-label">Model confidence
                                    <small>How sure Nugen is about this analysis</small>
                                </div>
                                <div class="conf-track"><div class="conf-fill" style="width:{confidence:.0f}%"></div></div>
                                <div class="conf-val">{confidence:.0f}%</div>
                            </div>
                            """
                        )

                    st.write("")
                    c1, c2, c3 = st.columns(3, gap="medium")
                    with c1:
                        render(skill_card("Matched", matched, "c-match"))
                    with c2:
                        render(skill_card("Partially matched", partial, "c-partial"))
                    with c3:
                        render(skill_card("Missing", missing, "c-missing"))

                    if recommendations:
                        items = "".join(
                            f'<div class="next-item"><span class="next-check"></span><span>{esc(item)}</span></div>'
                            for item in recommendations
                        )
                        render(
                            f"""
                            <div class="next-card">
                                <div class="next-title">Recommended next steps</div>
                                {items}
                            </div>
                            """
                        )

                    with st.expander("View raw Nugen analysis"):
                        st.write(data.get("nugen_analysis", "No model analysis returned."))

            except requests.exceptions.ConnectionError:
                st.error("The backend is not running. Start it with: uvicorn app:app --reload")
            except requests.exceptions.Timeout:
                st.error("The analysis timed out. Try again, or shorten the texts.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

render(
    """
    <div class="footer">
        Nugen domain alignment · FastAPI · Rule based skill validation
    </div>
    """
)