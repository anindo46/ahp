import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AHP Calculator", layout="wide")

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.card {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}
.notice {
    background-color: rgba(255,255,255,0.05);
    padding: 12px;
    border-left: 4px solid #4CAF50;
    border-radius: 6px;
}
.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='title'>AHP Calculator</div>", unsafe_allow_html=True)

# -----------------------------
# NOTICE
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("""
<div class='notice'>
Use short names (Elev, Dist, Slp, etc).<br>
Saaty scale (1–9).<br>
CR &lt; 0.1 = acceptable.<br>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# INPUT
# -----------------------------
criteria_input = st.sidebar.text_area(
    "Criteria",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo"
)

criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

# -----------------------------
# PAIRWISE MATRIX INPUT
# -----------------------------
matrix = np.ones((n, n))

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Input Pairwise Matrix</div>", unsafe_allow_html=True)

for i in range(n):
    cols = st.columns(n)
    for j in range(n):
        if i == j:
            cols[j].markdown("—")
        elif j > i:
            val = cols[j].number_input(
                f"{i}-{j}",
                min_value=0.11,
                max_value=9.0,
                value=1.0,
                step=0.1,
                key=f"{i}-{j}"
            )
            matrix[i][j] = val
            matrix[j][i] = 1 / val
        else:
            cols[j].markdown(" ")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# RUN
# -----------------------------
if st.button("Run AHP"):

    # -------- TABLE 1 --------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 1: Pairwise Comparison Matrix</div>", unsafe_allow_html=True)

    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria)
    df1["Row Sum"] = df1.sum(axis=1)
    df1.loc["TOTAL"] = df1.sum()

    st.dataframe(df1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------- NORMALIZATION --------
    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum

    # -------- TABLE 2 --------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 2: Normalized Pairwise Matrix</div>", unsafe_allow_html=True)

    df2 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria)
    df2.loc["TOTAL"] = df2.sum()

    st.dataframe(df2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------- WEIGHTS --------
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals.real)
    weights = np.abs(eigvecs[:, max_index].real)
    weights = weights / weights.sum()

    weighted_sum = np.dot(matrix, weights)
    lambda_vals = weighted_sum / weights
    lambda_max = np.mean(lambda_vals)

    CI = (lambda_max - n) / (n - 1)
    RI_dict = {8: 1.41}
    RI = RI_dict.get(n, 1.41)
    CR = CI / RI

    # -------- TABLE 3 (CONSISTENCY MATRIX FULL GRID) --------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 3: Consistency Matrix</div>", unsafe_allow_html=True)

    weighted_matrix = matrix * weights
    df3 = pd.DataFrame(weighted_matrix, index=criteria, columns=criteria)
    df3.loc["TOTAL"] = df3.sum()

    st.dataframe(df3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -------- TABLE 4 (CONSISTENCY SUMMARY) --------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 4: Consistency Summary</div>", unsafe_allow_html=True)

    df4 = pd.DataFrame({
        "Weighted Sum": weighted_sum,
        "Criteria Weight": weights,
        "WSV/W": lambda_vals
    }, index=criteria)

    df4.loc["TOTAL"] = df4.sum()

    st.dataframe(df4, use_container_width=True)

    st.write(f"CI = {CI:.6f}")
    st.write(f"RI = {RI}")
    st.write(f"CR = {CR:.6f}")

    st.markdown("</div>", unsafe_allow_html=True)

    # -------- TABLE 5 (GIS WEIGHT) --------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 5: GIS Usable Weight</div>", unsafe_allow_html=True)

    gis_weights = np.round(weights, 2)

    df5 = pd.DataFrame({
        "Criteria": criteria,
        "GIS Weight": gis_weights
    })

    st.dataframe(df5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # -------- GRAPH --------
    fig, ax = plt.subplots()
    ax.bar(criteria, weights)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("""
<b>Anindo Paul Sourav</b><br>
Free for all users<br><br>

🔗 https://www.linkedin.com/in/anindo046/ <br>
🌐 https://anindo46.github.io/portfolio/
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
