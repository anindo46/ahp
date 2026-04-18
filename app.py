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
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
}
.subtitle {
    text-align: center;
    color: #9aa0a6;
    margin-bottom: 20px;
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
    margin-bottom: 15px;
}
.footer {
    text-align: center;
    padding: 30px;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='title'>AHP Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analytic Hierarchy Process Tool</div>", unsafe_allow_html=True)

# -----------------------------
# NOTICE BOARD
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("""
<div class='notice'>
<b>Notice:</b><br>
• This tool calculates weights using AHP (Analytic Hierarchy Process)<br>
• Input criteria using short names (El, Sl, Dis, DD) for better layout<br>
• Values follow Saaty Scale (1–9)<br>
• Output includes normalized matrix, weights, and consistency check (CI, CR)<br>
• CR &lt; 0.1 → Acceptable consistency
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR INPUT
# -----------------------------
st.sidebar.header("Input")

criteria_input = st.sidebar.text_area(
    "Criteria (comma separated)",
    "Elev, Dist, Slope, TWI, Rainf, D_D, Soil, Geo"
)

criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

# -----------------------------
# RI TABLE
# -----------------------------
RI_dict = {
    1: 0, 2: 0, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32,
    8: 1.41, 9: 1.45, 10: 1.49
}

# -----------------------------
# PAIRWISE MATRIX
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Pairwise Comparison Matrix</div>", unsafe_allow_html=True)

matrix = np.ones((n, n))

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
# RUN AHP
# -----------------------------
if st.button("Run AHP"):

    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum

    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals.real)
    weights = np.abs(eigvecs[:, max_index].real)
    weights = weights / weights.sum()

    weighted_sum = np.dot(matrix, weights)
    lambda_vals = weighted_sum / weights
    lambda_max = np.mean(lambda_vals)

    CI = (lambda_max - n) / (n - 1)
    RI = RI_dict.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0

    # -----------------------------
    # TABLE 1
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 1: Normalized Pairwise Matrix</div>", unsafe_allow_html=True)

    table1 = pd.DataFrame(norm_matrix, index=criteria, columns=criteria)
    table1["Weighted Sum"] = weighted_sum
    table1["Weight"] = weights

    st.dataframe(table1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # TABLE 2
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 2: Weighted Matrix</div>", unsafe_allow_html=True)

    weighted_matrix = matrix * weights
    table2 = pd.DataFrame(weighted_matrix, index=criteria, columns=criteria)
    table2["Weighted Sum"] = weighted_sum

    st.dataframe(table2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # TABLE 3 (CI CALCULATION)
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 3: Consistency Index Calculation</div>", unsafe_allow_html=True)

    ci_table = pd.DataFrame({
        "Criteria": criteria,
        "WSV/W": lambda_vals
    })

    st.dataframe(ci_table, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # TABLE 4 (FINAL RESULTS)
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Table 4: Final Consistency Results</div>", unsafe_allow_html=True)

    final_df = pd.DataFrame({
        "λmax": [lambda_max],
        "CI": [CI],
        "RI": [RI],
        "CR": [CR]
    })

    st.dataframe(final_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # CHARTS
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Weight Visualization</div>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.bar(criteria, weights)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.pie(weights, labels=criteria, autopct='%1.1f%%')
    st.pyplot(fig2)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PREMIUM FOOTER
# -----------------------------
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("""
<b>Developed by Anindo Paul Sourav</b><br>
Geology & Mining, University of Barishal<br><br>

🔗 LinkedIn: https://www.linkedin.com/in/anindo046/ <br>
🌐 Portfolio: https://anindo46.github.io/portfolio/ <br><br>

<b>Free for all users</b>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
