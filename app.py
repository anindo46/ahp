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
    padding: 14px;
    border-left: 5px solid #00c853;
    border-radius: 8px;
}
.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
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
Use short names. Saaty scale (1–9). CR &lt; 0.1 acceptable.
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
criteria_input = st.sidebar.text_area(
    "Criteria",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo"
)

criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

# -----------------------------
# MATRIX INPUT
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
                f"{criteria[i]} vs {criteria[j]}",
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

    # TABLE 1
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 1: Pairwise Comparison Matrix</div>", unsafe_allow_html=True)

    df1 = pd.DataFrame(matrix, index=criteria, columns=criteria)
    st.dataframe(df1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # NORMALIZATION
    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum

    # TABLE 2
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 2: Normalized Pairwise Matrix</div>", unsafe_allow_html=True)

    df2 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria)
    df2.loc["TOTAL"] = df2.sum()

    st.dataframe(df2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # WEIGHTS (Eigenvector)
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals.real)
    weights = np.abs(eigvecs[:, max_index].real)
    weights = weights / weights.sum()

    # -----------------------------
    # 🔥 CONSISTENCY MATRIX FIX (COLUMN * WEIGHT)
    # -----------------------------
    consistency_matrix = norm_matrix * weights  # broadcasting column-wise

    # TABLE 3
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 3: Consistency Matrix (Weighted Normalized Matrix)</div>", unsafe_allow_html=True)

    df3 = pd.DataFrame(consistency_matrix, index=criteria, columns=criteria)
    df3.loc["TOTAL"] = df3.sum()

    st.dataframe(df3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # WEIGHTED SUM (ROW SUM OF TABLE 3)
    # -----------------------------
    weighted_sum = df3.iloc[:-1].sum(axis=1).values

    lambda_vals = weighted_sum / weights
    lambda_max = np.mean(lambda_vals)

    CI = (lambda_max - n) / (n - 1)

    RI_dict = {8: 1.41}
    RI = RI_dict.get(n, 1.41)

    CR = CI / RI

    # TABLE 4
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

    # TABLE 5
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 5: GIS Usable Weight</div>", unsafe_allow_html=True)

    df5 = pd.DataFrame({
        "Criteria": criteria,
        "GIS Weight": np.round(weights, 2)
    })

    st.dataframe(df5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # GRAPH
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
