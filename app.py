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
.ahp-metric-val.ok   { color: #2dd4bf; }
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
    50%       { opacity: 1;   transform: scale(1.3); }
}
@keyframes hexspin {
    to { transform: rotate(360deg); }
}
@keyframes lpulse {
    0%, 100% { opacity: 0.12; }
    50%       { opacity: 0.4;  }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER ───────────────────────────
st.markdown("""
<div style="background:#0c1420;border-bottom:1px solid #131f2e;
padding:32px 40px 28px 40px;margin-bottom:22px;
display:flex;align-items:center;gap:32px;">

  <div style="flex-shrink:0;">
    <svg width="80" height="80" viewBox="0 0 88 88" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <style>
          .h1{fill:none;stroke:#2dd4bf;stroke-width:1.3}
          .h2{fill:none;stroke:#0d9488;stroke-width:0.7;opacity:.35}
          .hr{fill:none;stroke:#2dd4bf;stroke-width:0.5}
          .hd{fill:#2dd4bf}
          .hl{stroke:#2dd4bf;stroke-width:0.9;opacity:.45;fill:none}
          .sp1{transform-origin:44px 38px;animation:hexspin 22s linear infinite}
          .sp2{transform-origin:44px 38px;animation:hexspin 13s linear infinite reverse}
          .pu{animation:lpulse 3.5s ease-in-out infinite}
        </style>
      </defs>
      <g class="sp1"><polygon class="h1" points="44,6 68,19 68,48 44,62 20,48 20,19"/></g>
      <g class="sp2"><polygon class="h2" points="44,2 72,17 72,52 44,68 16,52 16,17"/></g>
      <circle class="hr pu" cx="44" cy="35" r="22"/>
      <circle class="hr" cx="44" cy="35" r="14" style="animation:lpulse 3.5s 0.8s ease-in-out infinite"/>
      <line class="hl" x1="44" y1="10" x2="44" y2="54"/>
      <line class="hl" x1="22" y1="22" x2="66" y2="46"/>
      <line class="hl" x1="66" y1="22" x2="22" y2="46"/>
      <circle class="hd" cx="44" cy="10" r="2.8"/>
      <circle class="hd" cx="22" cy="22" r="2"/>
      <circle class="hd" cx="66" cy="22" r="2"/>
      <circle class="hd" cx="44" cy="35" r="4"/>
      <circle class="hd" cx="22" cy="46" r="2"/>
      <circle class="hd" cx="66" cy="46" r="2"/>
      <circle class="hd" cx="44" cy="54" r="2.8"/>
    </svg>
  </div>

  <div style="flex:1;">
    <div style="font-size:10px;font-weight:700;letter-spacing:4px;text-transform:uppercase;
    color:#2dd4bf;font-family:'JetBrains Mono',monospace;margin-bottom:8px;opacity:0.7;">
    Multi-Criteria Decision Analysis</div>

    <div style="font-size:40px;font-weight:700;color:#d4e4f0;letter-spacing:-1.5px;
    line-height:1.08;font-family:'Space Grotesk',sans-serif;">
    AHP&nbsp;<span style="color:#2dd4bf;">Calculator</span></div>

    <div style="font-size:13px;color:#2a3f55;font-weight:400;margin-top:9px;letter-spacing:0.3px;">
    Analytic Hierarchy Process &nbsp;·&nbsp; Pairwise Comparison &nbsp;·&nbsp; Consistency Analysis</div>

    <div style="display:flex;gap:8px;margin-top:14px;flex-wrap:wrap;">
      <span style="background:#2dd4bf10;border:1px solid #2dd4bf28;color:#2dd4bf;
      border-radius:20px;padding:3px 12px;font-size:10px;font-weight:600;
      font-family:'JetBrains Mono',monospace;letter-spacing:0.5px;">CR &lt; 0.10</span>
      <span style="background:#131f2e;color:#2a3f55;border-radius:20px;padding:3px 12px;
      font-size:10px;font-weight:500;font-family:'JetBrains Mono',monospace;">Up to n = 15</span>
      <span style="background:#131f2e;color:#2a3f55;border-radius:20px;padding:3px 12px;
      font-size:10px;font-weight:500;font-family:'JetBrains Mono',monospace;">Saaty Scale 1–9</span>
      <span style="background:#131f2e;color:#2a3f55;border-radius:20px;padding:3px 12px;
      font-size:10px;font-weight:500;font-family:'JetBrains Mono',monospace;">GIS Ready</span>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────── NOTICE ───────────────────────────
st.markdown("""
<div class="ahp-card">
  <div class="ahp-notice">
    <span style="color:#2dd4bf;font-weight:600;">How to use —</span>
    Enter your criteria names separated by commas in the sidebar.
    Fill only the <span style="color:#c8d8e8;font-weight:500;">upper-triangle</span> cells using the Saaty scale (1–9).
    The diagonal is fixed at 1 and lower-triangle reciprocals are computed automatically.
    A <span style="color:#c8d8e8;font-weight:500;">Consistency Ratio CR &lt; 0.10</span> confirms acceptable judgement consistency.
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
    ("Step 2 · Average / Weight",        r"W_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}"),
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

for i in range(n):
    cols = st.columns([1.0] + [1] * n)
    cols[0].markdown(
        f"<div class='ahp-row-label'>{criteria[i]}</div>",
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
        "Criteria CW":      [round(CW[i],4)          for i in sorted_idx],
        "CW %":             [f"{CW_pct[i]:.2f}%"    for i in sorted_idx],
    })
    st.dataframe(df5, use_container_width=True, hide_index=True)
    card_close()

    # CHARTS
    card_open("Weight Visualization", "Charts", "Priority weight distribution across criteria")

    BG   = "#060a0e"
    SURF = "#0c1420"
    TEAL = "#2dd4bf"
    MUT  = "#2a3f55"
    TXT  = "#6a8a9a"

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
    ax1.set_title("Criteria Weight (CW)", color=TXT, fontsize=10,
                  pad=12, fontfamily="monospace", loc="left")
    ax1.set_xlabel("Criteria", color=MUT, fontsize=9, labelpad=7)
    ax1.set_ylabel("CW",       color=MUT, fontsize=9, labelpad=7)
    ax1.tick_params(colors=MUT, labelsize=8)
    for sp in ax1.spines.values():
        sp.set_color("#131f2e"); sp.set_linewidth(0.5)
    ax1.grid(axis="y", color="#131f2e", linewidth=0.5, zorder=0)
    ax1.set_axisbelow(True)
    for bar, w in zip(bars, sorted_cw):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + max(sorted_cw)*0.018,
                 f"{w:.4f}", ha="center", va="bottom",
                 color=TEAL, fontsize=7.5, fontfamily="monospace")

    # Pie
    ax2 = axes[1]
    ax2.set_facecolor(BG)
    wedges, texts, auts = ax2.pie(
        sorted_cw, labels=sorted_criteria, autopct="%1.1f%%",
        colors=palette[:len(sorted_cw)], startangle=140,
        pctdistance=0.78,
        textprops={"color": TXT, "fontsize": 8, "fontfamily": "monospace"},
        wedgeprops={"edgecolor": BG, "linewidth": 2}
    )
    for at in auts:
        at.set_color("#c8d8e8"); at.set_fontsize(7.5)
    ax2.set_title("CW Distribution", color=TXT, fontsize=10,
                  pad=12, fontfamily="monospace", loc="left")

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
<div style="margin-top:64px;padding:40px 20px 30px;text-align:center;
border-top:1px solid #0d1824;">

  <!-- Decorative divider -->
  <div style="display:flex;align-items:center;gap:14px;justify-content:center;margin-bottom:34px;">
    <div style="height:1px;width:56px;background:linear-gradient(90deg,transparent,#2dd4bf35);"></div>
    <svg width="18" height="18" viewBox="0 0 88 88" xmlns="http://www.w3.org/2000/svg">
      <polygon points="44,6 70,21 70,51 44,66 18,51 18,21"
               fill="none" stroke="#2dd4bf" stroke-width="2.5" opacity="0.4">
        <animateTransform attributeName="transform" type="rotate"
          from="0 44 44" to="360 44 44" dur="9s" repeatCount="indefinite"/>
      </polygon>
      <circle cx="44" cy="37" r="5" fill="#2dd4bf" opacity="0.55"/>
    </svg>
    <div style="height:1px;width:56px;background:linear-gradient(90deg,#2dd4bf35,transparent);"></div>
  </div>

  <!-- Credit card -->
  <div style="position:relative;width:300px;height:190px;margin:0 auto 26px auto;
  background:#0c1420;border-radius:18px;
  box-shadow:0 8px 36px rgba(0,0,0,0.4),0 0 0 1px #162030;overflow:hidden;">

    <div style="position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,transparent,#2dd4bf28,transparent);"></div>
    <div style="position:absolute;width:160px;height:160px;
    background:radial-gradient(circle,#2dd4bf08,transparent);top:-50px;right:-50px;border-radius:50%;"></div>

    <div style="position:absolute;inset:0;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:4px;padding:20px;">

      <div style="font-size:9px;letter-spacing:4px;text-transform:uppercase;
      color:#2dd4bf;font-family:'JetBrains Mono',monospace;font-weight:700;opacity:0;
      animation:slideUp 0.55s 0.15s ease both;">Created by</div>

      <div style="font-size:25px;font-weight:700;color:#d4e4f0;letter-spacing:-0.5px;
      font-family:'Space Grotesk',sans-serif;opacity:0;
      animation:slideUp 0.55s 0.30s ease both;">Anindo Paul</div>

      <div style="font-size:20px;font-weight:300;color:#2dd4bf;letter-spacing:2px;
      font-family:'Space Grotesk',sans-serif;opacity:0;
      animation:slideUp 0.55s 0.44s ease both;">Sourav</div>

      <div style="height:1px;width:50px;background:linear-gradient(90deg,transparent,#2dd4bf40,transparent);
      margin:5px 0;opacity:0;animation:slideUp 0.55s 0.57s ease both;"></div>

      <div style="font-size:10px;color:#2a3f55;font-family:'JetBrains Mono',monospace;
      letter-spacing:2px;text-transform:uppercase;opacity:0;
      animation:slideUp 0.55s 0.70s ease both;">AHP Calculator</div>

      <div style="font-size:10px;color:#162030;font-family:'JetBrains Mono',monospace;
      letter-spacing:1px;opacity:0;animation:slideUp 0.55s 0.82s ease both;">
      Free for all users &nbsp;·&nbsp; 2025</div>

    </div>
  </div>

  <!-- Pulsing dots -->
  <div style="display:flex;justify-content:center;gap:7px;margin-bottom:24px;">
    <div style="width:5px;height:5px;border-radius:50%;background:#2dd4bf;
    animation:pdot 1.5s 0.0s ease-in-out infinite;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#2dd4bf;
    animation:pdot 1.5s 0.2s ease-in-out infinite;"></div>
    <div style="width:5px;height:5px;border-radius:50%;background:#2dd4bf;
    animation:pdot 1.5s 0.4s ease-in-out infinite;"></div>
  </div>

  <!-- Links -->
  <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
    <a href="https://www.linkedin.com/in/anindo046/" target="_blank"
    style="display:inline-flex;align-items:center;gap:6px;background:#061510;
    border:1px solid #2dd4bf1e;border-radius:20px;padding:7px 16px;
    font-size:11px;color:#2dd4bf;font-weight:600;text-decoration:none;
    font-family:'Space Grotesk',sans-serif;letter-spacing:0.3px;">
    &#128279; LinkedIn</a>
    <a href="https://anindo46.github.io/portfolio/" target="_blank"
    style="display:inline-flex;align-items:center;gap:6px;background:#090e16;
    border:1px solid #131f2e;border-radius:20px;padding:7px 16px;
    font-size:11px;color:#2a3f55;font-weight:600;text-decoration:none;
    font-family:'Space Grotesk',sans-serif;letter-spacing:0.3px;">
    &#127760; Portfolio</a>
  </div>

  <div style="font-size:10px;color:#0d1824;font-family:'JetBrains Mono',monospace;
  letter-spacing:1.5px;padding-bottom:10px;text-transform:uppercase;">
  Analytic Hierarchy Process &nbsp;·&nbsp; Open Source &nbsp;·&nbsp; 2025
  </div>

</div>
""", unsafe_allow_html=True)
