import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(page_title="AHP Calculator", layout="wide")

# ─────────────────────────── STYLE ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

/* Page background */
.stApp { background: #0f1117; }

.title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #e0f7e9;
    padding: 18px 0 4px 0;
    font-family: 'IBM Plex Mono', monospace;
}
.subtitle {
    text-align: center;
    font-size: 13px;
    color: #78909c;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 28px;
}

.card {
    background: rgba(255,255,255,0.03);
    padding: 22px 26px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 22px;
}

.section-title {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #80cbc4;
    margin-bottom: 14px;
    font-family: 'IBM Plex Mono', monospace;
    border-bottom: 1px solid rgba(128,203,196,0.2);
    padding-bottom: 8px;
}

.notice {
    background: rgba(0,200,83,0.07);
    padding: 14px 18px;
    border-left: 4px solid #00c853;
    border-radius: 8px;
    font-size: 13px;
    color: #b2dfdb;
}

.cr-ok   { color: #69f0ae; font-weight: 700; font-size: 16px; }
.cr-fail { color: #ff5252; font-weight: 700; font-size: 16px; }

.metric-box {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 14px;
    text-align: center;
}
.metric-label { font-size: 11px; color: #78909c; letter-spacing: 2px; text-transform: uppercase; }
.metric-value { font-size: 26px; font-weight: 700; color: #e0f7e9; font-family: 'IBM Plex Mono', monospace; }

.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    color: #546e7a;
    font-size: 13px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
.footer a { color: #80cbc4; text-decoration: none; }

/* Dataframe styling */
div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid rgba(255,255,255,0.06); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── HEADER ───────────────────────────
st.markdown("<div class='title'>⬡ AHP CALCULATOR</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analytic Hierarchy Process · Multi-Criteria Decision Analysis</div>", unsafe_allow_html=True)

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

st.sidebar.markdown("**1. Column Sum Normalization**")
st.sidebar.latex(r"\bar{a}_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}}")

st.sidebar.markdown("**2. Priority Weight (Criteria Weight)**")
st.sidebar.latex(r"W_i = \frac{1}{n} \sum_{j=1}^{n} \bar{a}_{ij}")

st.sidebar.markdown("**3. Consistency Matrix Cell**")
st.sidebar.latex(r"CM_{ij} = a_{ij} \times W_j")

st.sidebar.markdown("**4. Weighted Sum Vector**")
st.sidebar.latex(r"WS_i = \sum_{j=1}^{n} CM_{ij}")

st.sidebar.markdown("**5. Lambda Max**")
st.sidebar.latex(r"\lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{WS_i}{W_i}")

st.sidebar.markdown("**6. Consistency Index (CI)**")
st.sidebar.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")

st.sidebar.markdown("**7. Consistency Ratio (CR)**")
st.sidebar.latex(r"CR = \frac{CI}{RI}")

st.sidebar.markdown("**Acceptable: CR < 0.10**")

st.sidebar.markdown("---")

# ── RI Table ──
RI_dict = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
    11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
}

st.sidebar.markdown("### 📊 Random Index (RI) Table")
ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n (Criteria)", "RI Value"])
st.sidebar.dataframe(ri_df, use_container_width=True, hide_index=True)

st.sidebar.markdown(f"**Current n = {n} → RI = {RI_dict.get(n, 1.59)}**")

st.sidebar.markdown("---")

# ── Saaty Scale ──
st.sidebar.markdown("### 🔢 Saaty Scale")
saaty_df = pd.DataFrame({
    "Value": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Meaning": [
        "Equal importance",
        "Weak/Slight",
        "Moderate importance",
        "Moderate plus",
        "Strong importance",
        "Strong plus",
        "Very strong importance",
        "Very, very strong",
        "Extreme importance"
    ],
    "Reciprocal": ["1/1","1/2","1/3","1/4","1/5","1/6","1/7","1/8","1/9"]
})
st.sidebar.dataframe(saaty_df, use_container_width=True, hide_index=True)

# ─────────────────────────── MATRIX INPUT ───────────────────────────
st.markdown("<div class='card'><div class='section-title'>📥 Step 1 · Pairwise Comparison Matrix Input</div>", unsafe_allow_html=True)
st.caption("Fill only the upper triangle (highlighted). Lower triangle auto-fills as reciprocals. Diagonal = 1.")

matrix = np.ones((n, n))

for i in range(n):
    cols = st.columns([0.8] + [1] * n)
    cols[0].markdown(f"**{criteria[i]}**")
    for j in range(n):
        if i == j:
            cols[j + 1].markdown(
                f"<div style='text-align:center;padding:6px;background:rgba(128,203,196,0.15);border-radius:6px;color:#80cbc4;font-weight:700;font-family:monospace'>1</div>",
                unsafe_allow_html=True
            )
        elif j > i:
            val = cols[j + 1].number_input(
                f"{criteria[i]} vs {criteria[j]}",
                min_value=0.111, max_value=9.0, value=1.0, step=0.5,
                key=f"m{i}-{j}", label_visibility="collapsed"
            )
            matrix[i][j] = val
            matrix[j][i] = round(1 / val, 6)
        else:
            cols[j + 1].markdown(
                f"<div style='text-align:center;padding:6px;color:#546e7a;font-family:monospace;font-size:13px'>1/{int(round(1/matrix[i][j])) if matrix[i][j] < 1 else round(matrix[j][i],2)}</div>",
                unsafe_allow_html=True
            )

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────── RUN ───────────────────────────
if st.button("▶ Run AHP Analysis", use_container_width=True):

    # ── TABLE 1: Pairwise Matrix ──
    st.markdown("<div class='card'><div class='section-title'>Table 1 · Pairwise Comparison Matrix</div>", unsafe_allow_html=True)
    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria).round(4)
    col_sums = matrix.sum(axis=0)
    df1.loc["Column Sum"] = col_sums.round(4)
    st.dataframe(df1, use_container_width=True)
    st.caption("Diagonal = 1 | Upper triangle = input values | Lower triangle = reciprocals | Bottom row = column sums")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── NORMALIZATION ──
    col_sums_raw = matrix.sum(axis=0)
    norm_matrix = matrix / col_sums_raw   # each cell ÷ column sum

    # ── TABLE 2: Normalized Matrix ──
    st.markdown("<div class='card'><div class='section-title'>Table 2 · Normalized Matrix (Column Sum Normalized)</div>", unsafe_allow_html=True)
    df2 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria).round(4)
    # Criteria weight = row mean of normalized matrix
    weights = norm_matrix.mean(axis=1)
    df2["Criteria Weight (W)"] = weights.round(4)
    df2.loc["Column Sum"] = df2.sum()
    df2.loc["Column Sum", "Criteria Weight (W)"] = weights.sum().round(4)
    st.dataframe(df2, use_container_width=True)
    st.caption("Each cell = original value ÷ column sum | Criteria Weight = row mean | Column sums ≈ 1.0")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 3: Consistency Matrix ──
    # Each cell CM[i][j] = original_matrix[i][j] × W[j]  (multiply each column by its weight)
    consistency_matrix = matrix * weights[np.newaxis, :]  # broadcast: col j × W[j]

    st.markdown("<div class='card'><div class='section-title'>Table 3 · Consistency Matrix</div>", unsafe_allow_html=True)
    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria).round(4)
    # Weighted Sum = row sum of consistency matrix
    weighted_sum = consistency_matrix.sum(axis=1)
    df3["Weighted Sum"] = weighted_sum.round(4)
    df3.loc["Column Total"] = df3.sum()
    st.dataframe(df3, use_container_width=True)
    st.caption("Each cell = Pairwise value × Column criterion weight | Weighted Sum = sum across row")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CONSISTENCY CALCULATIONS ──
    lambda_vals = weighted_sum / weights          # WSV / W
    lambda_max = lambda_vals.mean()
    CI = (lambda_max - n) / (n - 1)
    RI = RI_dict.get(n, 1.59)
    CR = CI / RI if RI > 0 else 0

    # ── TABLE 4: Consistency Summary ──
    st.markdown("<div class='card'><div class='section-title'>Table 4 · Consistency Summary</div>", unsafe_allow_html=True)

    df4 = pd.DataFrame({
        "Criteria": criteria,
        "Weighted Sum (WS)": weighted_sum.round(6),
        "Criteria Weight (W)": weights.round(6),
        "WSV / W (λ)": lambda_vals.round(6),
    })

    # Totals row
    total_row = pd.DataFrame([{
        "Criteria": "TOTAL",
        "Weighted Sum (WS)": weighted_sum.sum().round(6),
        "Criteria Weight (W)": weights.sum().round(6),
        "WSV / W (λ)": lambda_vals.sum().round(6),
    }])
    df4 = pd.concat([df4, total_row], ignore_index=True)
    st.dataframe(df4, use_container_width=True, hide_index=True)

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>λ max</div><div class='metric-value'>{lambda_max:.6f}</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>CI</div><div class='metric-value'>{CI:.6f}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-box'><div class='metric-label'>RI (n={n})</div><div class='metric-value'>{RI}</div></div>", unsafe_allow_html=True)
    with m4:
        cr_class = "cr-ok" if CR < 0.10 else "cr-fail"
        cr_verdict = "✅ Consistent" if CR < 0.10 else "❌ Inconsistent"
        st.markdown(f"<div class='metric-box'><div class='metric-label'>CR</div><div class='metric-value {cr_class}'>{CR:.6f}</div><div style='font-size:12px;color:#78909c;margin-top:4px'>{cr_verdict}</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── TABLE 5: GIS Weight Summary ──
    st.markdown("<div class='card'><div class='section-title'>Table 5 · GIS / Final Priority Weights</div>", unsafe_allow_html=True)

    sorted_idx = np.argsort(weights)[::-1]
    df5 = pd.DataFrame({
        "Rank": range(1, n + 1),
        "Criteria": [criteria[i] for i in sorted_idx],
        "Priority Weight": [round(weights[i], 4) for i in sorted_idx],
        "Weight %": [f"{weights[i]*100:.2f}%" for i in sorted_idx],
    })
    st.dataframe(df5, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CHARTS ──
    st.markdown("<div class='card'><div class='section-title'>📊 Weight Visualization</div>", unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor="#0f1117")

    sorted_criteria = [criteria[i] for i in sorted_idx]
    sorted_weights  = [weights[i] for i in sorted_idx]

    # Bar chart
    ax1 = axes[0]
    ax1.set_facecolor("#0f1117")
    colors = ["#80cbc4" if w == max(sorted_weights) else "#26a69a" for w in sorted_weights]
    bars = ax1.bar(sorted_criteria, sorted_weights, color=colors, edgecolor="#0f1117", linewidth=0.8)
    ax1.set_title("Priority Weights by Criteria", color="#e0f7e9", fontsize=12, pad=12)
    ax1.set_xlabel("Criteria", color="#78909c")
    ax1.set_ylabel("Weight", color="#78909c")
    ax1.tick_params(colors="#78909c", labelsize=9)
    ax1.spines[:].set_color("#263238")
    for bar, w in zip(bars, sorted_weights):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                 f"{w:.3f}", ha="center", va="bottom", color="#80cbc4", fontsize=8)

    # Pie chart
    ax2 = axes[1]
    ax2.set_facecolor("#0f1117")
    palette = ["#80cbc4","#26a69a","#00897b","#00796b","#00695c",
               "#4db6ac","#b2dfdb","#e0f2f1"][:n]
    wedges, texts, autotexts = ax2.pie(
        sorted_weights, labels=sorted_criteria, autopct="%1.1f%%",
        colors=palette[:len(sorted_weights)], startangle=140,
        textprops={"color":"#b2dfdb","fontsize":8},
        wedgeprops={"edgecolor":"#0f1117","linewidth":1.5}
    )
    for at in autotexts:
        at.set_color("#e0f7e9")
        at.set_fontsize(8)
    ax2.set_title("Weight Distribution", color="#e0f7e9", fontsize=12, pad=12)

    plt.tight_layout(pad=2)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── CONSISTENCY INTERPRETATION ──
    st.markdown("<div class='card'><div class='section-title'>🔍 Consistency Interpretation</div>", unsafe_allow_html=True)
    if CR < 0.10:
        st.success(f"✅ CR = {CR:.6f} < 0.10 → The pairwise comparisons are **consistent**. Results are reliable.")
    else:
        st.error(f"❌ CR = {CR:.6f} ≥ 0.10 → The pairwise comparisons are **inconsistent**. Please revise your matrix.")
        st.warning("Tip: Review judgments where values deviate strongly from transitivity (e.g., A>B, B>C but C>A).")

    st.markdown(f"""
    | Parameter | Value | Formula |
    |-----------|-------|---------|
    | n (criteria count) | {n} | — |
    | λ_max | {lambda_max:.6f} | mean(WS_i / W_i) |
    | CI | {CI:.6f} | (λ_max − n) / (n − 1) |
    | RI | {RI} | Saaty RI table for n={n} |
    | CR | {CR:.6f} | CI / RI |
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
