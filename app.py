import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="AHP Calculator", layout="wide")

# ─────────────────────────── PREMIUM STYLE ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Base ── */
.stApp {
    background: #080c10;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0b0f14 !important;
    border-right: 1px solid #1a2332 !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── Cards ── */
.card {
    background: linear-gradient(135deg, #0e1520 0%, #0a1018 100%);
    padding: 28px 32px;
    border-radius: 16px;
    border: 1px solid #1e2d42;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2dd4bf44, transparent);
}

/* ── Section titles ── */
.section-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #2dd4bf;
    margin-bottom: 18px;
    font-family: 'JetBrains Mono', monospace;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3a4a, transparent);
}

/* ── Notice banner ── */
.notice {
    background: #071a14;
    padding: 16px 20px;
    border-left: 3px solid #2dd4bf;
    border-radius: 0 10px 10px 0;
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.6;
}
.notice b { color: #e2e8f0; }

/* ── Metric boxes ── */
.metric-box {
    background: #0b1520;
    border-radius: 14px;
    border: 1px solid #1e2d42;
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-box::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, #2dd4bf08, transparent);
}
.metric-label {
    font-size: 10px;
    color: #475569;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 22px;
    font-weight: 700;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.5px;
}
.metric-value.cr-ok   { color: #2dd4bf; }
.metric-value.cr-fail { color: #f87171; }
.metric-verdict {
    font-size: 11px;
    color: #475569;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #134e4a, #0f766e) !important;
    color: #ccfbf1 !important;
    border: 1px solid #2dd4bf44 !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    padding: 14px 0 !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    border-color: #2dd4bf88 !important;
    transform: translateY(-1px) !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #1e2d42 !important;
}

/* ── Number inputs ── */
div[data-testid="stNumberInput"] input {
    background: #0b1520 !important;
    border: 1px solid #1e2d42 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    text-align: center !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #2dd4bf66 !important;
    box-shadow: 0 0 0 2px #2dd4bf11 !important;
}

/* ── Caption ── */
.stCaption {
    color: #334155 !important;
    font-size: 11px !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.5px !important;
}

/* ── Sidebar text ── */
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    border-bottom: 1px solid #1e2d42;
    padding-bottom: 6px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 40px 20px;
    margin-top: 50px;
    color: #1e2d42;
    font-size: 12px;
    border-top: 1px solid #0f1f2e;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
}
.footer a { color: #2dd4bf; text-decoration: none; opacity: 0.7; }
.footer a:hover { opacity: 1; }

/* ── Diagonal cell ── */
.diag-cell {
    text-align: center;
    padding: 6px 4px;
    background: #2dd4bf0d;
    border-radius: 6px;
    color: #2dd4bf;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    border: 1px solid #2dd4bf22;
}
.recip-cell {
    text-align: center;
    padding: 6px 4px;
    color: #334155;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

/* ── Tag badge ── */
.tag {
    display: inline-block;
    background: #2dd4bf11;
    border: 1px solid #2dd4bf33;
    color: #2dd4bf;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-left: 8px;
    vertical-align: middle;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2d42, transparent);
    margin: 8px 0 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER / LOGO ───────────────────────────
st.markdown("""
<div style="display:flex;justify-content:center;padding:30px 0 10px 0;">
<svg width="700" viewBox="0 0 700 120" xmlns="http://www.w3.org/2000/svg">
<defs><style>
.hex{fill:none;stroke:#2dd4bf;stroke-width:1.2}
.hex2{fill:none;stroke:#0d9488;stroke-width:0.7;opacity:.45}
.ring{fill:none;stroke:#2dd4bf;stroke-width:0.5;opacity:.25}
.dot{fill:#2dd4bf}
.ln{stroke:#2dd4bf;stroke-width:0.9;opacity:.5;fill:none}
.s1{transform-origin:56px 44px;animation:spin 22s linear infinite}
.s2{transform-origin:56px 44px;animation:spin 13s linear infinite reverse}
.pu{animation:pulse 3.5s ease-in-out infinite}
.fi{animation:fadein 1.4s cubic-bezier(.16,1,.3,1) both}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:.2}50%{opacity:.55}}
@keyframes fadein{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
</style></defs>
<g class="fi">
  <g class="s1"><polygon class="hex" points="56,7 79,19 79,44 56,57 33,44 33,19"/></g>
  <g class="s2"><polygon class="hex2" points="56,1 84,17 84,52 56,68 28,52 28,17"/></g>
  <circle class="ring pu" cx="56" cy="32" r="24"/>
  <circle class="ring" cx="56" cy="32" r="16" style="animation-delay:.8s"/>
  <line class="ln" x1="56" y1="11" x2="56" y2="53"/>
  <line class="ln" x1="36" y1="21" x2="76" y2="43"/>
  <line class="ln" x1="76" y1="21" x2="36" y2="43"/>
  <circle class="dot" cx="56" cy="11" r="2.5"/>
  <circle class="dot" cx="36" cy="21" r="1.8"/>
  <circle class="dot" cx="76" cy="21" r="1.8"/>
  <circle class="dot" cx="56" cy="32" r="3.8"/>
  <circle class="dot" cx="36" cy="43" r="1.8"/>
  <circle class="dot" cx="76" cy="43" r="1.8"/>
  <circle class="dot" cx="56" cy="53" r="2.5"/>

  <text x="105" y="42" font-family="Space Grotesk,sans-serif" font-size="40" font-weight="700" letter-spacing="-1" fill="#e2e8f0">AHP</text>
  <text x="107" y="67" font-family="Space Grotesk,sans-serif" font-size="22" font-weight="300" letter-spacing="8" fill="#2dd4bf">CALCULATOR</text>
  <text x="109" y="88" font-family="JetBrains Mono,monospace" font-size="10" letter-spacing="5" fill="#334155">ANALYTIC HIERARCHY PROCESS</text>

  <line x1="105" y1="76" x2="420" y2="76" stroke="#1e2d42" stroke-width="0.5"/>
</g>
</svg>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── NOTICE ───────────────────────────
st.markdown("""
<div class='card' style='margin-bottom:28px'>
<div class='notice'>
<b>Instructions —</b> Enter criteria names separated by commas. Fill the upper-triangle cells using the Saaty scale (1–9).
The diagonal is fixed at 1 and lower-triangle reciprocals are computed automatically.
A <b>Consistency Ratio CR &lt; 0.10</b> confirms acceptable judgement consistency.
</div></div>
""", unsafe_allow_html=True)

# ─────────────────────────── SIDEBAR ───────────────────────────
st.sidebar.markdown("""
<div style='padding:18px 4px 4px 4px;'>
<div style='font-size:10px;letter-spacing:3px;text-transform:uppercase;
color:#2dd4bf;font-family:JetBrains Mono,monospace;border-bottom:1px solid #1e2d42;
padding-bottom:10px;margin-bottom:16px;'>⚙ Configuration</div>
</div>
""", unsafe_allow_html=True)

criteria_input = st.sidebar.text_area(
    "Criteria (comma-separated)",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo",
    help="Enter short names for your criteria"
)
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### 📐 AHP Formulas")

st.sidebar.markdown("**Step 1 · Normalize Each Column**")
st.sidebar.latex(r"\bar{a}_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}}")
st.sidebar.markdown("**Step 2 · Average / Weight (Priority Vector)**")
st.sidebar.latex(r"W_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}")
st.sidebar.markdown("**Step 3 · Criteria Weight (CW)**")
st.sidebar.latex(r"CW_i = \frac{W_i}{n}")
st.sidebar.markdown("**Step 4 · Consistency Matrix Cell**")
st.sidebar.latex(r"CM_{ij} = a_{ij} \times CW_j")
st.sidebar.markdown("**Step 5 · Weighted Sum Vector**")
st.sidebar.latex(r"WS_i = \sum_{j=1}^{n} CM_{ij}")
st.sidebar.markdown("**Step 6 · Lambda Max**")
st.sidebar.latex(r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{WS_i}{CW_i}")
st.sidebar.markdown("**Step 7 · Consistency Index**")
st.sidebar.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")
st.sidebar.markdown("**Step 8 · Consistency Ratio**")
st.sidebar.latex(r"CR = \frac{CI}{RI}")
st.sidebar.markdown("""<div style='background:#071a14;border-left:3px solid #2dd4bf;
border-radius:0 8px 8px 0;padding:10px 14px;font-size:12px;color:#2dd4bf;
font-family:JetBrains Mono,monospace;margin-top:8px;'>
✓ Acceptable when CR &lt; 0.10</div>""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

RI_dict = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,  5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
   11: 1.51,12: 1.48,13: 1.56,14: 1.57, 15: 1.59
}
st.sidebar.markdown("### 📊 Random Index (RI) Table")
ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n", "RI"])
st.sidebar.dataframe(ri_df, use_container_width=True, hide_index=True)
st.sidebar.markdown(f"""<div style='font-size:11px;color:#2dd4bf;font-family:JetBrains Mono,monospace;
padding:8px 12px;background:#071a14;border-radius:8px;border:1px solid #1e2d42;margin-top:6px;'>
n = {n}  →  RI = {RI_dict.get(n, 1.59)}</div>""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### 🔢 Saaty Scale")
saaty_df = pd.DataFrame({
    "Value":      [1,2,3,4,5,6,7,8,9],
    "Meaning":    ["Equal","Weak/Slight","Moderate","Mod. plus","Strong",
                   "Strong plus","Very strong","Very very","Extreme"],
    "1/x":        ["1/1","1/2","1/3","1/4","1/5","1/6","1/7","1/8","1/9"]
})
st.sidebar.dataframe(saaty_df, use_container_width=True, hide_index=True)

# ─────────────────────────── MATRIX INPUT ───────────────────────────
st.markdown("""
<div class='card'>
<div class='section-title'>Pairwise Comparison Matrix Input<span class='tag'>Step 1</span></div>
<p style='color:#475569;font-size:13px;margin:-6px 0 16px 0;'>
Fill upper triangle only · Diagonal = 1 · Reciprocals auto-filled · Saaty scale 1–9
</p>
""", unsafe_allow_html=True)

matrix = np.ones((n, n))

for i in range(n):
    cols = st.columns([1.0] + [1] * n)
    cols[0].markdown(
        f"<div style='padding:8px 0;color:#94a3b8;font-size:12px;"
        f"font-family:JetBrains Mono,monospace;font-weight:500;"
        f"letter-spacing:1px;'>{criteria[i]}</div>",
        unsafe_allow_html=True
    )
    for j in range(n):
        if i == j:
            cols[j+1].markdown(
                "<div class='diag-cell'>1</div>",
                unsafe_allow_html=True
            )
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
            cols[j+1].markdown(
                f"<div class='recip-cell'>{label}</div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── RUN BUTTON ───────────────────────────
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if st.button("▶  RUN AHP ANALYSIS", use_container_width=True):

    # ══════ CORE CALCULATIONS ══════
    col_sums        = matrix.sum(axis=0)
    norm_matrix     = matrix / col_sums
    avg_weight      = norm_matrix.mean(axis=1)
    CW              = avg_weight / n
    CW_pct          = CW / CW.sum() * 100
    consistency_matrix = matrix * CW[np.newaxis, :]
    weighted_sum    = consistency_matrix.sum(axis=1)
    wsv_over_cw     = weighted_sum / CW
    lambda_max      = wsv_over_cw.mean()
    CI              = (lambda_max - n) / (n - 1)
    RI              = RI_dict.get(n, 1.59)
    CR              = CI / RI if RI > 0 else 0.0

    # ── TABLE 1 ──
    st.markdown("""<div class='card'><div class='section-title'>
    Pairwise Comparison Matrix<span class='tag'>Table 1</span></div>""", unsafe_allow_html=True)
    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria).round(4)
    df1.loc["Column Sum"] = col_sums.round(4)
    st.dataframe(df1, use_container_width=True)
    st.caption("Diagonal = 1  ·  Upper = inputs  ·  Lower = reciprocals  ·  Last row = column sums")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 2 ──
    st.markdown("""<div class='card'><div class='section-title'>
    Normalized Pairwise Matrix<span class='tag'>Table 2</span></div>""", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 3 ──
    st.markdown("""<div class='card'><div class='section-title'>
    Consistency Matrix<span class='tag'>Table 3</span></div>""", unsafe_allow_html=True)
    cw_row = pd.DataFrame([list(CW.round(3)) + [""]], columns=criteria + ["Weighted Sum"], index=["CW →"])
    st.dataframe(cw_row, use_container_width=True)
    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria).round(3)
    df3["Weighted Sum"] = weighted_sum.round(3)
    df3.loc["TOTAL"]    = df3.sum()
    st.dataframe(df3, use_container_width=True)
    st.caption("Cell[i][j] = pairwise[i][j] × CW[j]  ·  Weighted Sum = row sum")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 4 ──
    st.markdown("""<div class='card'><div class='section-title'>
    Consistency Summary<span class='tag'>Table 4</span></div>""", unsafe_allow_html=True)
    df4 = pd.DataFrame({
        "Criteria":         criteria,
        "Weighted Sum (WS)":weighted_sum.round(4),
        "Criteria Weight (CW)": CW.round(4),
        "WS / CW  (λ)":    wsv_over_cw.round(4),
    })
    total4 = pd.DataFrame([{
        "Criteria":         "TOTAL",
        "Weighted Sum (WS)":round(weighted_sum.sum(), 4),
        "Criteria Weight (CW)": round(CW.sum(), 4),
        "WS / CW  (λ)":    round(wsv_over_cw.sum(), 4),
    }])
    df4 = pd.concat([df4, total4], ignore_index=True)
    st.dataframe(df4, use_container_width=True, hide_index=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Metric boxes
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class='metric-box'>
        <div class='metric-label'>λ max</div>
        <div class='metric-value'>{lambda_max:.6f}</div>
        <div class='metric-verdict'>Principal eigenvalue</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='metric-box'>
        <div class='metric-label'>CI</div>
        <div class='metric-value'>{CI:.6f}</div>
        <div class='metric-verdict'>Consistency index</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class='metric-box'>
        <div class='metric-label'>RI  (n={n})</div>
        <div class='metric-value'>{RI}</div>
        <div class='metric-verdict'>Random index</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        cr_cls     = "cr-ok"        if CR < 0.10 else "cr-fail"
        cr_verdict = "✓ Consistent" if CR < 0.10 else "✗ Inconsistent"
        st.markdown(f"""<div class='metric-box'>
        <div class='metric-label'>CR</div>
        <div class='metric-value {cr_cls}'>{CR:.6f}</div>
        <div class='metric-verdict'>{cr_verdict}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 5 ──
    st.markdown("""<div class='card'><div class='section-title'>
    GIS Priority Weights<span class='tag'>Table 5</span></div>""", unsafe_allow_html=True)
    sorted_idx = np.argsort(avg_weight)[::-1]
    df5 = pd.DataFrame({
        "Rank":              range(1, n+1),
        "Criteria":          [criteria[i]            for i in sorted_idx],
        "Avg / Weight (W)":  [round(avg_weight[i],4) for i in sorted_idx],
        "Criteria CW":       [round(CW[i],4)          for i in sorted_idx],
        "CW %":              [f"{CW_pct[i]:.2f}%"    for i in sorted_idx],
    })
    st.dataframe(df5, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CHARTS ──
    st.markdown("""<div class='card'><div class='section-title'>
    Weight Visualization<span class='tag'>Charts</span></div>""", unsafe_allow_html=True)

    BG      = "#080c10"
    SURFACE = "#0e1520"
    TEAL    = "#2dd4bf"
    TEAL2   = "#0d9488"
    MUTED   = "#475569"
    TEXT    = "#94a3b8"

    sorted_criteria = [criteria[i] for i in sorted_idx]
    sorted_cw       = [CW[i]       for i in sorted_idx]
    palette = [TEAL, TEAL2, "#0f766e", "#134e4a", "#115e59",
               "#1d4ed8", "#1e40af", "#1e3a8a", "#312e81", "#4338ca"]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor=BG)
    fig.subplots_adjust(wspace=0.35)

    # — Bar chart —
    ax1 = axes[0]
    ax1.set_facecolor(SURFACE)
    bar_colors = [TEAL if i == 0 else palette[min(i, len(palette)-1)]
                  for i in range(len(sorted_cw))]
    bars = ax1.bar(sorted_criteria, sorted_cw,
                   color=bar_colors, edgecolor=BG, linewidth=1.2,
                   width=0.6, zorder=3)
    ax1.set_title("Criteria Weight (CW)", color=TEXT, fontsize=11,
                  pad=14, fontfamily="monospace", fontweight="normal", loc="left")
    ax1.set_xlabel("Criteria", color=MUTED, fontsize=9, labelpad=8)
    ax1.set_ylabel("CW", color=MUTED, fontsize=9, labelpad=8)
    ax1.tick_params(colors=MUTED, labelsize=8)
    for sp in ax1.spines.values():
        sp.set_color("#1e2d42")
        sp.set_linewidth(0.5)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.grid(axis="y", color="#1e2d42", linewidth=0.5, zorder=0)
    ax1.set_axisbelow(True)
    for bar, w in zip(bars, sorted_cw):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + max(sorted_cw)*0.015,
                 f"{w:.4f}", ha="center", va="bottom",
                 color=TEAL, fontsize=7.5, fontfamily="monospace")

    # — Pie chart —
    ax2 = axes[1]
    ax2.set_facecolor(BG)
    wedge_colors = palette[:len(sorted_cw)]
    wedges, texts, autotexts = ax2.pie(
        sorted_cw,
        labels=sorted_criteria,
        autopct="%1.1f%%",
        colors=wedge_colors,
        startangle=140,
        pctdistance=0.78,
        textprops={"color": TEXT, "fontsize": 8, "fontfamily": "monospace"},
        wedgeprops={"edgecolor": BG, "linewidth": 2}
    )
    for at in autotexts:
        at.set_color("#e2e8f0")
        at.set_fontsize(7.5)
    ax2.set_title("CW Distribution", color=TEXT, fontsize=11,
                  pad=14, fontfamily="monospace", fontweight="normal", loc="left")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CONSISTENCY INTERPRETATION ──
    st.markdown("""<div class='card'><div class='section-title'>
    Consistency Interpretation<span class='tag'>Result</span></div>""", unsafe_allow_html=True)

    if CR < 0.10:
        st.success(f"CR = {CR:.6f} < 0.10 — Pairwise comparisons are **consistent**. Results are reliable for decision making.")
    else:
        st.error(f"CR = {CR:.6f} ≥ 0.10 — Pairwise comparisons are **inconsistent**. Please revise your matrix.")
        st.warning("Tip: Review judgments that violate transitivity (e.g., A > B, B > C but C > A).")

    st.markdown(f"""
| Parameter | Value | Formula |
|-----------|-------|---------|
| n (criteria) | {n} | — |
| λ_max | {lambda_max:.6f} | mean(WS_i / CW_i) |
| CI | {CI:.6f} | (λ_max − n) / (n − 1) |
| RI | {RI} | Saaty RI table, n = {n} |
| CR | {CR:.6f} | CI / RI |
| Result | {"Consistent ✓" if CR < 0.10 else "Inconsistent ✗"} | CR {"<" if CR < 0.10 else "≥"} 0.10 |
""")
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── FOOTER ───────────────────────────
st.markdown("""
<div class='footer'>
<div style='color:#1e3a4a;font-size:18px;margin-bottom:10px;'>⬡</div>
<div style='color:#2dd4bf;font-size:13px;font-weight:600;letter-spacing:2px;margin-bottom:6px;'>
ANINDO PAUL SOURAV</div>
<div style='color:#1e2d42;margin-bottom:14px;font-size:11px;letter-spacing:1px;'>
AHP CALCULATOR · FREE FOR ALL USERS</div>
<a href='https://www.linkedin.com/in/anindo046/' target='_blank'>LinkedIn</a>
<span style='color:#1e2d42;margin:0 12px;'>·</span>
<a href='https://anindo46.github.io/portfolio/' target='_blank'>Portfolio</a>
</div>
""", unsafe_allow_html=True)
