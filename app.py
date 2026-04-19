import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AHP Calculator", layout="wide")

# ─────────────────────────── STYLE ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 20%, #0b0f14, #030507);
}

/* Smooth animation */
@keyframes fadeUp {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

/* Premium glass card */
.card, .ahp-card {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 22px;
    animation: fadeUp 0.35s ease;
}

/* Section headers */
.section-title, .ahp-sec-label {
    font-family: 'JetBrains Mono', monospace;
    color: #34d399;
    letter-spacing: 2px;
    font-size: 12px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #065f46, #10b981);
    border-radius: 12px;
    border: none;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16,185,129,0.3);
}

/* Inputs */
input {
    background:#020406 !important;
    border:1px solid #1f2937 !important;
    color:#d1fae5 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Metrics */
.ahp-metric, .metric-box {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Footer */
.footer {
    text-align:center;
    padding:40px;
    border-top:1px solid rgba(255,255,255,0.05);
    color:#6b7280;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER ───────────────────────────
st.markdown("""
<div style="display:flex;justify-content:center;padding:10px 0 20px 0;">
<svg width="680" viewBox="0 0 680 110" xmlns="http://www.w3.org/2000/svg">
<defs><style>
.hex{fill:none;stroke:#80cbc4;stroke-width:1.2}
.hex2{fill:none;stroke:#26a69a;stroke-width:0.7;opacity:.5}
.ring{fill:none;stroke:#4db6ac;stroke-width:0.6;opacity:.35}
.dot{fill:#80cbc4}
.ln{stroke:#80cbc4;stroke-width:1;opacity:.6;fill:none}
.s1{transform-origin:55px 42px;animation:spin 18s linear infinite}
.s2{transform-origin:55px 42px;animation:spin 11s linear infinite reverse}
.pu{animation:pulse 3s ease-in-out infinite}
.fi{animation:fadein 1.2s ease both}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:.75}}
@keyframes fadein{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
</style></defs>
<g class="fi">
<g class="s1"><polygon class="hex" points="55,5 77,17 77,42 55,54 33,42 33,17"/></g>
<g class="s2"><polygon class="hex2" points="55,0 82,15 82,50 55,65 28,50 28,15"/></g>
<circle class="ring pu" cx="55" cy="29" r="22"/>
<circle class="ring" cx="55" cy="29" r="15" style="animation-delay:.6s"/>
<line class="ln" x1="55" y1="10" x2="55" y2="50"/>
<line class="ln" x1="36" y1="20" x2="74" y2="40"/>
<line class="ln" x1="74" y1="20" x2="36" y2="40"/>
<circle class="dot" cx="55" cy="10" r="2.5"/>
<circle class="dot" cx="36" cy="20" r="2"/>
<circle class="dot" cx="74" cy="20" r="2"/>
<circle class="dot" cx="55" cy="29" r="3.5"/>
<circle class="dot" cx="36" cy="40" r="2"/>
<circle class="dot" cx="74" cy="40" r="2"/>
<circle class="dot" cx="55" cy="50" r="2.5"/>
<text x="108" y="38" font-family="IBM Plex Mono,monospace" font-size="34" font-weight="700" letter-spacing="3" fill="#e0f7e9">AHP</text>
<text x="108" y="60" font-family="IBM Plex Mono,monospace" font-size="34" font-weight="700" letter-spacing="3" fill="#80cbc4">CALCULATOR</text>
<text x="110" y="80" font-family="IBM Plex Sans,sans-serif" font-size="12" letter-spacing="5" fill="#78909c">ANALYTIC HIERARCHY PROCESS</text>
</g>
</svg>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── NOTICE ───────────────────────────
st.markdown("""
<div class='card'>
<div class='notice'>
📌 <b>Instructions:</b> Enter criteria separated by commas. Fill upper-triangle values using Saaty scale (1–9).
Diagonal is automatically set to 1, and reciprocals are auto-filled. A <b>CR &lt; 0.10</b> indicates acceptable consistency.
</div></div>
""", unsafe_allow_html=True)

# ─────────────────────────── SIDEBAR ───────────────────────────
st.sidebar.markdown("## ⚙️ Configuration")

criteria_input = st.sidebar.text_area(
    "Criteria (comma-separated)",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo",
    help="Enter short names for your criteria"
)
criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

st.sidebar.markdown("---")

# ── AHP Formulas ──
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

st.sidebar.markdown("**✅ Acceptable: CR < 0.10**")
st.sidebar.markdown("---")

# ── RI Table ──
RI_dict = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,  5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
   11: 1.51,12: 1.48,13: 1.56,14: 1.57, 15: 1.59
}

st.sidebar.markdown("### 📊 Random Index (RI) Table")
ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n (Criteria)", "RI Value"])
st.sidebar.dataframe(ri_df, use_container_width=True, hide_index=True)
st.sidebar.markdown(f"**Current n = {n} → RI = {RI_dict.get(n, 1.59)}**")
st.sidebar.markdown("---")

# ── Saaty Scale ──
st.sidebar.markdown("### 🔢 Saaty Scale")
saaty_df = pd.DataFrame({
    "Value":   [1,2,3,4,5,6,7,8,9],
    "Meaning": ["Equal importance","Weak/Slight","Moderate importance",
                "Moderate plus","Strong importance","Strong plus",
                "Very strong importance","Very, very strong","Extreme importance"],
    "Reciprocal": ["1/1","1/2","1/3","1/4","1/5","1/6","1/7","1/8","1/9"]
})
st.sidebar.dataframe(saaty_df, use_container_width=True, hide_index=True)

# ─────────────────────────── MATRIX INPUT ───────────────────────────
st.markdown("<div class='card'><div class='section-title'>📥 Step 1 · Pairwise Comparison Matrix Input</div>",
            unsafe_allow_html=True)
st.caption("Fill only the upper triangle. Lower triangle auto-fills as reciprocals. Diagonal = 1.")

matrix = np.ones((n, n))

for i in range(n):
    cols = st.columns([0.8] + [1] * n)
    cols[0].markdown(f"**{criteria[i]}**")
    for j in range(n):
        if i == j:
            cols[j+1].markdown(
                "<div style='text-align:center;padding:6px;background:rgba(128,203,196,0.15);"
                "border-radius:6px;color:#80cbc4;font-weight:700;font-family:monospace'>1</div>",
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
                f"<div style='text-align:center;padding:6px;color:#546e7a;"
                f"font-family:monospace;font-size:12px'>{label}</div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── RUN ───────────────────────────
if st.button("▶ Run AHP Analysis", use_container_width=True):

    # ══════════════════════════════════════════════════════════════
    #  CORE CALCULATIONS  — matches Excel exactly
    #
    #  Excel workflow (verified from screenshots):
    #  1. Normalize: norm[i][j] = pairwise[i][j] / col_sum[j]
    #  2. Average/Weight W[i] = row mean of norm matrix
    #  3. Criteria Weight CW[i] = W[i] / n
    #  4. Consistency Matrix CM[i][j] = pairwise[i][j] * CW[j]
    #  5. Weighted Sum WS[i] = sum of row i of CM  (= pairwise[i] dot CW)
    #  6. WSV/CW[i] = WS[i] / CW[i]
    #  7. lambda_max = mean(WSV/CW)
    #  8. CI = (lambda_max - n) / (n - 1)
    #  9. CR = CI / RI
    # ══════════════════════════════════════════════════════════════

    col_sums       = matrix.sum(axis=0)                   # (n,)
    norm_matrix    = matrix / col_sums                    # normalised matrix
    avg_weight     = norm_matrix.mean(axis=1)             # W  — e.g. 0.295, 0.186 …
    CW             = avg_weight / n                       # CW — e.g. 0.037, 0.023 …
    CW_pct         = CW / CW.sum() * 100                 # percentage

    # Consistency matrix: CM[i][j] = pairwise[i][j] * CW[j]
    consistency_matrix = matrix * CW[np.newaxis, :]       # broadcast across columns

    weighted_sum   = consistency_matrix.sum(axis=1)       # WS — row sums
    wsv_over_cw    = weighted_sum / CW                    # WS / CW

    lambda_max     = wsv_over_cw.mean()
    CI             = (lambda_max - n) / (n - 1)
    RI             = RI_dict.get(n, 1.59)
    CR             = CI / RI if RI > 0 else 0.0

    # ── TABLE 1 ──────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>Table 1 · Pairwise Comparison Matrix</div>",
                unsafe_allow_html=True)
    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria).round(4)
    df1.loc["Column Sum"] = col_sums.round(4)
    st.dataframe(df1, use_container_width=True)
    st.caption("Diagonal = 1 | Upper triangle = your inputs | Lower triangle = reciprocals | Last row = column sums")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 2 ──────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>Table 2 · Normalized Pairwise Matrix</div>",
                unsafe_allow_html=True)
    df2 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria).round(9)
    df2["Average / Weight (W)"] = avg_weight.round(3)
    df2["Criteria Weight (CW)"] = CW.round(3)
    df2["CW %"]                 = CW_pct.round(3)
    totals2 = {c: norm_matrix[:, j].sum() for j, c in enumerate(criteria)}
    totals2["Average / Weight (W)"] = round(avg_weight.sum(), 3)
    totals2["Criteria Weight (CW)"] = round(CW.sum(), 3)
    totals2["CW %"]                 = round(CW_pct.sum(), 3)
    df2.loc["TOTAL"] = totals2
    st.dataframe(df2, use_container_width=True)
    st.caption("Each cell = original ÷ column sum | W = row mean | CW = W ÷ n | Column sums = 1.0")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 3 ──────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>Table 3 · Consistency Matrix</div>",
                unsafe_allow_html=True)

    # CW header row (mimics the orange row in Excel)
    cw_row = pd.DataFrame([list(CW.round(3)) + [""]], columns=criteria + ["Weighted Sum"], index=["CW →"])
    st.dataframe(cw_row, use_container_width=True)

    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria).round(3)
    df3["Weighted Sum"] = weighted_sum.round(3)
    df3.loc["TOTAL"]    = df3.sum()
    st.dataframe(df3, use_container_width=True)
    st.caption("Cell[i][j] = pairwise[i][j] × CW[j]  |  Weighted Sum = row sum  |  TOTAL = column sums")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 4 ──────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>Table 4 · Consistency Summary</div>",
                unsafe_allow_html=True)

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

    # Metric boxes
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>λ max</div>"
                    f"<div class='metric-value'>{lambda_max:.6f}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>CI</div>"
                    f"<div class='metric-value'>{CI:.6f}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>RI  (n={n})</div>"
                    f"<div class='metric-value'>{RI}</div></div>", unsafe_allow_html=True)
    with m4:
        cr_class   = "cr-ok"        if CR < 0.10 else "cr-fail"
        cr_verdict = "✅ Consistent" if CR < 0.10 else "❌ Inconsistent"
        st.markdown(f"<div class='metric-box'><div class='metric-label'>CR</div>"
                    f"<div class='metric-value {cr_class}'>{CR:.6f}</div>"
                    f"<div style='font-size:12px;color:#78909c;margin-top:4px'>{cr_verdict}</div></div>",
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 5 ──────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>Table 5 · GIS / Final Priority Weights</div>",
                unsafe_allow_html=True)
    sorted_idx = np.argsort(avg_weight)[::-1]
    df5 = pd.DataFrame({
        "Rank":                 range(1, n+1),
        "Criteria":             [criteria[i]       for i in sorted_idx],
        "Average/Weight (W)":   [round(avg_weight[i], 4) for i in sorted_idx],
        "Criteria Weight (CW)": [round(CW[i],       4) for i in sorted_idx],
        "CW %":                 [f"{CW_pct[i]:.2f}%"   for i in sorted_idx],
    })
    st.dataframe(df5, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CHARTS ───────────────────────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>📊 Weight Visualization</div>",
                unsafe_allow_html=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor="#0f1117")

    sorted_criteria = [criteria[i] for i in sorted_idx]
    sorted_cw       = [CW[i]       for i in sorted_idx]

    ax1 = axes[0]
    ax1.set_facecolor("#0f1117")
    colors = ["#80cbc4" if w == max(sorted_cw) else "#26a69a" for w in sorted_cw]
    bars = ax1.bar(sorted_criteria, sorted_cw, color=colors, edgecolor="#0f1117", linewidth=0.8)
    ax1.set_title("Criteria Weight (CW)", color="#e0f7e9", fontsize=12, pad=12)
    ax1.set_xlabel("Criteria", color="#78909c")
    ax1.set_ylabel("CW", color="#78909c")
    ax1.tick_params(colors="#78909c", labelsize=9)
    ax1.spines[:].set_color("#263238")
    for bar, w in zip(bars, sorted_cw):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0002,
                 f"{w:.4f}", ha="center", va="bottom", color="#80cbc4", fontsize=8)

    ax2 = axes[1]
    ax2.set_facecolor("#0f1117")
    palette = ["#80cbc4","#26a69a","#00897b","#00796b","#00695c",
               "#4db6ac","#b2dfdb","#e0f2f1","#a5d6a7","#c8e6c9"]
    wedges, texts, autotexts = ax2.pie(
        sorted_cw, labels=sorted_criteria, autopct="%1.1f%%",
        colors=palette[:len(sorted_cw)], startangle=140,
        textprops={"color":"#b2dfdb","fontsize":8},
        wedgeprops={"edgecolor":"#0f1117","linewidth":1.5}
    )
    for at in autotexts:
        at.set_color("#e0f7e9"); at.set_fontsize(8)
    ax2.set_title("CW Distribution", color="#e0f7e9", fontsize=12, pad=12)

    plt.tight_layout(pad=2)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CONSISTENCY INTERPRETATION ────────────────────────────────
    st.markdown("<div class='card'><div class='section-title'>🔍 Consistency Interpretation</div>",
                unsafe_allow_html=True)
    if CR < 0.10:
        st.success(f"✅ CR = {CR:.6f} < 0.10 → Pairwise comparisons are **consistent**. Results are reliable.")
    else:
        st.error(f"❌ CR = {CR:.6f} ≥ 0.10 → Pairwise comparisons are **inconsistent**. Please revise your matrix.")
        st.warning("Tip: Review judgments that violate transitivity (e.g., A>B, B>C but C>A).")

    st.markdown(f"""
| Parameter | Value | Formula |
|-----------|-------|---------|
| n (criteria) | {n} | — |
| λ_max | {lambda_max:.6f} | mean(WS_i / CW_i) |
| CI | {CI:.6f} | (λ_max − n) / (n − 1) |
| RI | {RI} | Saaty RI table, n = {n} |
| CR | {CR:.6f} | CI / RI |
| Result | {"Consistent ✅" if CR < 0.10 else "Inconsistent ❌"} | CR {"<" if CR < 0.10 else "≥"} 0.10 |
""")
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── FOOTER ───────────────────────────
st.markdown("""
<div class='footer'>
<b style='color:#80cbc4;font-size:15px'>Anindo Paul Sourav</b><br>
<span style='color:#546e7a'>AHP Calculator · Free for all users</span><br><br>
<a href='https://www.linkedin.com/in/anindo046/' target='_blank'>🔗 LinkedIn</a> &nbsp;|&nbsp;
<a href='https://anindo46.github.io/portfolio/' target='_blank'>🌐 Portfolio</a>
</div>
""", unsafe_allow_html=True)
