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
    background-color: rgba(255,255,255,0.04);
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
.footer {
    text-align: center;
    color: #9aa0a6;
    font-size: 14px;
    padding-top: 20px;
}
.note {
    background-color: rgba(255,255,255,0.05);
    padding: 12px;
    border-left: 4px solid #4CAF50;
    border-radius: 6px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='title'>AHP Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analytic Hierarchy Process Tool</div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Input")

criteria_input = st.sidebar.text_area(
    "Criteria (comma separated)",
    "Elevation, Distance, Slope, TWI, Rainfall, Drainage_Density, Soil, Geology"
)

criteria = [c.strip() for c in criteria_input.split(",") if c.strip()]
n = len(criteria)

st.sidebar.write(f"Total Criteria: {n}")

# -----------------------------
# FORMULAS
# -----------------------------
st.sidebar.markdown("### Formulas")
st.sidebar.latex(r"\lambda_{max} = \frac{1}{n} \sum \frac{(A \cdot W)_i}{W_i}")
st.sidebar.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")
st.sidebar.latex(r"CR = \frac{CI}{RI}")

# -----------------------------
# RI TABLE
# -----------------------------
RI_dict = {
    1: 0, 2: 0, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32,
    8: 1.41, 9: 1.45, 10: 1.49
}

st.sidebar.markdown("### RI Table")
st.sidebar.dataframe(pd.DataFrame(list(RI_dict.items()), columns=["n", "RI"]))

# -----------------------------
# SAATY SCALE
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Saaty Scale (Saaty, 2000)</div>", unsafe_allow_html=True)

saaty_df = pd.DataFrame({
    "Scale": [1, 3, 5, 7, 9, "2,4,6,8"],
    "Meaning": ["Equal", "Moderate", "Strong", "Very Strong", "Extreme", "Intermediate"],
    "Explanation": [
        "Equal contribution",
        "Slightly favor",
        "Strongly favor",
        "Dominance evident",
        "Highest preference",
        "Between judgments"
    ]
})

st.dataframe(saaty_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PAIRWISE INPUT
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Pairwise Comparison</div>", unsafe_allow_html=True)

st.markdown("""
<div class='note'>
<b>N.B.</b> Use short variable names (El, Sl, Dis, DD) to avoid layout issues.
</div>
""", unsafe_allow_html=True)

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

df_matrix = pd.DataFrame(matrix, index=criteria, columns=criteria)
df_matrix["Row Sum"] = df_matrix.sum(axis=1)
df_matrix.loc["Column Sum"] = df_matrix.sum(axis=0)

st.dataframe(df_matrix, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# CALCULATION
# -----------------------------
if st.button("Run AHP"):

    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum
    weights = norm_matrix.mean(axis=1)

    weighted_sum = np.dot(matrix, weights)
    lambda_vals = weighted_sum / weights
    lambda_max = np.mean(lambda_vals)

    CI = (lambda_max - n) / (n - 1)
    RI = RI_dict.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Analytical Results Table (Normalized pairwise comparison matrix)</div>", unsafe_allow_html=True)

    norm_df = pd.DataFrame(norm_matrix, index=criteria, columns=criteria)

    table = norm_df.copy()
    table["Weighted Sum"] = weighted_sum
    table["Weight (W)"] = weights
    table["Lambda (WS/W)"] = lambda_vals

    st.dataframe(table, use_container_width=True)

    st.markdown("#### Key Metrics")
    st.write(f"λmax = {lambda_max:.3f}")
    st.write(f"CI = {CI:.3f}")
    st.write(f"CR = {CR:.3f}")

    st.markdown("#### Weights (%)")
    st.dataframe(pd.DataFrame({
        "Criteria": criteria,
        "Weight (%)": np.round(weights * 100, 2)
    }), use_container_width=True)

    st.markdown("#### Weight Distribution")
    fig, ax = plt.subplots()
    ax.bar(criteria, weights)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("""
Anindo Paul Sourav  
Geology and Mining, University of Barishal  
anindo.glm@gmail.com
""")
st.markdown("</div>", unsafe_allow_html=True)
