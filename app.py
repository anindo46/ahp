import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="AHP Calculator", layout="wide")

# ─────────────────────────── STYLE ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #faf8f4;
    background-image:
        radial-gradient(ellipse 900px 600px at 20% 10%, rgba(99, 148, 120, 0.07) 0%, transparent 70%),
        radial-gradient(ellipse 700px 500px at 80% 80%, rgba(139, 115, 85, 0.06) 0%, transparent 70%);
}

section[data-testid="stSidebar"] {
    background: #f4f0e8 !important;
    border-right: 1px solid #ddd5c4 !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #2c3e30 !important;
    font-size: 18px !important;
}

.main .block-container { padding-top: 0 !important; }

/* Cards */
.ahp-card {
    background: rgba(255, 253, 248, 0.95);
    padding: 28px 32px;
    border-radius: 12px;
    border: 1px solid #e2d9cc;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 20px rgba(80, 60, 40, 0.06), 0 1px 4px rgba(80, 60, 40, 0.04);
    animation: cardRise 0.5s ease-out both;
}
.ahp-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #639478 0%, #a8c5b0 40%, #c9a96e 100%);
    border-radius: 12px 12px 0 0;
}

@keyframes cardRise {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Section headers */
.ahp-sec {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}
.ahp-sec-label {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    font-weight: 600;
    color: #1e2d22;
    letter-spacing: 0.2px;
}
.ahp-sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #c9bfb0 0%, transparent 100%);
}
.ahp-sec-badge {
    font-size: 10px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    color: #639478;
    background: #edf4ef;
    border: 1px solid #b5d0bc;
    border-radius: 20px;
    padding: 3px 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.ahp-sec-sub {
    font-size: 13px;
    color: #8a7f72;
    margin-bottom: 20px;
    font-weight: 400;
    letter-spacing: 0.2px;
}

/* Diagonal / reciprocal cells */
.ahp-diag {
    text-align: center;
    padding: 7px 4px;
    background: #edf4ef;
    border-radius: 7px;
    color: #639478;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    border: 1px solid #b5d0bc;
}
.ahp-recip {
    text-align: center;
    padding: 7px 4px;
    color: #b5a99a;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}
.ahp-row-label {
    padding: 8px 4px;
    color: #5a7060;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Metric boxes */
.ahp-metric {
    background: linear-gradient(145deg, #fdfcf9 0%, #f7f3ec 100%);
    border-radius: 12px;
    border: 1px solid #e2d9cc;
    padding: 22px 16px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(80, 60, 40, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.ahp-metric:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(80, 60, 40, 0.10);
}
.ahp-metric-label {
    font-size: 9px;
    color: #a89880;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
    margin-bottom: 10px;
}
.ahp-metric-val {
    font-size: 22px;
    font-weight: 700;
    color: #2c3e30;
    font-family: 'DM Mono', monospace;
    letter-spacing: -0.5px;
}
.ahp-metric-val.ok   { color: #3d7a5c; }
.ahp-metric-val.fail { color: #c0392b; }
.ahp-metric-sub {
    font-size: 10px;
    color: #a89880;
    margin-top: 7px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.5px;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #3d6b50 0%, #639478 100%) !important;
    color: #f0f9f3 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 3px !important;
    padding: 15px 0 !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(61, 107, 80, 0.25) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2c5040 0%, #4d7a60 100%) !important;
    box-shadow: 0 6px 22px rgba(61, 107, 80, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* Inputs */
div[data-testid="stNumberInput"] input {
    background: #fdfcf9 !important;
    border: 1px solid #ddd5c4 !important;
    border-radius: 8px !important;
    color: #2c3e30 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    text-align: center !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #639478 !important;
    box-shadow: 0 0 0 2px rgba(99, 148, 120, 0.15) !important;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid #e2d9cc !important;
}

.stCaption {
    color: #a89880 !important;
    font-size: 11px !important;
    font-family: 'DM Mono', monospace !important;
}

/* Sidebar inputs */
.stTextArea textarea {
    background: #fdfcf9 !important;
    border: 1px solid #ddd5c4 !important;
    border-radius: 8px !important;
    color: #2c3e30 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

/* Sidebar info box */
.ahp-sidebar-info {
    background: #edf4ef;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 8px 0 14px 0;
    border: 1px solid #b5d0bc;
}

/* Notice */
.ahp-notice {
    background: #f5f1ea;
    padding: 14px 18px;
    border-left: 3px solid #639478;
    border-radius: 0 10px 10px 0;
    font-size: 13px;
    color: #6b7c6e;
    line-height: 1.7;
}

/* Watermark paper texture overlay */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23noise)' opacity='0.025'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER ───────────────────────────
st.markdown("""
<style>
.ph-wrapper {
    position: relative;
    margin-top: -20px;
    margin-bottom: 30px;
    padding: 48px 40px 40px 40px;
    background: linear-gradient(180deg, rgba(237, 244, 239, 0.6) 0%, rgba(250, 248, 244, 0) 100%);
    border-bottom: 1px solid #ddd5c4;
    border-radius: 0 0 20px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    animation: headerDrop 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes headerDrop {
    0%  { opacity: 0; transform: translateY(-30px); }
    100%{ opacity: 1; transform: translateY(0); }
}

/* Decorative grid lines */
.ph-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,148,120,0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,148,120,0.07) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 0%, transparent 100%);
    pointer-events: none;
}

.ph-inner {
    display: flex;
    align-items: center;
    gap: 40px;
    position: relative;
    z-index: 2;
    max-width: 900px;
}

/* Logo */
.ph-logo-wrap {
    position: relative;
    flex-shrink: 0;
}
.ph-logo-ring {
    width: 100px; height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, #edf4ef 0%, #fdfcf9 100%);
    border: 2px solid #b5d0bc;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 6px 30px rgba(99,148,120,0.18), inset 0 1px 0 rgba(255,255,255,0.8);
    animation: floatRing 5s ease-in-out infinite;
}
.ph-logo-ring-outer {
    position: absolute; inset: -8px;
    border-radius: 50%;
    border: 1px dashed rgba(99,148,120,0.35);
    animation: spinSlow 25s linear infinite;
}
.ph-logo-ring-outer-2 {
    position: absolute; inset: -18px;
    border-radius: 50%;
    border: 1px solid rgba(201, 169, 110, 0.2);
    animation: spinSlow 40s linear infinite reverse;
}

@keyframes floatRing {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-8px); }
}
@keyframes spinSlow {
    to { transform: rotate(360deg); }
}

/* Text */
.ph-text { display: flex; flex-direction: column; }

.ph-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    color: #639478;
    background: #edf4ef;
    border: 1px solid #b5d0bc;
    padding: 4px 14px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 14px;
    width: fit-content;
    animation: badgePop 0.6s 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
@keyframes badgePop {
    from { opacity: 0; transform: scale(0.8); }
    to   { opacity: 1; transform: scale(1); }
}

.ph-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 700;
    line-height: 1;
    margin: 0 0 10px 0;
    color: #1e2d22;
    letter-spacing: -1px;
    position: relative;
}
.ph-title em {
    font-style: italic;
    color: #639478;
    background: linear-gradient(135deg, #639478, #c9a96e);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.ph-sub {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #a89880;
    text-transform: uppercase;
    letter-spacing: 4px;
    margin: 0;
    animation: fadeUp 0.7s 0.5s ease-out both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Decorative divider dots */
.ph-dots {
    display: flex; gap: 6px; align-items: center; margin-top: 14px;
}
.ph-dot {
    width: 5px; height: 5px; border-radius: 50%;
    background: #639478;
    animation: dotPulse 2s ease-in-out infinite;
}
.ph-dot:nth-child(2) { background: #c9a96e; animation-delay: 0.3s; }
.ph-dot:nth-child(3) { background: #a8c5b0; animation-delay: 0.6s; }
.ph-dot:nth-child(4) { width: 20px; height: 1px; border-radius: 2px; background: #ddd5c4; animation: none; }
.ph-dot:nth-child(5) { width: 8px; height: 1px; border-radius: 2px; background: #e8e0d0; animation: none; }
@keyframes dotPulse {
    0%, 100% { transform: scale(1); opacity: 0.7; }
    50%       { transform: scale(1.4); opacity: 1; }
}

@media (max-width: 768px) {
    .ph-inner { flex-direction: column; text-align: center; gap: 24px; }
    .ph-badge  { align-self: center; }
    .ph-title  { font-size: 36px; }
    .ph-dots   { justify-content: center; }
}
</style>

<div class="ph-wrapper">
  <div class="ph-inner">

    <div class="ph-logo-wrap">
      <div class="ph-logo-ring-outer-2"></div>
      <div class="ph-logo-ring-outer"></div>
      <div class="ph-logo-ring">
        <svg width="52" height="52" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="gTop" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#3d6b50"/>
              <stop offset="100%" stop-color="#639478"/>
            </linearGradient>
            <linearGradient id="gBot" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#639478"/>
              <stop offset="100%" stop-color="#c9a96e"/>
            </linearGradient>
          </defs>
          <!-- Hierarchy lines -->
          <line x1="50" y1="30" x2="22" y2="70" stroke="url(#gBot)" stroke-width="2.5" stroke-linecap="round" opacity="0.7">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s" repeatCount="indefinite" begin="0s"/>
          </line>
          <line x1="50" y1="30" x2="50" y2="70" stroke="url(#gBot)" stroke-width="2.5" stroke-linecap="round" opacity="0.7">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s" repeatCount="indefinite" begin="0.4s"/>
          </line>
          <line x1="50" y1="30" x2="78" y2="70" stroke="url(#gBot)" stroke-width="2.5" stroke-linecap="round" opacity="0.7">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2.5s" repeatCount="indefinite" begin="0.8s"/>
          </line>
          <!-- Top node -->
          <circle cx="50" cy="26" r="10" fill="url(#gTop)" opacity="0.95">
            <animate attributeName="r" values="9;11;9" dur="3s" repeatCount="indefinite"/>
          </circle>
          <circle cx="50" cy="26" r="4" fill="white" opacity="0.9"/>
          <!-- Bottom nodes -->
          <circle cx="22" cy="74" r="8" fill="url(#gBot)" opacity="0.85">
            <animate attributeName="r" values="7;9;7" dur="3s" repeatCount="indefinite" begin="0.5s"/>
          </circle>
          <circle cx="22" cy="74" r="3" fill="white" opacity="0.8"/>
          <circle cx="50" cy="74" r="8" fill="url(#gBot)" opacity="0.85">
            <animate attributeName="r" values="7;9;7" dur="3s" repeatCount="indefinite" begin="1s"/>
          </circle>
          <circle cx="50" cy="74" r="3" fill="white" opacity="0.8"/>
          <circle cx="78" cy="74" r="8" fill="url(#gBot)" opacity="0.85">
            <animate attributeName="r" values="7;9;7" dur="3s" repeatCount="indefinite" begin="1.5s"/>
          </circle>
          <circle cx="78" cy="74" r="3" fill="white" opacity="0.8"/>
        </svg>
      </div>
    </div>

    <div class="ph-text">
      <div class="ph-badge">Decision Support System</div>
      <h1 class="ph-title">AHP <em>Calculator</em></h1>
      <p class="ph-sub">Analytic Hierarchy Process &nbsp;·&nbsp; Multi-Criteria Analysis</p>
      <div class="ph-dots">
        <div class="ph-dot"></div>
        <div class="ph-dot"></div>
        <div class="ph-dot"></div>
        <div class="ph-dot"></div>
        <div class="ph-dot"></div>
      </div>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── SIDEBAR ───────────────────────────
st.sidebar.markdown("""
<div style="padding:20px 4px 4px 4px;">
  <div style="font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600;
  color:#1e2d22;margin-bottom:3px;">Configuration</div>
  <div style="font-size:11px;color:#a89880;margin-bottom:14px;font-family:'DM Mono',monospace;">
  AHP Model Setup</div>
  <div style="height:1px;background:linear-gradient(90deg,#b5d0bc,transparent);margin-bottom:14px;"></div>
</div>
""", unsafe_allow_html=True)

criteria_input = st.sidebar.text_area(
    "Criteria (comma-separated)",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo",
    help="Enter short names for your criteria"
)
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

st.sidebar.markdown(f"""
<div style="background:#edf4ef;border-radius:10px;padding:9px 14px;margin:8px 0 14px 0;
border:1px solid #b5d0bc;">
<span style="font-size:11px;color:#3d7a5c;font-family:'DM Mono',monospace;
font-weight:600;letter-spacing:0.5px;">n = {n} &nbsp;criteria detected</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 AHP Formulas")
for label, formula in [
    ("Step 1 · Normalize columns",      r"\bar{a}_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}}"),
    ("Step 2 · Average / Weight",       r"W_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}"),
    ("Step 3 · Criteria Weight",         r"CW_i = \frac{W_i}{n}"),
    ("Step 4 · Consistency Matrix",      r"CM_{ij} = a_{ij} \times CW_j"),
    ("Step 5 · Weighted Sum",            r"WS_i = \sum_{j=1}^{n} CM_{ij}"),
    ("Step 6 · Lambda Max",              r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{WS_i}{CW_i}"),
    ("Step 7 · CI",                      r"CI = \frac{\lambda_{max} - n}{n - 1}"),
    ("Step 8 · CR",                      r"CR = \frac{CI}{RI}"),
]:
    st.sidebar.markdown(f"**{label}**")
    st.sidebar.latex(formula)

st.sidebar.markdown("""
<div style="background:#edf4ef;border-left:2px solid #639478;border-radius:0 8px 8px 0;
padding:9px 14px;font-size:11px;color:#3d7a5c;font-family:'DM Mono',monospace;
margin-top:6px;letter-spacing:0.5px;">&#10003; Acceptable when CR &lt; 0.10</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

RI_dict = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,  5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
   11: 1.51,12: 1.48,13: 1.56,14: 1.57, 15: 1.59
}

st.sidebar.markdown("### 📊 Random Index (RI)")
ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n", "RI"])
st.sidebar.dataframe(ri_df, use_container_width=True, hide_index=True)
st.sidebar.markdown(f"""
<div style="background:#fdfcf9;border-radius:8px;padding:8px 12px;margin-top:6px;
font-size:11px;color:#a89880;font-family:'DM Mono',monospace;
border:1px solid #e2d9cc;letter-spacing:0.5px;">
n = {n} &nbsp;&#8594;&nbsp; RI = {RI_dict.get(n, 1.59)}</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔢 Saaty Scale")
saaty_df = pd.DataFrame({
    "Val":     [1,2,3,4,5,6,7,8,9],
    "Meaning": ["Equal","Weak","Moderate","Mod+","Strong",
                "Strong+","V.Strong","V.V.Strong","Extreme"],
    "1/x":     ["1/1","1/2","1/3","1/4","1/5","1/6","1/7","1/8","1/9"]
})
st.sidebar.dataframe(saaty_df, use_container_width=True, hide_index=True)

# ─────────────────────────── MATRIX INPUT ───────────────────────────
st.markdown("""
<div class="ahp-card">
  <div class="ahp-sec">
    <span class="ahp-sec-label">Pairwise Comparison Matrix</span>
    <span class="ahp-sec-badge">Step 01</span>
    <span class="ahp-sec-line"></span>
  </div>
  <div class="ahp-sec-sub">Upper triangle only &nbsp;·&nbsp; Diagonal fixed at 1 &nbsp;·&nbsp; Reciprocals auto-computed &nbsp;·&nbsp; Saaty scale 1–9</div>
""", unsafe_allow_html=True)

matrix = np.ones((n, n))

header_cols = st.columns([1.0] + [1] * n)
header_cols[0].write("")
for j in range(n):
    header_cols[j+1].markdown(
        f"<div class='ahp-row-label' style='text-align:center;color:#639478;border-bottom:1px solid #ddd5c4;padding-bottom:8px;margin-bottom:8px;'>{criteria[j]}</div>",
        unsafe_allow_html=True
    )

for i in range(n):
    cols = st.columns([1.0] + [1] * n)
    cols[0].markdown(
        f"<div class='ahp-row-label' style='margin-top:4px;'>{criteria[i]}</div>",
        unsafe_allow_html=True
    )
    for j in range(n):
        if i == j:
            cols[j+1].markdown("<div class='ahp-diag'>1</div>", unsafe_allow_html=True)
        elif j > i:
            val = cols[j+1].number_input(
                f"{criteria[i]} vs {criteria[j]}",
                min_value=0.111, max_value=9.0, value=1.0, step=0.5,
                key=f"m{i}-{j}", label_visibility="collapsed"
            )
            matrix[i][j] = val
            matrix[j][i] = round(1.0 / val, 6)
        else:
            recip = matrix[j][i]
            label = f"1/{round(recip)}" if recip >= 1 else f"{matrix[i][j]:.3f}"
            cols[j+1].markdown(f"<div class='ahp-recip'>{label}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── RUN ───────────────────────────
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if st.button("▶   RUN AHP ANALYSIS", use_container_width=True):

    # ══════ CORE CALCULATIONS ══════
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

    # TABLE 1
    card_open("Pairwise Comparison Matrix", "Table 1", "Raw input matrix with column sums")
    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria).round(4)
    df1.loc["Column Sum"] = col_sums.round(4)
    st.dataframe(df1, use_container_width=True)
    st.caption("Diagonal = 1  ·  Upper = inputs  ·  Lower = reciprocals  ·  Last row = column sums")
    card_close()

    # TABLE 2
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
    st.caption("Each cell = original ÷ column sum  ·  W = row mean  ·  CW = W ÷ n  ·  Column sums = 1.0")
    card_close()

    # TABLE 3
    card_open("Consistency Matrix", "Table 3", "Each cell = pairwise[i][j] × CW[j]")
    cw_row = pd.DataFrame([list(CW.round(3)) + [""]], columns=criteria + ["Weighted Sum"], index=["CW →"])
    st.dataframe(cw_row, use_container_width=True)
    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria).round(3)
    df3["Weighted Sum"] = weighted_sum.round(3)
    df3.loc["TOTAL"]    = df3.sum()
    st.dataframe(df3, use_container_width=True)
    st.caption("CW row = column weights used as multipliers  ·  Weighted Sum = row sum")
    card_close()

    # TABLE 4
    card_open("Consistency Summary", "Table 4", "Weighted sums, criteria weights and lambda values per criterion")
    df4 = pd.DataFrame({
        "Criteria":             criteria,
        "Weighted Sum (WS)":    weighted_sum.round(4),
        "Criteria Weight (CW)": CW.round(4),
        "WS / CW  (λ)":         wsv_over_cw.round(4),
    })
    total4 = pd.DataFrame([{
        "Criteria":             "TOTAL",
        "Weighted Sum (WS)":    round(weighted_sum.sum(), 4),
        "Criteria Weight (CW)": round(CW.sum(), 4),
        "WS / CW  (λ)":         round(wsv_over_cw.sum(), 4),
    }])
    df4 = pd.concat([df4, total4], ignore_index=True)
    st.dataframe(df4, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    cr_cls     = "ok"           if CR < 0.10 else "fail"
    cr_verdict = "Consistent"   if CR < 0.10 else "Inconsistent"
    for col, lbl, val, sub in [
        (m1, "λ max",       f"{lambda_max:.6f}", "Principal eigenvalue"),
        (m2, "CI",          f"{CI:.6f}",          "Consistency index"),
        (m3, f"RI  n={n}",  f"{RI}",              "Random index"),
        (m4, "CR",          f"{CR:.6f}",           cr_verdict),
    ]:
        extra_cls = f" {cr_cls}" if lbl == "CR" else ""
        with col:
            st.markdown(f"""
            <div class="ahp-metric">
              <div class="ahp-metric-label">{lbl}</div>
              <div class="ahp-metric-val{extra_cls}">{val}</div>
              <div class="ahp-metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    card_close()

    # TABLE 5
    card_open("GIS Priority Weights", "Table 5", "Ranked criteria weights ready for GIS weighted overlay analysis")
    sorted_idx = np.argsort(avg_weight)[::-1]
    df5 = pd.DataFrame({
        "Rank":             range(1, n+1),
        "Criteria":         [criteria[i]            for i in sorted_idx],
        "Avg / Weight (W)": [round(avg_weight[i],4) for i in sorted_idx],
        "Criteria CW":      [round(CW[i],4)         for i in sorted_idx],
        "CW %":             [float(CW_pct[i])       for i in sorted_idx],
    })
    st.dataframe(
        df5,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Avg / Weight (W)": st.column_config.NumberColumn(format="%.4f"),
            "Criteria CW": st.column_config.NumberColumn(format="%.4f"),
            "CW %": st.column_config.ProgressColumn(
                "CW %",
                help="Visual representation of criteria weight percentage",
                format="%.2f %%",
                min_value=0,
                max_value=100,
            )
        }
    )

    st.markdown("""
    <div style="background:#edf4ef;border:1px solid #b5d0bc;border-left:3px solid #639478;
    padding:14px 18px;border-radius:8px;margin-top:16px;">
        <div style="color:#3d6b50;font-family:'DM Mono',monospace;font-size:11px;font-weight:700;
        text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">🗺️ GIS Application Ready</div>
        <div style="color:#4a6b54;font-size:12px;line-height:1.6;">Input the <b>Criteria CW</b> values
        into your spatial analysis tool (e.g., ArcGIS Weighted Overlay, QGIS Raster Calculator) to
        generate your suitability map. Ensure all input raster layers are reclassified to a common
        scale before multiplying by these weights.</div>
    </div>
    """, unsafe_allow_html=True)

    card_close()

    # CHARTS
    card_open("Weight Visualization", "Charts", "Priority weight distribution across criteria")

    BG      = "#faf8f4"
    SURF    = "#fdfcf9"
    GREEN   = "#639478"
    GOLD    = "#c9a96e"
    MUT     = "#8a7f72"
    TXT     = "#1e2d22"

    palette = ["#639478","#3d6b50","#4d8f65","#8ab89a","#a8c5b0",
               "#c9a96e","#b08040","#d4b88a","#e8d4b0","#f0e6d0"]

    sorted_criteria = [criteria[i] for i in sorted_idx]
    sorted_cw       = [CW[i]       for i in sorted_idx]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4), facecolor=BG)
    fig.subplots_adjust(wspace=0.32)

    # Bar chart
    ax1 = axes[0]
    ax1.set_facecolor(SURF)
    for sp in ax1.spines.values():
        sp.set_color("#e2d9cc"); sp.set_linewidth(0.8)
    bc   = [palette[i % len(palette)] for i in range(len(sorted_cw))]
    bars = ax1.bar(sorted_criteria, sorted_cw, color=bc,
                   edgecolor=SURF, linewidth=1.2, width=0.54, zorder=3)
    ax1.set_title("Criteria Weight (CW)", color=TXT, fontsize=12, fontweight="bold",
                  pad=14, fontfamily="monospace", loc="left")
    ax1.set_xlabel("Criteria", color=MUT, fontsize=10, labelpad=9)
    ax1.set_ylabel("CW",       color=MUT, fontsize=10, labelpad=9)
    ax1.tick_params(colors=MUT, labelsize=9)
    ax1.grid(axis="y", color="#e8e0d4", linewidth=0.6, zorder=0)
    ax1.set_axisbelow(True)
    for bar, w in zip(bars, sorted_cw):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + max(sorted_cw)*0.018,
                 f"{w:.4f}", ha="center", va="bottom",
                 color=TXT, fontsize=9, fontweight="bold", fontfamily="monospace")

    # Pie chart
    ax2 = axes[1]
    ax2.set_facecolor(BG)
    wedges, texts, auts = ax2.pie(
        sorted_cw, labels=sorted_criteria, autopct="%1.1f%%",
        colors=palette[:len(sorted_cw)], startangle=140,
        pctdistance=0.74,
        textprops={"color": "#3a4a40", "fontsize": 10, "fontfamily": "monospace"},
        wedgeprops={"edgecolor": BG, "linewidth": 2.5}
    )
    for at in auts:
        at.set_color("#1e2d22")
        at.set_fontsize(9)
        at.set_fontweight("bold")
    ax2.set_title("CW Distribution", color=TXT, fontsize=12, fontweight="bold",
                  pad=14, fontfamily="monospace", loc="left")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    card_close()

    # RESULT
    card_open("Consistency Interpretation", "Result", "Saaty consistency check for your pairwise judgements")
    if CR < 0.10:
        st.success(f"CR = {CR:.6f} < 0.10 — Pairwise comparisons are **consistent**. Results are reliable.")
    else:
        st.error(f"CR = {CR:.6f} ≥ 0.10 — Pairwise comparisons are **inconsistent**. Please revise your matrix.")
        st.warning("Tip: Review judgments that violate transitivity (e.g., A > B, B > C but C > A).")

    st.markdown(f"""
| Parameter | Value | Formula |
|-----------|-------|---------|
| n | {n} | — |
| λ_max | {lambda_max:.6f} | mean(WS / CW) |
| CI | {CI:.6f} | (λ_max − n) / (n − 1) |
| RI | {RI} | Saaty table, n = {n} |
| CR | {CR:.6f} | CI / RI |
| Result | {"Consistent ✓" if CR < 0.10 else "Inconsistent ✗"} | CR {"<" if CR < 0.10 else "≥"} 0.10 |
""")
    card_close()

# ─────────────────────────── CREDITS ───────────────────────────
st.markdown("""
<style>

@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(99,148,120,0.25); }
    50%        { border-color: rgba(99,148,120,0.55); }
}
@keyframes floatCredit {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-4px); }
}
@keyframes orbitDot {
    from { transform: rotate(0deg) translateX(38px) rotate(0deg); }
    to   { transform: rotate(360deg) translateX(38px) rotate(-360deg); }
}
@keyframes fadeInFooter {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.pf-outer {
    margin-top: 60px;
    padding: 48px 36px;
    background: linear-gradient(145deg, #fdfcf9 0%, #f4f0e8 50%, #edf4ef 100%);
    border: 1px solid rgba(99,148,120,0.25);
    border-radius: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 4px 30px rgba(80, 60, 40, 0.08),
        0 1px 4px rgba(80, 60, 40, 0.04),
        inset 0 1px 0 rgba(255,255,255,0.9);
    animation: fadeInFooter 0.8s ease-out both, borderGlow 4s ease-in-out infinite;
}

/* Decorative corner motifs */
.pf-outer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #639478, #c9a96e, #8ab89a, #639478);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
}
.pf-outer::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,148,120,0.4), transparent);
}

/* Background watermark graphic */
.pf-bg-icon {
    position: absolute;
    right: -30px; bottom: -30px;
    width: 180px; height: 180px;
    opacity: 0.04;
    pointer-events: none;
}

/* Avatar ring */
.pf-avatar-wrap {
    display: inline-block;
    position: relative;
    margin-bottom: 20px;
    animation: floatCredit 5s ease-in-out infinite;
}
.pf-avatar {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #edf4ef 0%, #fdfcf9 100%);
    border: 2px solid rgba(99,148,120,0.4);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto;
    box-shadow: 0 4px 20px rgba(99,148,120,0.15), inset 0 1px 0 rgba(255,255,255,0.8);
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    color: #639478;
    font-weight: 700;
    font-style: italic;
}
/* Orbiting dot */
.pf-orbit {
    position: absolute;
    top: 50%; left: 50%;
    width: 8px; height: 8px;
    margin: -4px 0 0 -4px;
    border-radius: 50%;
    background: #c9a96e;
    animation: orbitDot 4s linear infinite;
    box-shadow: 0 0 6px rgba(201,169,110,0.6);
}

.pf-by {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #a89880;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
}
.pf-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 32px;
    font-weight: 700;
    color: #1e2d22;
    margin-bottom: 6px;
    letter-spacing: -0.3px;
    background: linear-gradient(135deg, #1e2d22 0%, #3d6b50 50%, #c9a96e 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
}
.pf-dept {
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #6b7c6e;
    margin-bottom: 4px;
}
.pf-univ {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #a89880;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 28px;
}
.pf-divider {
    display: flex; align-items: center; justify-content: center;
    gap: 10px; margin-bottom: 24px;
}
.pf-divider-line {
    height: 1px; width: 60px;
    background: linear-gradient(90deg, transparent, #ddd5c4, transparent);
}
.pf-divider-diamond {
    width: 6px; height: 6px;
    background: #639478; border-radius: 1px;
    transform: rotate(45deg);
}

.pf-links {
    display: flex; justify-content: center; gap: 14px; flex-wrap: wrap;
}
.pf-link {
    text-decoration: none !important;
    color: #3d6b50 !important;
    background: rgba(99,148,120,0.08);
    border: 1px solid rgba(99,148,120,0.3);
    padding: 10px 22px;
    border-radius: 30px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: inline-flex; align-items: center; gap: 8px;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(99,148,120,0.08);
}
.pf-link:hover {
    background: rgba(99,148,120,0.15);
    border-color: rgba(99,148,120,0.55);
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(99,148,120,0.18);
    color: #2c5040 !important;
}
.pf-link.gold {
    color: #7a5a20 !important;
    background: rgba(201,169,110,0.10);
    border-color: rgba(201,169,110,0.35);
}
.pf-link.gold:hover {
    background: rgba(201,169,110,0.18);
    border-color: rgba(201,169,110,0.6);
    color: #5c4010 !important;
    box-shadow: 0 6px 18px rgba(201,169,110,0.2);
}
</style>

<div class="pf-outer">

  <!-- Background watermark SVG -->
  <svg class="pf-bg-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" fill="none">
    <circle cx="50" cy="26" r="12" fill="#1e2d22"/>
    <line x1="50" y1="38" x2="22" y2="78" stroke="#1e2d22" stroke-width="3"/>
    <line x1="50" y1="38" x2="50" y2="78" stroke="#1e2d22" stroke-width="3"/>
    <line x1="50" y1="38" x2="78" y2="78" stroke="#1e2d22" stroke-width="3"/>
    <circle cx="22" cy="82" r="9" fill="#1e2d22"/>
    <circle cx="50" cy="82" r="9" fill="#1e2d22"/>
    <circle cx="78" cy="82" r="9" fill="#1e2d22"/>
  </svg>

  <div class="pf-avatar-wrap">
    <div class="pf-avatar">A</div>
    <div class="pf-orbit"></div>
  </div>

  <div class="pf-by">Designed &amp; Developed by</div>
  <div class="pf-name">Anindo Paul Sourav</div>
  <div class="pf-dept">Department of Geology and Mining</div>
  <div class="pf-univ">University of Barishal</div>

  <div class="pf-divider">
    <div class="pf-divider-line"></div>
    <div class="pf-divider-diamond"></div>
    <div class="pf-divider-line"></div>
  </div>

  <div class="pf-links">
    <a href="https://www.linkedin.com/in/anindo046/" target="_blank" class="pf-link">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
      </svg>
      LinkedIn
    </a>
    <a href="https://anindo46.github.io/portfolio/" target="_blank" class="pf-link gold">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="2" y1="12" x2="22" y2="12"></line>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
      </svg>
      Portfolio
    </a>
  </div>

</div>
""", unsafe_allow_html=True)
