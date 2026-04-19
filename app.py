import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="AHP Calculator", layout="wide")

# ─────────────────────────── STYLE ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp { background: #060a0e; }

section[data-testid="stSidebar"] {
    background: #080d12 !important;
    border-right: 1px solid #131f2e !important;
}
section[data-testid="stSidebar"] * { font-family: 'Space Grotesk', sans-serif !important; }

.main .block-container { padding-top: 0 !important; }

/* Cards */
.ahp-card {
    background: #0c1420;
    padding: 26px 30px;
    border-radius: 16px;
    border: 1px solid #162030;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
}
.ahp-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent 0%, #2dd4bf30 50%, transparent 100%);
}

/* Section headers */
.ahp-sec {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.ahp-sec-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2dd4bf;
    font-family: 'JetBrains Mono', monospace;
}
.ahp-sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #162030 0%, transparent 100%);
}
.ahp-sec-badge {
    font-size: 9px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    color: #2dd4bf;
    background: #2dd4bf12;
    border: 1px solid #2dd4bf25;
    border-radius: 20px;
    padding: 2px 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.ahp-sec-sub {
    font-size: 12px;
    color: #2a3f55;
    margin-bottom: 16px;
    font-weight: 400;
    letter-spacing: 0.2px;
}

/* Notice */
.ahp-notice {
    background: #061510;
    padding: 14px 18px;
    border-left: 2px solid #2dd4bf;
    border-radius: 0 10px 10px 0;
    font-size: 13px;
    color: #64748b;
    line-height: 1.7;
}

/* Diagonal / reciprocal cells */
.ahp-diag {
    text-align: center;
    padding: 7px 4px;
    background: #2dd4bf0e;
    border-radius: 7px;
    color: #2dd4bf;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    border: 1px solid #2dd4bf1e;
}
.ahp-recip {
    text-align: center;
    padding: 7px 4px;
    color: #243040;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.ahp-row-label {
    padding: 8px 4px;
    color: #4a6070;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* Metric boxes */
.ahp-metric {
    background: #090e16;
    border-radius: 14px;
    border: 1px solid #131f2e;
    padding: 20px 14px;
    text-align: center;
}
.ahp-metric-label {
    font-size: 9px;
    color: #2a3f55;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 10px;
}
.ahp-metric-val {
    font-size: 20px;
    font-weight: 700;
    color: #c8d8e8;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.5px;
}
.ahp-metric-val.ok    { color: #2dd4bf; }
.ahp-metric-val.fail { color: #f87171; }
.ahp-metric-sub {
    font-size: 10px;
    color: #2a3f55;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
}

/* Button */
.stButton > button {
    background: #0f4a45 !important;
    color: #a7f3d0 !important;
    border: 1px solid #2dd4bf30 !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 3px !important;
    padding: 15px 0 !important;
    text-transform: uppercase !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #134e48 !important;
    border-color: #2dd4bf55 !important;
    color: #ccfbf1 !important;
}

/* Inputs */
div[data-testid="stNumberInput"] input {
    background: #090e16 !important;
    border: 1px solid #131f2e !important;
    border-radius: 8px !important;
    color: #c8d8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    text-align: center !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #2dd4bf50 !important;
    box-shadow: 0 0 0 2px #2dd4bf0e !important;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid #131f2e !important;
}

.stCaption {
    color: #1e2d3d !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Credits */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pdot {
    0%, 100% { opacity: 0.15; transform: scale(0.8); }
    50%        { opacity: 1;   transform: scale(1.3); }
}
@keyframes hexspin {
    to { transform: rotate(360deg); }
}
@keyframes lpulse {
    0%, 100% { opacity: 0.12; }
    50%        { opacity: 0.4;  }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER ───────────────────────────
st.markdown("""
<style>
.premium-header-wrapper {
    position: relative;
    margin-top: -20px;
    margin-bottom: 25px;
    padding: 40px 30px;
    background: linear-gradient(180deg, rgba(12, 20, 32, 0.8) 0%, rgba(6, 10, 14, 0) 100%);
    border-bottom: 1px solid rgba(45, 212, 191, 0.1);
    border-radius: 0 0 24px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    animation: fadeSlideDown 0.8s ease-out forwards;
}
.header-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse at center, rgba(45, 212, 191, 0.08) 0%, transparent 60%);
    transform: translate(-50%, -50%);
    pointer-events: none;
    animation: pulseGlow 6s ease-in-out infinite alternate;
}
.header-content {
    display: flex;
    align-items: center;
    gap: 35px;
    position: relative;
    z-index: 2;
}
.header-icon-box {
    width: 110px;
    height: 110px;
    background: rgba(12, 20, 32, 0.5);
    border: 1px solid rgba(45, 212, 191, 0.2);
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(45, 212, 191, 0.05);
    backdrop-filter: blur(10px);
    animation: floatIcon 4s ease-in-out infinite;
}
.header-text-box {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.ph-badge {
    align-self: flex-start;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #2dd4bf;
    background: rgba(45, 212, 191, 0.1);
    border: 1px solid rgba(45, 212, 191, 0.25);
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}
.ph-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 800;
    margin: 0;
    line-height: 1.1;
    background: linear-gradient(90deg, #ffffff, #2dd4bf, #80cbc4, #ffffff);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    animation: gradientTextShine 4s linear infinite;
    letter-spacing: -1px;
}
.ph-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #6a8a9a;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin: 8px 0 0 0;
    font-weight: 500;
}
@keyframes fadeSlideDown { 0% { opacity: 0; transform: translateY(-30px); } 100% { opacity: 1; transform: translateY(0); } }
@keyframes floatIcon { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-8px) rotate(2deg); } }
@keyframes pulseGlow { 0% { opacity: 0.5; transform: translate(-50%, -50%) scale(0.9); } 100% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); } }
@keyframes gradientTextShine { to { background-position: 200% center; } }
.svg-node { transform-origin: center; animation: pulseNode 2s infinite alternate; }
.svg-line { stroke-dasharray: 60; stroke-dashoffset: 60; animation: drawLine 3s ease-in-out infinite alternate; }
@keyframes pulseNode { 0% { filter: drop-shadow(0 0 2px #2dd4bf); transform: scale(1); } 100% { filter: drop-shadow(0 0 8px #2dd4bf); transform: scale(1.15); } }
@keyframes drawLine { 0% { stroke-dashoffset: 60; } 100% { stroke-dashoffset: 0; } }
@media (max-width: 768px) { .header-content { flex-direction: column; text-align: center; gap: 20px; } .ph-badge { align-self: center; } .ph-title { font-size: 32px; } }
</style>

<div class="premium-header-wrapper">
<div class="header-glow"></div>
<div class="header-content">
<div class="header-icon-box">
<svg width="65" height="65" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="lineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#2dd4bf" stop-opacity="0.8"/>
<stop offset="100%" stop-color="#0284c7" stop-opacity="0.2"/>
</linearGradient>
</defs>
<path d="M 50 25 L 20 70" stroke="url(#lineGrad)" stroke-width="3" stroke-linecap="round" fill="none" class="svg-line" style="animation-delay: 0s;"/>
<path d="M 50 25 L 50 70" stroke="url(#lineGrad)" stroke-width="3" stroke-linecap="round" fill="none" class="svg-line" style="animation-delay: 0.2s;"/>
<path d="M 50 25 L 80 70" stroke="url(#lineGrad)" stroke-width="3" stroke-linecap="round" fill="none" class="svg-line" style="animation-delay: 0.4s;"/>
<circle cx="50" cy="22" r="9" fill="#a7f3d0" class="svg-node" style="animation-delay: 0s;"/>
<circle cx="50" cy="22" r="4" fill="#060a0e" />
<circle cx="20" cy="73" r="7" fill="#2dd4bf" class="svg-node" style="animation-delay: 0.5s;"/>
<circle cx="20" cy="73" r="3" fill="#060a0e" />
<circle cx="50" cy="73" r="7" fill="#2dd4bf" class="svg-node" style="animation-delay: 0.7s;"/>
<circle cx="50" cy="73" r="3" fill="#060a0e" />
<circle cx="80" cy="73" r="7" fill="#2dd4bf" class="svg-node" style="animation-delay: 0.9s;"/>
<circle cx="80" cy="73" r="3" fill="#060a0e" />
</svg>
</div>
<div class="header-text-box">
<div class="ph-badge">Decision Support System</div>
<h1 class="ph-title">AHP CALCULATOR</h1>
<p class="ph-subtitle">Analytic Hierarchy Process</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── SIDEBAR ───────────────────────────
st.sidebar.markdown("""
<div style="padding:20px 4px 4px 4px;">
  <div style="font-size:17px;font-weight:700;color:#c8d8e8;letter-spacing:-0.3px;
  font-family:'Space Grotesk',sans-serif;margin-bottom:3px;">Settings</div>
  <div style="font-size:11px;color:#2a3f55;margin-bottom:14px;font-family:'JetBrains Mono',monospace;">
  Configure your AHP model</div>
  <div style="height:1px;background:#131f2e;margin-bottom:14px;"></div>
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
<div style="background:#061510;border-radius:10px;padding:9px 14px;margin:8px 0 14px 0;
border:1px solid #2dd4bf18;">
<span style="font-size:11px;color:#2dd4bf;font-family:'JetBrains Mono',monospace;
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
<div style="background:#061510;border-left:2px solid #2dd4bf;border-radius:0 8px 8px 0;
padding:9px 14px;font-size:11px;color:#2dd4bf;font-family:'JetBrains Mono',monospace;
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
<div style="background:#090e16;border-radius:8px;padding:8px 12px;margin-top:6px;
font-size:11px;color:#2a3f55;font-family:'JetBrains Mono',monospace;
border:1px solid #131f2e;letter-spacing:0.5px;">
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
    <span class="ahp-sec-label">Pairwise Comparison Input</span>
    <span class="ahp-sec-badge">Step 1</span>
    <span class="ahp-sec-line"></span>
  </div>
  <div class="ahp-sec-sub">Upper triangle only &nbsp;·&nbsp; Diagonal fixed at 1 &nbsp;·&nbsp; Reciprocals auto-computed &nbsp;·&nbsp; Saaty scale 1–9</div>
""", unsafe_allow_html=True)

matrix = np.ones((n, n))

# --- ADDED: Column Header Row ---
header_cols = st.columns([1.0] + [1] * n)
header_cols[0].write("") # Empty top-left corner
for j in range(n):
    header_cols[j+1].markdown(
        f"<div class='ahp-row-label' style='text-align:center; color:#2dd4bf; border-bottom:1px solid #131f2e; padding-bottom:8px; margin-bottom:8px;'>{criteria[j]}</div>",
        unsafe_allow_html=True
    )
# --------------------------------

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
    <div style="background:#061510; border:1px solid #131f2e; border-left:3px solid #2dd4bf; padding:14px 18px; border-radius:8px; margin-top:16px;">
        <div style="color:#2dd4bf; font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">🗺️ GIS Application Ready</div>
        <div style="color:#8a9fae; font-size:12px; line-height:1.6;">Input the <b style="color:#c8d8e8;">Criteria CW</b> values into your spatial analysis tool (e.g., ArcGIS Weighted Overlay, QGIS Raster Calculator) to generate your suitability map. Ensure all input raster layers are reclassified to a common scale before multiplying by these weights.</div>
    </div>
    """, unsafe_allow_html=True)
    
    card_close()

    # CHARTS (Consolidated single block to prevent duplication)
    card_open("Weight Visualization", "Charts", "Priority weight distribution across criteria")

    BG   = "#060a0e"
    SURF = "#0c1420"
    TEAL = "#2dd4bf"
    MUT  = "#4a6070"  # Slightly brightened muted text
    TXT  = "#a7f3d0"  # Brighter text for chart titles

    palette = ["#2dd4bf","#0d9488","#0f766e","#134e4a","#115e59",
               "#1d9488","#14b8a6","#5eead4","#99f6e4","#ccfbf1"]

    sorted_criteria = [criteria[i] for i in sorted_idx]
    sorted_cw       = [CW[i]       for i in sorted_idx]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), facecolor=BG)
    fig.subplots_adjust(wspace=0.32)

    # Bar
    ax1 = axes[0]
    ax1.set_facecolor(SURF)
    bc = [palette[i % len(palette)] for i in range(len(sorted_cw))]
    bars = ax1.bar(sorted_criteria, sorted_cw, color=bc,
                   edgecolor=BG, linewidth=1.4, width=0.56, zorder=3)
    ax1.set_title("Criteria Weight (CW)", color=TXT, fontsize=11, fontweight="bold",
                  pad=15, fontfamily="monospace", loc="left")
    ax1.set_xlabel("Criteria", color=MUT, fontsize=10, labelpad=9)
    ax1.set_ylabel("CW",       color=MUT, fontsize=10, labelpad=9)
    ax1.tick_params(colors=MUT, labelsize=9)
    for sp in ax1.spines.values():
        sp.set_color("#131f2e"); sp.set_linewidth(0.5)
    ax1.grid(axis="y", color="#131f2e", linewidth=0.5, zorder=0)
    ax1.set_axisbelow(True)
    
    # Enhanced Bar chart text (bold and bright)
    for bar, w in zip(bars, sorted_cw):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + max(sorted_cw)*0.018,
                 f"{w:.4f}", ha="center", va="bottom",
                 color="#ffffff", fontsize=9, fontweight="bold", fontfamily="monospace")

    # Pie
    ax2 = axes[1]
    ax2.set_facecolor(BG)
    wedges, texts, auts = ax2.pie(
        sorted_cw, labels=sorted_criteria, autopct="%1.1f%%",
        colors=palette[:len(sorted_cw)], startangle=140,
        pctdistance=0.74, # Brought percentages slightly closer to center
        # Enhanced Pie chart external labels
        textprops={"color": "#e2e8f0", "fontsize": 10, "fontweight": "500", "fontfamily": "monospace"},
        wedgeprops={"edgecolor": BG, "linewidth": 2.5}
    )
    
    # Enhanced Pie chart internal percentages (bold white)
    for at in auts:
        at.set_color("#ffffff")
        at.set_fontsize(9.5)
        at.set_fontweight("bold")
        
    ax2.set_title("CW Distribution", color=TXT, fontsize=11, fontweight="bold",
                  pad=15, fontfamily="monospace", loc="left")

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

# ─────────────────────────── ANIMATED CREDITS ───────────────────────────
st.markdown("""
<style>
.premium-footer {
    margin-top: 50px;
    padding: 30px 20px;
    background: linear-gradient(145deg, rgba(12, 20, 32, 0.8) 0%, rgba(6, 10, 14, 0.95) 100%);
    border: 1px solid rgba(45, 212, 191, 0.15);
    border-radius: 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    animation: floatUp 1s ease-out forwards;
}

.premium-footer::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(45,212,191,0.05) 0%, transparent 60%);
    animation: slowSpin 15s linear infinite;
    pointer-events: none;
}

.pf-label {
    font-size: 10px;
    color: #4a6070;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

.pf-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(90deg, #2dd4bf, #80cbc4, #2dd4bf);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    animation: shine 3s linear infinite;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}

.pf-info {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    color: #6a8a9a;
    margin-bottom: 22px;
    letter-spacing: 0.2px;
}

.pf-info span {
    color: #2dd4bf;
    opacity: 0.7;
}

.pf-links {
    display: flex;
    justify-content: center;
    gap: 15px;
    position: relative;
    z-index: 2;
}

.pf-link {
    text-decoration: none !important;
    color: #a7f3d0 !important;
    background: rgba(45, 212, 191, 0.05);
    border: 1px solid rgba(45, 212, 191, 0.2);
    padding: 10px 20px;
    border-radius: 30px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.pf-link:hover {
    background: rgba(45, 212, 191, 0.15);
    border-color: rgba(45, 212, 191, 0.5);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(45, 212, 191, 0.15);
    color: #ffffff !important;
}

@keyframes shine {
    to { background-position: 200% center; }
}
@keyframes floatUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes slowSpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<div class="premium-footer">
    <div class="pf-label">Designed & Developed By</div>
    <div class="pf-name">Anindo Paul Sourav</div>
    <div class="pf-info">
        Geology and Mining <span>•</span> University of Barishal
    </div>
    <div class="pf-links">
        <a href="https://www.linkedin.com/in/anindo046/" target="_blank" class="pf-link">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            LinkedIn
        </a>
        <a href="https://anindo46.github.io/portfolio/" target="_blank" class="pf-link">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
            Portfolio
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
