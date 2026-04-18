import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Flood Hazard AHP Tool", layout="wide")

# -----------------------------
# HEADER + LOGO
# -----------------------------
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Best for Flood Hazard Mapping</h1>
        <p><b>AHP-Based Multi-Criteria Decision Tool</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Simple logo (text-based)
st.markdown(
    """
    <div style='text-align:center; font-size:18px; padding:5px;'>
    🌊 <b>AHP Flood Tool</b> 🌍
    </div>
    """,
    unsafe_allow_html=True
)

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

st.sidebar.markdown("### Random Index (RI)")

ri_df = pd.DataFrame(list(RI_dict.items()), columns=["n", "RI"])
st.sidebar.dataframe(ri_df)

# -----------------------------
# SCALE IMAGE
# -----------------------------
st.markdown("### Saaty Scale Reference")

image = Image.open("/mnt/data/image.png")
st.image(image, use_container_width=True)

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
# CALCULATION
# -----------------------------
if st.button("Run AHP Analysis"):

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
    # TABLES
    # -----------------------------
    st.success("Calculation Complete")

    st.markdown("### Normalized Matrix")
    st.dataframe(pd.DataFrame(norm_matrix, index=criteria, columns=criteria), use_container_width=True)

    st.markdown("### Weights")
    df_weights = pd.DataFrame({"Criteria": criteria, "Weight": weights})
    st.dataframe(df_weights, use_container_width=True)

    st.markdown("### Weighted Sum")
    st.dataframe(pd.DataFrame({"Criteria": criteria, "Weighted Sum": weighted_sum}), use_container_width=True)

    st.markdown("### Lambda Values")
    st.dataframe(pd.DataFrame({"Criteria": criteria, "Lambda": lambda_vals}), use_container_width=True)

    # -----------------------------
    # CONSISTENCY
    # -----------------------------
    st.markdown("### Consistency Check")
    st.write(f"λmax = {lambda_max:.4f}")
    st.write(f"CI = {CI:.4f}")
    st.write(f"RI = {RI}")
    st.write(f"CR = {CR:.4f}")

    if CR < 0.1:
        st.success("Consistent (CR < 0.1)")
    else:
        st.error("Not Consistent (CR > 0.1)")

    # -----------------------------
    # GIS WEIGHTS
    # -----------------------------
    st.markdown("### GIS Usable Weights (%)")

    gis_weights = weights / weights.sum() * 100
    df_gis = pd.DataFrame({
        "Criteria": criteria,
        "Weight (%)": np.round(gis_weights, 2)
    })

    st.dataframe(df_gis, use_container_width=True)

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
    csv = df_gis.to_csv(index=False).encode("utf-8")
    st.download_button("Download GIS Weights", csv, "gis_weights.csv", "text/csv")

# -----------------------------
# FOOTER (CREDIT)
# -----------------------------
st.markdown("---")
st.markdown(
    """
    **Developed by:**  
    Anindo Paul Sourav  
    Geology and Mining, University of Barishal  
    Email: anindo.glm@gmail.com
    """
)
