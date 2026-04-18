import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AHP Professional Tool", layout="wide")

st.title("Analytic Hierarchy Process (AHP) Tool")
st.markdown("### Flood Hazard Mapping – Paper Ready Calculator")

# -----------------------------
# SIDEBAR INPUT
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
# FORMULAS (SIDE PANEL)
# -----------------------------
st.sidebar.markdown("### Formulas Used")

st.sidebar.latex(r"\lambda_{max} = \frac{1}{n} \sum \frac{(A \cdot W)_i}{W_i}")
st.sidebar.latex(r"CI = \frac{\lambda_{max} - n}{n - 1}")
st.sidebar.latex(r"CR = \frac{CI}{RI}")

# -----------------------------
# MATRIX INPUT
# -----------------------------
st.subheader("Pairwise Comparison Input")

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

st.markdown("### Pairwise Matrix")
st.dataframe(df_matrix, use_container_width=True)

# -----------------------------
# CALCULATE BUTTON
# -----------------------------
if st.button("Run AHP Analysis"):

    # -----------------------------
    # NORMALIZATION
    # -----------------------------
    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum

    df_norm = pd.DataFrame(norm_matrix, index=criteria, columns=criteria)

    # -----------------------------
    # WEIGHTS
    # -----------------------------
    weights = norm_matrix.mean(axis=1)

    df_weights = pd.DataFrame({
        "Criteria": criteria,
        "Weight": weights
    })

    # -----------------------------
    # WEIGHTED SUM
    # -----------------------------
    weighted_sum = np.dot(matrix, weights)

    df_ws = pd.DataFrame({
        "Criteria": criteria,
        "Weighted Sum": weighted_sum
    })

    # -----------------------------
    # LAMBDA MAX
    # -----------------------------
    lambda_vals = weighted_sum / weights
    lambda_max = np.mean(lambda_vals)

    # -----------------------------
    # CI & CR
    # -----------------------------
    CI = (lambda_max - n) / (n - 1)

    RI_dict = {
        1: 0, 2: 0, 3: 0.58, 4: 0.90,
        5: 1.12, 6: 1.24, 7: 1.32,
        8: 1.41, 9: 1.45, 10: 1.49
    }

    RI = RI_dict.get(n, 1.49)
    CR = CI / RI if RI != 0 else 0

    # -----------------------------
    # OUTPUT SECTION
    # -----------------------------
    st.success("AHP Calculation Completed")

    # Normalized matrix
    st.markdown("### Normalized Matrix")
    st.dataframe(df_norm, use_container_width=True)

    # Weights
    st.markdown("### Weights")
    st.dataframe(df_weights, use_container_width=True)

    # Weighted sum
    st.markdown("### Weighted Sum")
    st.dataframe(df_ws, use_container_width=True)

    # Lambda table
    st.markdown("### λ (Lambda Values)")
    df_lambda = pd.DataFrame({
        "Criteria": criteria,
        "Lambda_i": lambda_vals
    })
    st.dataframe(df_lambda, use_container_width=True)

    # Final consistency
    st.markdown("### Consistency Results")
    st.write(f"λmax = {lambda_max:.4f}")
    st.write(f"CI = {CI:.4f}")
    st.write(f"RI = {RI}")
    st.write(f"CR = {CR:.4f}")

    if CR < 0.1:
        st.success("Consistent (CR < 0.1)")
    else:
        st.error("Not Consistent (CR > 0.1)")

    # -----------------------------
    # GRAPH
    # -----------------------------
    st.markdown("### Weight Distribution")

    fig, ax = plt.subplots()
    ax.bar(criteria, weights)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    st.markdown("### Export")

    csv = df_weights.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Weights CSV",
        csv,
        "AHP_weights.csv",
        "text/csv"
    )
