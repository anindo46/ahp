import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AHP Calculator", layout="wide")

# -----------------------------
# PREMIUM CSS
# -----------------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background-color: #eef1f5;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #6c757d;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* Table style */
.dataframe {
    border-radius: 10px !important;
    overflow: hidden;
}

/* Footer */
.footer {
    text-align: center;
    color: #6c757d;
    font-size: 14px;
    padding: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<div class='main-title'>AHP Calculator</div>", unsafe_allow_html=True)
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
# SAATY SCALE CARD
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Saaty Scale")

saaty_df = pd.DataFrame({
    "Scale": [1, 3, 5, 7, 9, "2,4,6,8"],
    "Meaning": [
        "Equal importance",
        "Moderate importance",
        "Strong importance",
        "Very strong importance",
        "Extreme importance",
        "Intermediate values"
    ],
    "Explanation": [
        "Two criteria contribute equally",
        "Slightly favor one over another",
        "Strongly favor one",
        "Dominance clearly evident",
        "Highest level of preference",
        "Between adjacent judgments"
    ]
})

st.dataframe(saaty_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# MATRIX INPUT CARD
# -----------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### Pairwise Comparison")

matrix = np.ones((n, n))
cols = st.columns(n)

for i in range(n):
    for j in range(i + 1, n):
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

df_matrix = pd.DataFrame(matrix, index=criteria, columns=criteria)

st.markdown("#### Pairwise Matrix")
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

    # -----------------------------
    # RESULTS CARD
    # -----------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Results")

    st.markdown("#### Normalized Matrix")
    st.dataframe(pd.DataFrame(norm_matrix, index=criteria, columns=criteria), use_container_width=True)

    st.markdown("#### Weights")
    df_weights = pd.DataFrame({"Criteria": criteria, "Weight": weights})
    st.dataframe(df_weights, use_container_width=True)

    st.markdown("#### Consistency")
    st.write(f"λmax = {lambda_max:.4f} | CI = {CI:.4f} | CR = {CR:.4f}")

    if CR < 0.1:
        st.success("Consistent")
    else:
        st.error("Not Consistent")

    # GIS weights
    gis_weights = weights / weights.sum() * 100
    df_gis = pd.DataFrame({
        "Criteria": criteria,
        "Weight (%)": np.round(gis_weights, 2)
    })

    st.markdown("#### Weights (%)")
    st.dataframe(df_gis, use_container_width=True)

    # Graph
    fig, ax = plt.subplots()
    ax.bar(criteria, weights)
    plt.xticks(rotation=45)
    plt.tight_layout()
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
