import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AHP Calculator · University of Barishal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;1,400;1,600&family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], [class*="st-"], div, p, span, label {
    font-family: 'Source Sans 3', 'Segoe UI', Tahoma, Geneva, sans-serif !important;
}

.stApp {
    background-color: #f8f6f1 !important;
    background-image:
        radial-gradient(ellipse 1000px 700px at 15% 5%, rgba(78,130,96,0.06) 0%, transparent 65%),
        radial-gradient(ellipse 700px 500px at 85% 90%, rgba(160,130,80,0.05) 0%, transparent 65%) !important;
    min-height: 100vh;
}
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 60px !important;
    max-width: 1200px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f0ece1 !important;
    border-right: 1px solid #d8cfbf !important;
}
section[data-testid="stSidebar"] > div { background-color: #f0ece1 !important; }
section[data-testid="stSidebar"] * {
    font-family: 'Source Sans 3', 'Segoe UI', sans-serif !important;
    color: #1a2418 !important;
}
section[data-testid="stSidebar"] h3 {
    font-family: 'Playfair Display', Georgia, 'Times New Roman', serif !important;
    font-size: 17px !important; font-weight: 600 !important;
    color: #1a2418 !important; margin-top: 16px !important; margin-bottom: 8px !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown li,
section[data-testid="stSidebar"] .stMarkdown strong {
    color: #3a4a38 !important; font-size: 13px !important;
}

/* Textarea */
textarea, .stTextArea textarea {
    background-color: #fdfcf8 !important;
    border: 1px solid #cdc5b4 !important;
    border-radius: 8px !important;
    color: #1a2418 !important;
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-size: 12px !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: #4e8260 !important;
    box-shadow: 0 0 0 2px rgba(78,130,96,0.15) !important;
    outline: none !important;
}

/* Number input */
div[data-testid="stNumberInput"] input {
    background-color: #fdfcf8 !important;
    border: 1px solid #cdc5b4 !important;
    border-radius: 7px !important;
    color: #1a2418 !important;
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-size: 13px !important;
    text-align: center !important;
    padding: 6px 4px !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #4e8260 !important;
    box-shadow: 0 0 0 2px rgba(78,130,96,0.15) !important;
}
div[data-testid="stNumberInput"] button {
    background-color: #eee8da !important;
    border-color: #cdc5b4 !important;
    color: #3a4a38 !important;
}

/* Run button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #2d5a3d 0%, #4e8260 50%, #3d6b50 100%) !important;
    color: #f0f7f2 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 3.5px !important;
    padding: 16px 0 !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    box-shadow: 0 4px 18px rgba(45,90,61,0.28), 0 1px 4px rgba(45,90,61,0.15) !important;
    transition: all 0.22s ease !important;
    margin-top: 4px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e3d29 0%, #3d6b50 50%, #2d5a3d 100%) !important;
    box-shadow: 0 6px 24px rgba(45,90,61,0.38) !important;
    transform: translateY(-1px) !important;
}
.stButton > button p {
    color: #f0f7f2 !important;
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-weight: 600 !important; letter-spacing: 3.5px !important;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    border: 1px solid #d8cfbf !important;
    overflow: hidden !important;
    background: #fdfcf8 !important;
}
div[data-testid="stDataFrame"] * {
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-size: 12px !important; color: #1a2418 !important;
}

/* Alerts */
div[data-testid="stAlert"] { border-radius: 10px !important; }

/* Caption */
.stCaption, div[data-testid="stCaptionContainer"] p {
    color: #8a7d6a !important; font-size: 11px !important;
    font-family: 'Source Code Pro', 'Courier New', monospace !important;
    font-style: italic !important;
}

/* Latex */
.stLatex, .katex { color: #2d3a2a !important; font-size: 13px !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0ece1; }
::-webkit-scrollbar-thumb { background: #b0a898; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #8a7d6a; }

hr { border-color: #d8cfbf !important; }

/* Card */
.ahp-card {
    background: #fdfcf8;
    padding: 28px 32px 24px 32px;
    border-radius: 14px;
    border: 1px solid #d8cfbf;
    margin-bottom: 22px;
    position: relative;
    box-shadow: 0 2px 16px rgba(60,45,25,0.06), 0 1px 3px rgba(60,45,25,0.04);
}
.ahp-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #4e8260 0%, #7ab394 40%, #c9a050 100%);
    border-radius: 14px 14px 0 0;
}

/* Section header */
.ahp-sec { display: flex; align-items: center; gap: 14px; margin-bottom: 4px; }
.ahp-sec-label {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 20px; font-weight: 700; color: #1a2418;
    letter-spacing: 0.2px; white-space: nowrap;
}
.ahp-sec-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, #c8bfb0 0%, transparent 100%);
}
.ahp-sec-badge {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 10px; font-weight: 600;
    color: #4e8260; background: #eaf3ed;
    border: 1px solid #a8ccb5; border-radius: 20px;
    padding: 3px 12px; letter-spacing: 1px;
    text-transform: uppercase; white-space: nowrap;
}
.ahp-sec-sub {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 13px; color: #7a6e60;
    margin-bottom: 20px; margin-top: 4px;
    font-weight: 400; letter-spacing: 0.1px;
}

/* Matrix cells */
.ahp-diag {
    text-align: center; padding: 7px 4px;
    background: #eaf3ed; border-radius: 7px;
    color: #3d6b50; font-weight: 600;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 14px; border: 1px solid #a8ccb5;
}
.ahp-recip {
    text-align: center; padding: 7px 4px;
    color: #a89880;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 12px;
}
.ahp-row-label {
    padding: 8px 6px; color: #4e7060; font-size: 12px;
    font-family: 'Source Code Pro', monospace !important;
    font-weight: 600; letter-spacing: 0.5px; margin-top: 2px;
}

/* Metrics */
.ahp-metric {
    background: linear-gradient(145deg, #fdfcf8 0%, #f5f0e6 100%);
    border-radius: 12px; border: 1px solid #d8cfbf;
    padding: 22px 14px 18px 14px; text-align: center;
    box-shadow: 0 2px 10px rgba(60,45,25,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.ahp-metric:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(60,45,25,0.09); }
.ahp-metric-label {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 9px; color: #9a8c7a;
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;
}
.ahp-metric-val {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 20px; font-weight: 700; color: #1a2418; letter-spacing: -0.5px;
}
.ahp-metric-val.ok   { color: #2d6b48; }
.ahp-metric-val.fail { color: #b03030; }
.ahp-metric-sub {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 10px; color: #9a8c7a; margin-top: 7px; letter-spacing: 0.4px;
}

/* Sidebar chips */
.sb-chip {
    background: #eaf3ed; border-radius: 8px;
    padding: 8px 12px; margin: 6px 0 12px 0;
    border: 1px solid #a8ccb5;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 11px; color: #2d6b48; font-weight: 600; letter-spacing: 0.3px;
}
.sb-note {
    background: #fdfcf8; border-radius: 7px;
    padding: 8px 12px; margin-top: 6px; border: 1px solid #d8cfbf;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 11px; color: #8a7d6a; letter-spacing: 0.3px;
}
.sb-ok {
    background: #eaf3ed; border-left: 3px solid #4e8260;
    border-radius: 0 8px 8px 0; padding: 8px 12px; margin-top: 8px;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 11px; color: #2d6b48; letter-spacing: 0.4px;
}

/* GIS box */
.gis-box {
    background: #eaf3ed; border: 1px solid #a8ccb5;
    border-left: 4px solid #4e8260;
    padding: 14px 18px; border-radius: 0 10px 10px 0; margin-top: 16px;
}
.gis-box-title {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 10px; font-weight: 700; color: #2d6b48;
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px;
}
.gis-box-body {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 13px; color: #3a5a42; line-height: 1.65;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
.ph-wrap {
    position: relative;
    margin: -20px -1rem 30px -1rem;
    padding: 44px 48px 36px 48px;
    background: linear-gradient(180deg, #eef5f0 0%, rgba(248,246,241,0) 100%);
    border-bottom: 1px solid #d0c8b8;
    overflow: hidden;
    display: flex; align-items: center; justify-content: center;
}
.ph-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(78,130,96,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(78,130,96,0.08) 1px, transparent 1px);
    background-size: 36px 36px;
    -webkit-mask-image: radial-gradient(ellipse 85% 90% at 50% 50%, black 0%, transparent 100%);
    mask-image: radial-gradient(ellipse 85% 90% at 50% 50%, black 0%, transparent 100%);
    pointer-events: none;
}
.ph-inner {
    position: relative; z-index: 2;
    display: flex; align-items: center; gap: 44px;
    max-width: 960px; width: 100%;
}

/* Logo */
.ph-logo-shell { position: relative; width: 108px; height: 108px; flex-shrink: 0; }
.ph-ring-2 {
    position: absolute; inset: -10px; border-radius: 50%;
    border: 1px dashed rgba(78,130,96,0.22);
    animation: spinCCW 28s linear infinite;
}
.ph-ring-3 {
    position: absolute; inset: -20px; border-radius: 50%;
    border: 1px solid rgba(78,130,96,0.12);
    animation: spinCW 50s linear infinite;
}
.ph-disc {
    width: 108px; height: 108px; border-radius: 50%;
    background: linear-gradient(145deg, #fdfcf8 0%, #eef5f0 100%);
    border: 2px solid #a8ccb5;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 8px 32px rgba(45,90,61,0.14), 0 2px 8px rgba(45,90,61,0.08),
                inset 0 1px 0 rgba(255,255,255,0.9);
    animation: floatDisc 6s ease-in-out infinite;
    position: relative; z-index: 1;
}
@keyframes spinCW  { to { transform: rotate(360deg);  } }
@keyframes spinCCW { to { transform: rotate(-360deg); } }
@keyframes floatDisc { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }

.svg-ln { stroke-dasharray: 80; stroke-dashoffset: 80; animation: drawLn 2.5s ease-out forwards infinite alternate; }
.svg-ln:nth-child(1){animation-delay:0s;} .svg-ln:nth-child(2){animation-delay:0.4s;} .svg-ln:nth-child(3){animation-delay:0.8s;}
.svg-nd { animation: ndPulse 2.8s ease-in-out infinite; transform-origin:center; }
.svg-nd:nth-child(1){animation-delay:0s;} .svg-nd:nth-child(2){animation-delay:0.5s;} .svg-nd:nth-child(3){animation-delay:0.9s;} .svg-nd:nth-child(4){animation-delay:1.3s;}
@keyframes drawLn { to { stroke-dashoffset: 0; } }
@keyframes ndPulse { 0%,100%{opacity:0.8;transform:scale(1);} 50%{opacity:1;transform:scale(1.18);} }

/* Title */
.ph-text { display: flex; flex-direction: column; }
.ph-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-family: 'Source Code Pro','Courier New',monospace;
    font-size: 10px; font-weight: 600;
    color: #4e8260; background: #eaf3ed;
    border: 1px solid #a8ccb5; padding: 4px 14px;
    border-radius: 20px; text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 14px; width: fit-content;
}
.ph-badge-dot {
    width: 5px; height: 5px; border-radius: 50%; background: #4e8260;
    animation: dotBlink 2s ease-in-out infinite;
}
@keyframes dotBlink { 0%,100%{opacity:0.4;transform:scale(0.8);} 50%{opacity:1;transform:scale(1.3);} }

.ph-title {
    font-family: 'Playfair Display', Georgia, 'Times New Roman', serif !important;
    font-size: 54px; font-weight: 800; color: #1a2418;
    line-height: 1; margin: 0 0 8px 0; letter-spacing: -1.5px;
}
.ph-title-em {
    font-style: italic;
    background: linear-gradient(130deg, #4e8260 0%, #2d5a3d 40%, #c9a050 100%);
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.ph-subtitle {
    font-family: 'Source Code Pro','Courier New',monospace !important;
    font-size: 11px; font-weight: 500; color: #8a7d6a;
    text-transform: uppercase; letter-spacing: 4px; margin: 0;
}
.ph-accent {
    display: flex; align-items: center; gap: 8px; margin-top: 14px;
}
.ph-accent-bar { height: 2px; width: 40px; border-radius: 2px; background: linear-gradient(90deg,#4e8260,#c9a050); }
.ph-accent-dot { width: 5px; height: 5px; border-radius: 50%; }
.ph-accent-line { height: 1px; flex: 1; max-width: 80px; background: linear-gradient(90deg,#d8cfbf,transparent); }

@media (max-width: 800px) {
    .ph-inner { flex-direction: column; text-align: center; gap: 24px; }
    .ph-badge  { align-self: center; }
    .ph-title  { font-size: 38px; }
    .ph-accent { justify-content: center; }
}
</style>

<div class="ph-wrap">
  <div class="ph-inner">
    <div class="ph-logo-shell">
      <div class="ph-ring-3"></div>
      <div class="ph-ring-2"></div>
      <div class="ph-disc">
        <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="lg1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%"   stop-color="#2d5a3d"/>
              <stop offset="100%" stop-color="#4e8260"/>
            </linearGradient>
            <linearGradient id="lg2" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%"   stop-color="#4e8260"/>
              <stop offset="100%" stop-color="#c9a050"/>
            </linearGradient>
          </defs>
          <line class="svg-ln" x1="50" y1="30" x2="20" y2="74" stroke="url(#lg2)" stroke-width="2.5" stroke-linecap="round"/>
          <line class="svg-ln" x1="50" y1="30" x2="50" y2="74" stroke="url(#lg2)" stroke-width="2.5" stroke-linecap="round"/>
          <line class="svg-ln" x1="50" y1="30" x2="80" y2="74" stroke="url(#lg2)" stroke-width="2.5" stroke-linecap="round"/>
          <circle class="svg-nd" cx="50" cy="26" r="11" fill="url(#lg1)" opacity="0.95"/>
          <circle cx="50" cy="26" r="4.5" fill="#fdfcf8" opacity="0.95"/>
          <circle class="svg-nd" cx="20" cy="77" r="8.5" fill="url(#lg2)" opacity="0.90"/>
          <circle cx="20" cy="77" r="3.5" fill="#fdfcf8" opacity="0.90"/>
          <circle class="svg-nd" cx="50" cy="77" r="8.5" fill="url(#lg2)" opacity="0.90"/>
          <circle cx="50" cy="77" r="3.5" fill="#fdfcf8" opacity="0.90"/>
          <circle class="svg-nd" cx="80" cy="77" r="8.5" fill="url(#lg2)" opacity="0.90"/>
          <circle cx="80" cy="77" r="3.5" fill="#fdfcf8" opacity="0.90"/>
        </svg>
      </div>
    </div>
    <div class="ph-text">
      <div class="ph-badge">
        <span class="ph-badge-dot"></span>
        Decision Support System
      </div>
      <h1 class="ph-title">AHP&nbsp;<span class="ph-title-em">Calculator</span></h1>
      <p class="ph-subtitle">Analytic Hierarchy Process &nbsp;&middot;&nbsp; Multi-Criteria Decision Analysis</p>
      <div class="ph-accent">
        <div class="ph-accent-bar"></div>
        <div class="ph-accent-dot" style="background:#4e8260;"></div>
        <div class="ph-accent-dot" style="background:#7ab394;"></div>
        <div class="ph-accent-dot" style="background:#c9a050;"></div>
        <div class="ph-accent-line"></div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="padding:16px 2px 4px 2px;">
  <div style="font-family:'Playfair Display',Georgia,serif;font-size:22px;font-weight:700;color:#1a2418;margin-bottom:2px;">Configuration</div>
  <div style="font-family:'Source Code Pro',monospace;font-size:11px;color:#8a7d6a;margin-bottom:12px;letter-spacing:0.5px;">AHP Model Setup</div>
  <div style="height:1px;background:linear-gradient(90deg,#a8ccb5,transparent);margin-bottom:12px;"></div>
</div>
""", unsafe_allow_html=True)

criteria_input = st.sidebar.text_area(
    "Criteria (comma-separated)",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo",
    help="Enter short names for your criteria"
)
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

st.sidebar.markdown(f'<div class="sb-chip">n = {n} &nbsp;&nbsp;criteria detected</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### AHP Formulas")

for label, formula in [
    ("Step 1 · Normalize columns",  r"\bar{a}_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}}"),
    ("Step 2 · Average / Weight",   r"W_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}"),
    ("Step 3 · Criteria Weight",    r"CW_i = \frac{W_i}{n}"),
    ("Step 4 · Consistency Matrix", r"CM_{ij} = a_{ij} \times CW_j"),
    ("Step 5 · Weighted Sum",       r"WS_i = \sum_{j=1}^{n} CM_{ij}"),
    ("Step 6 · Lambda Max",         r"\lambda_{max} = \frac{1}{n}\sum_{i=1}^{n}\frac{WS_i}{CW_i}"),
    ("Step 7 · CI",                 r"CI = \frac{\lambda_{max} - n}{n - 1}"),
    ("Step 8 · CR",                 r"CR = \frac{CI}{RI}"),
]:
    st.sidebar.markdown(f"**{label}**")
    st.sidebar.latex(formula)

st.sidebar.markdown('<div class="sb-ok">&#10003;&nbsp; Acceptable when CR &lt; 0.10</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

RI_dict = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,  5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
   11: 1.51,12: 1.48,13: 1.56,14: 1.57, 15: 1.59
}

st.sidebar.markdown("### Random Index (RI)")
ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n", "RI"])
st.sidebar.dataframe(ri_df, use_container_width=True, hide_index=True)
st.sidebar.markdown(f'<div class="sb-note">n = {n} &nbsp;&#8594;&nbsp; RI = {RI_dict.get(n, 1.59)}</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### Saaty Scale")
saaty_df = pd.DataFrame({
    "Val":     [1,2,3,4,5,6,7,8,9],
    "Meaning": ["Equal","Weak","Moderate","Mod+","Strong","Strong+","V.Strong","V.V.Strong","Extreme"],
    "1/x":     ["1/1","1/2","1/3","1/4","1/5","1/6","1/7","1/8","1/9"]
})
st.sidebar.dataframe(saaty_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
#  MATRIX INPUT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="ahp-card">
  <div class="ahp-sec">
    <span class="ahp-sec-label">Pairwise Comparison Matrix</span>
    <span class="ahp-sec-badge">Step 01</span>
    <span class="ahp-sec-line"></span>
  </div>
  <div class="ahp-sec-sub">Fill the upper triangle only &nbsp;&middot;&nbsp; Diagonal fixed at 1 &nbsp;&middot;&nbsp; Reciprocals auto-computed &nbsp;&middot;&nbsp; Saaty scale 1&ndash;9</div>
""", unsafe_allow_html=True)

matrix = np.ones((n, n))

hcols = st.columns([1.1] + [1] * n)
hcols[0].write("")
for j in range(n):
    hcols[j+1].markdown(
        f"<div class='ahp-row-label' style='text-align:center;color:#4e8260;"
        f"border-bottom:2px solid #d0c8b8;padding-bottom:8px;margin-bottom:6px;font-weight:700;'>"
        f"{criteria[j]}</div>", unsafe_allow_html=True)

for i in range(n):
    cols = st.columns([1.1] + [1] * n)
    cols[0].markdown(
        f"<div class='ahp-row-label' style='margin-top:6px;font-weight:700;color:#2d5a3d;'>"
        f"{criteria[i]}</div>", unsafe_allow_html=True)
    for j in range(n):
        if i == j:
            cols[j+1].markdown("<div class='ahp-diag'>1</div>", unsafe_allow_html=True)
        elif j > i:
            val = cols[j+1].number_input(
                f"{criteria[i]} vs {criteria[j]}",
                min_value=0.111, max_value=9.0, value=1.0, step=0.5,
                key=f"m_{i}_{j}", label_visibility="collapsed"
            )
            matrix[i][j] = val
            matrix[j][i] = round(1.0 / val, 6)
        else:
            recip = matrix[j][i]
            label = f"1/{round(recip)}" if recip >= 1 else f"{matrix[i][j]:.3f}"
            cols[j+1].markdown(f"<div class='ahp-recip'>{label}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  RUN + RESULTS
# ══════════════════════════════════════════════════════════════
if st.button("RUN AHP ANALYSIS", use_container_width=True):

    col_sums           = matrix.sum(axis=0)
    norm_matrix        = matrix / col_sums
    avg_weight         = norm_matrix.mean(axis=1)
    CW                 = avg_weight / n
    CW_pct             = CW / CW.sum() * 100
    consistency_matrix = matrix * CW[np.newaxis, :]
    weighted_sum       = consistency_matrix.sum(axis=1)
    wsv_over_cw        = weighted_sum / CW
    lambda_max         = wsv_over_cw.mean()
    CI                 = (lambda_max - n) / (n - 1)
    RI                 = RI_dict.get(n, 1.59)
    CR                 = CI / RI if RI > 0 else 0.0

    def card_open(title, badge, sub):
        st.markdown(f"""
        <div class="ahp-card">
          <div class="ahp-sec">
            <span class="ahp-sec-label">{title}</span>
            <span class="ahp-sec-badge">{badge}</span>
            <span class="ahp-sec-line"></span>
          </div>
          <div class="ahp-sec-sub">{sub}</div>
        """, unsafe_allow_html=True)

    def card_close():
        st.markdown("</div>", unsafe_allow_html=True)

    # Table 1
    card_open("Pairwise Comparison Matrix", "Table 1", "Raw input matrix with column sums")
    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria).round(4)
    df1.loc["Column Sum"] = col_sums.round(4)
    st.dataframe(df1, use_container_width=True)
    st.caption("Diagonal = 1  ·  Upper = inputs  ·  Lower = reciprocals  ·  Last row = column sums")
    card_close()

    # Table 2
    card_open("Normalized Pairwise Matrix", "Table 2", "Column-normalized values with priority weights")
    df2 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria).round(9)
    df2["Average / W"] = avg_weight.round(3)
    df2["CW"]          = CW.round(3)
    df2["CW %"]        = CW_pct.round(3)
    totals2 = {c: norm_matrix[:, j].sum() for j, c in enumerate(criteria)}
    totals2["Average / W"] = round(avg_weight.sum(), 3)
    totals2["CW"]          = round(CW.sum(), 3)
    totals2["CW %"]        = round(CW_pct.sum(), 3)
    df2.loc["TOTAL"] = totals2
    st.dataframe(df2, use_container_width=True)
    st.caption("Each cell = original / column sum  ·  W = row mean  ·  CW = W / n  ·  Column sums = 1.0")
    card_close()

    # Table 3
    card_open("Consistency Matrix", "Table 3", "Each cell = pairwise[i][j] x CW[j]")
    cw_row = pd.DataFrame([list(CW.round(3)) + [""]], columns=criteria + ["Weighted Sum"], index=["CW"])
    st.dataframe(cw_row, use_container_width=True)
    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria).round(3)
    df3["Weighted Sum"] = weighted_sum.round(3)
    df3.loc["TOTAL"]    = df3.sum()
    st.dataframe(df3, use_container_width=True)
    st.caption("CW row = column weights used as multipliers  ·  Weighted Sum = row sum")
    card_close()

    # Table 4 + Metrics
    card_open("Consistency Summary", "Table 4", "Weighted sums, criteria weights and lambda values per criterion")
    df4 = pd.DataFrame({
        "Criteria":             criteria,
        "Weighted Sum (WS)":    weighted_sum.round(4),
        "Criteria Weight (CW)": CW.round(4),
        "WS / CW (lambda)":    wsv_over_cw.round(4),
    })
    total4 = pd.DataFrame([{
        "Criteria":             "TOTAL",
        "Weighted Sum (WS)":    round(weighted_sum.sum(), 4),
        "Criteria Weight (CW)": round(CW.sum(), 4),
        "WS / CW (lambda)":    round(wsv_over_cw.sum(), 4),
    }])
    df4 = pd.concat([df4, total4], ignore_index=True)
    st.dataframe(df4, use_container_width=True, hide_index=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    cr_cls     = "ok"          if CR < 0.10 else "fail"
    cr_verdict = "Consistent"  if CR < 0.10 else "Inconsistent"
    m1, m2, m3, m4 = st.columns(4)
    for col, lbl, val, sub in [
        (m1, "Lambda max",  f"{lambda_max:.6f}", "Principal eigenvalue"),
        (m2, "CI",          f"{CI:.6f}",         "Consistency index"),
        (m3, f"RI  n={n}",  f"{RI}",             "Random index"),
        (m4, "CR",          f"{CR:.6f}",          cr_verdict),
    ]:
        extra = f" {cr_cls}" if lbl == "CR" else ""
        with col:
            st.markdown(f"""
            <div class="ahp-metric">
              <div class="ahp-metric-label">{lbl}</div>
              <div class="ahp-metric-val{extra}">{val}</div>
              <div class="ahp-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)
    card_close()

    # Table 5
    card_open("GIS Priority Weights", "Table 5", "Ranked criteria weights for GIS weighted overlay analysis")
    sorted_idx = np.argsort(avg_weight)[::-1]
    df5 = pd.DataFrame({
        "Rank":             range(1, n+1),
        "Criteria":         [criteria[i]            for i in sorted_idx],
        "Avg / Weight (W)": [round(avg_weight[i],4) for i in sorted_idx],
        "Criteria CW":      [round(CW[i],4)         for i in sorted_idx],
        "CW %":             [float(CW_pct[i])       for i in sorted_idx],
    })
    st.dataframe(
        df5, use_container_width=True, hide_index=True,
        column_config={
            "Avg / Weight (W)": st.column_config.NumberColumn(format="%.4f"),
            "Criteria CW":      st.column_config.NumberColumn(format="%.4f"),
            "CW %": st.column_config.ProgressColumn(
                "CW %", help="Visual weight percentage",
                format="%.2f %%", min_value=0, max_value=100,
            )
        }
    )
    st.markdown("""
    <div class="gis-box">
      <div class="gis-box-title">GIS Application Ready</div>
      <div class="gis-box-body">
        Input the <strong>Criteria CW</strong> values into your spatial analysis tool
        (e.g., ArcGIS Weighted Overlay, QGIS Raster Calculator) to generate your
        suitability map. Ensure all input raster layers are reclassified to a common
        scale before multiplying by these weights.
      </div>
    </div>
    """, unsafe_allow_html=True)
    card_close()

    # Charts
    card_open("Weight Visualization", "Charts", "Priority weight distribution across all criteria")

    BG   = "#f8f6f1"; SURF = "#fdfcf8"; TXT = "#1a2418"; MUT = "#7a6e60"; GRID = "#e8e0d4"
    palette = ["#4e8260","#2d5a3d","#7ab394","#3d6b50","#a8ccb5",
               "#c9a050","#a07830","#d4b87a","#e8d4a0","#6d9e7a"]

    sc = [criteria[i] for i in sorted_idx]
    sw = [CW[i]       for i in sorted_idx]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)
    fig.patch.set_facecolor(BG)
    fig.subplots_adjust(wspace=0.34)

    ax1 = axes[0]
    ax1.set_facecolor(SURF)
    for sp in ax1.spines.values(): sp.set_color(GRID); sp.set_linewidth(0.8)
    bars = ax1.bar(sc, sw, color=[palette[i % len(palette)] for i in range(len(sw))],
                   edgecolor=SURF, linewidth=1.2, width=0.55, zorder=3)
    ax1.set_title("Criteria Weight (CW)", color=TXT, fontsize=12, fontweight="bold", pad=14, loc="left", fontfamily="monospace")
    ax1.set_xlabel("Criteria", color=MUT, fontsize=10, labelpad=8)
    ax1.set_ylabel("CW", color=MUT, fontsize=10, labelpad=8)
    ax1.tick_params(colors=MUT, labelsize=9)
    ax1.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    for bar, w in zip(bars, sw):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sw)*0.018,
                 f"{w:.4f}", ha="center", va="bottom",
                 color=TXT, fontsize=9, fontweight="bold", fontfamily="monospace")

    ax2 = axes[1]
    ax2.set_facecolor(BG)
    wedges, texts, auts = ax2.pie(
        sw, labels=sc, autopct="%1.1f%%",
        colors=palette[:len(sw)], startangle=140, pctdistance=0.74,
        textprops={"color": "#2d3a2a", "fontsize": 10, "fontfamily": "monospace"},
        wedgeprops={"edgecolor": BG, "linewidth": 2.5}
    )
    for at in auts: at.set_color(TXT); at.set_fontsize(9); at.set_fontweight("bold")
    ax2.set_title("CW Distribution", color=TXT, fontsize=12, fontweight="bold", pad=14, loc="left", fontfamily="monospace")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    card_close()

    # Result
    card_open("Consistency Interpretation", "Result", "Saaty consistency check for pairwise judgements")
    if CR < 0.10:
        st.success(f"CR = {CR:.6f} < 0.10 — Pairwise comparisons are **consistent**. Results are reliable.")
    else:
        st.error(f"CR = {CR:.6f} >= 0.10 — Pairwise comparisons are **inconsistent**. Please revise your matrix.")
        st.warning("Tip: Review judgments that violate transitivity (e.g., A > B, B > C but C > A).")

    st.markdown(f"""
| Parameter | Value | Formula |
|-----------|-------|---------|
| n | {n} | — |
| lambda\_max | {lambda_max:.6f} | mean(WS / CW) |
| CI | {CI:.6f} | (lambda\_max - n) / (n - 1) |
| RI | {RI} | Saaty table, n = {n} |
| CR | {CR:.6f} | CI / RI |
| Result | {"Consistent" if CR < 0.10 else "Inconsistent"} | CR {"<" if CR < 0.10 else ">="} 0.10 |
""")
    card_close()


# ══════════════════════════════════════════════════════════════
#  CREDITS FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@keyframes shimmerName {
    0%   { background-position: -500px 0; }
    100% { background-position: 500px 0; }
}
@keyframes orbitGold {
    from { transform: rotate(0deg)   translateX(46px) rotate(0deg);   }
    to   { transform: rotate(360deg) translateX(46px) rotate(-360deg); }
}
@keyframes floatAvatar {
    0%,100% { transform: translateY(0);    }
    50%      { transform: translateY(-5px); }
}
@keyframes footFadeIn {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes topSweep {
    0%   { background-position: 0% 50%;   }
    100% { background-position: 200% 50%; }
}

.pf-shell {
    margin-top: 64px;
    padding: 52px 40px 44px 40px;
    background: linear-gradient(160deg, #fdfcf8 0%, #f4f0e6 60%, #eef5f0 100%);
    border: 1px solid #d0c8b8;
    border-radius: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 28px rgba(45,70,30,0.08), 0 1px 4px rgba(45,70,30,0.05),
                inset 0 1px 0 rgba(255,255,255,0.9);
    animation: footFadeIn 0.9s ease-out both;
}
.pf-shell::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #4e8260,#7ab394,#c9a050,#4e8260,#7ab394,#c9a050);
    background-size: 400% auto;
    border-radius: 20px 20px 0 0;
    animation: topSweep 4s linear infinite;
}
.pf-shell::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(78,130,96,0.35), transparent);
}
.pf-bg-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(78,130,96,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(78,130,96,0.05) 1px, transparent 1px);
    background-size: 28px 28px;
    -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 0%, transparent 100%);
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 0%, transparent 100%);
    pointer-events: none;
}
.pf-wm {
    position: absolute; right: -24px; bottom: -24px;
    width: 200px; height: 200px; opacity: 0.04; pointer-events: none;
}

.pf-av-wrap {
    display: inline-block; position: relative;
    margin-bottom: 22px;
    animation: floatAvatar 6s ease-in-out infinite;
}
.pf-av {
    width: 88px; height: 88px; border-radius: 50%;
    background: linear-gradient(145deg, #eef5f0 0%, #fdfcf8 100%);
    border: 2.5px solid #a8ccb5;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto;
    box-shadow: 0 6px 24px rgba(45,90,61,0.14), 0 2px 6px rgba(45,90,61,0.08),
                inset 0 1px 0 rgba(255,255,255,0.9);
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 32px; font-weight: 800; font-style: italic; color: #3d6b50;
    position: relative; z-index: 1;
}
.pf-av-ring {
    position: absolute; inset: -10px; border-radius: 50%;
    border: 1px dashed rgba(78,130,96,0.28);
    animation: spinCW 20s linear infinite;
}
.pf-av-dot {
    position: absolute; top: 50%; left: 50%;
    width: 9px; height: 9px; margin: -4.5px 0 0 -4.5px;
    border-radius: 50%;
    background: radial-gradient(circle, #e8c060 0%, #c9a050 100%);
    box-shadow: 0 0 8px rgba(201,160,80,0.5);
    animation: orbitGold 4.5s linear infinite;
}

.pf-by {
    font-family: 'Source Code Pro','Courier New',monospace;
    font-size: 10px; color: #9a8c7a;
    text-transform: uppercase; letter-spacing: 3px; margin-bottom: 8px;
}
.pf-name {
    font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
    font-size: 34px; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.5px;
    background: linear-gradient(120deg, #1a2418 0%, #2d5a3d 30%, #4e8260 55%, #c9a050 80%, #1a2418 100%);
    background-size: 300% auto;
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmerName 5s linear infinite; display: inline-block;
}
.pf-dept {
    font-family: 'Source Sans 3','Segoe UI',sans-serif;
    font-size: 14px; color: #4a6040; font-weight: 500; margin-bottom: 3px;
}
.pf-univ {
    font-family: 'Source Code Pro','Courier New',monospace;
    font-size: 11px; color: #8a7d6a;
    text-transform: uppercase; letter-spacing: 2.5px; margin-bottom: 28px;
}

.pf-div {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; margin-bottom: 26px;
}
.pf-div-line {
    height: 1px; width: 55px;
    background: linear-gradient(90deg, transparent, #c8bfb0);
}
.pf-div-line.r { background: linear-gradient(90deg, #c8bfb0, transparent); }
.pf-div-gem {
    width: 7px; height: 7px;
    background: linear-gradient(135deg, #4e8260, #c9a050);
    border-radius: 1px; transform: rotate(45deg);
    box-shadow: 0 1px 4px rgba(78,130,96,0.3);
}

.pf-links { display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; }
.pf-btn {
    text-decoration: none !important;
    display: inline-flex; align-items: center; gap: 8px;
    padding: 11px 24px; border-radius: 30px;
    font-family: 'Source Code Pro','Courier New',monospace;
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.pf-green {
    color: #2d5a3d !important;
    background: rgba(78,130,96,0.10);
    border: 1.5px solid rgba(78,130,96,0.35);
}
.pf-green:hover {
    background: rgba(78,130,96,0.18); border-color: rgba(78,130,96,0.60);
    color: #1a3828 !important; transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(78,130,96,0.18);
}
.pf-gold {
    color: #7a5a1a !important;
    background: rgba(201,160,80,0.10);
    border: 1.5px solid rgba(201,160,80,0.40);
}
.pf-gold:hover {
    background: rgba(201,160,80,0.20); border-color: rgba(201,160,80,0.65);
    color: #5c4010 !important; transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(201,160,80,0.20);
}
</style>

<div class="pf-shell">
  <div class="pf-bg-grid"></div>
  <svg class="pf-wm" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" fill="none">
    <circle cx="50" cy="24" r="13" fill="#1a2418"/>
    <line x1="50" y1="37" x2="18" y2="80" stroke="#1a2418" stroke-width="3.5"/>
    <line x1="50" y1="37" x2="50" y2="80" stroke="#1a2418" stroke-width="3.5"/>
    <line x1="50" y1="37" x2="82" y2="80" stroke="#1a2418" stroke-width="3.5"/>
    <circle cx="18" cy="84" r="10" fill="#1a2418"/>
    <circle cx="50" cy="84" r="10" fill="#1a2418"/>
    <circle cx="82" cy="84" r="10" fill="#1a2418"/>
  </svg>

  <div class="pf-av-wrap">
    <div class="pf-av-ring"></div>
    <div class="pf-av-dot"></div>
    <div class="pf-av">A</div>
  </div>

  <div class="pf-by">Designed &amp; Developed by</div>
  <div class="pf-name">Anindo Paul Sourav</div>
  <div class="pf-dept">Department of Geology &amp; Mining</div>
  <div class="pf-univ">University of Barishal</div>

  <div class="pf-div">
    <div class="pf-div-line"></div>
    <div class="pf-div-gem"></div>
    <div class="pf-div-line r"></div>
  </div>

  <div class="pf-links">
    <a href="https://www.linkedin.com/in/anindo046/" target="_blank" class="pf-btn pf-green">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
      </svg>
      LinkedIn
    </a>
    <a href="https://anindo46.github.io/portfolio/" target="_blank" class="pf-btn pf-gold">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
      </svg>
      Portfolio
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
