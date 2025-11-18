import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Sellers Dashboard", layout="wide")

st.title("📊 Sellers Dashboard — Excel ➜ CSV Converter")

# Upload .xlsx or .xls file
uploaded_file = st.file_uploader("Upload sellers.xlsx file", type=["xlsx", "xls"])


# =======================================================================
#                      KPI CARD CSS (GLOBAL)
# =======================================================================
# This section adds custom CSS to style KPI cards: colors, rounded borders, shadows, etc
st.markdown("""
<style>
.kpi-card {
    padding: 20px 25px;
    border-radius: 18px;
    background-color: #ffffff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.kpi-title {
    font-size: 24px;
    font-weight: 700;
    color: #2d2d2d;
}
.kpi-sub {
    font-size: 15px;
    color: #6e6e6e;
    margin-top: -10px;
}
.kpi-value {
    font-size: 38px;
    font-weight: 700;
    margin-top: -5px;
    color: #1a1a1a;
}
.delta-green {
    background: #d4f7d4;
    color: #0a8a0a;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
    display: inline-block;
}
.delta-red {
    background: #ffd6d6;
    color: #c40000;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 14px;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)



# =======================================================================
#                      MAIN LOGIC - ONLY RUNS IF USER UPLOADED A FILE
# =======================================================================
if uploaded_file is not None:

    # -----------------------------
    # LOAD DATA FROM EXCEL
    # -----------------------------
    df = pd.read_excel(uploaded_file)

    # Sort by date if exists
    if "Date" in df.columns:
        df = df.sort_values("Date")

    # -----------------------------
    # CALCULATE MARGINAL REVENUE
    # -----------------------------
    if {"INCOME", "SOLD UNITS"}.issubset(df.columns):

        df["Marginal_Revenue"] = df["INCOME"].diff() / df["SOLD UNITS"].diff()
        df["Marginal_Revenue"] = df["Marginal_Revenue"].round(2)

    else:
        df["Marginal_Revenue"] = pd.NA

    # ----------------------------------------
    # KPIs SECTION — Summary of performance
    # ----------------------------------------
    st.header("📌 Business Overview")

    income_col = df["INCOME"]
    units_col = df["SOLD UNITS"]
    mr_col = df["Marginal_Revenue"].dropna()
    # Calculate totals and averages
    total_income = income_col.sum()
    total_units = units_col.sum()
    avg_mr = mr_col.mean() if not mr_col.empty else 0

    # Deltas (last vs previous value)
    delta_income = income_col.iloc[-1] - income_col.iloc[-2] if len(income_col) > 1 else 0
    delta_units = units_col.iloc[-1] - units_col.iloc[-2] if len(units_col) > 1 else 0
    delta_mr = mr_col.iloc[-1] - mr_col.iloc[-2] if len(mr_col) > 1 else 0

    # ---- KPI layout (3 cards)
    col1, col2, col3 = st.columns(3)
    # ---------------- KPI 1 — TOTAL INCOME ----------------
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Income (Revenue)</div>
            <div class="kpi-sub">Accumulated Total</div>
            <div class="kpi-value">${total_income:,.2f}</div>
            <div class="{ 'delta-green' if delta_income >=0 else 'delta-red'}">
                {"▲" if delta_income >=0 else "▼"} {delta_income:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    # ---------------- KPI 2 — UNITS SOLD ----------------
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Units Sold</div>
            <div class="kpi-sub">Total Units</div>
            <div class="kpi-value">{total_units:,}</div>
            <div class="{ 'delta-green' if delta_units >=0 else 'delta-red'}">
                {"▲" if delta_units >=0 else "▼"} {delta_units:,.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    # ---------------- KPI 3 — AVERAGE MR ----------------
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg. Marginal Revenue (MR)</div>
            <div class="kpi-sub">Average Change</div>
            <div class="kpi-value">${avg_mr:.2f}</div>
            <div class="{ 'delta-green' if delta_mr >=0 else 'delta-red'}">
                {"▲" if delta_mr >=0 else "▼"} {delta_mr:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)



    # -----------------------------
    # DATASET PREVIEW
    # -----------------------------
    st.subheader("📄 Dataset Preview")
    st.dataframe(df, width="stretch")



    # ===================================================================
    # VISUALIZATIONS
    # ===================================================================
    st.header("📈 Data Visualizations")
     # Create grid layout for 4 graphs
    g1, g2 = st.columns(2)
    g3, g4 = st.columns(2)

    # # Detect if dataset contains a region column
    region_col = None
    for c in ["REGION", "Region", "region"]:
        if c in df.columns:
            region_col = c

    # ---------------- VISUAL 1 — Revenue by Region ----------------
    if region_col:
        fig1 = px.bar(
            df.groupby(region_col)["INCOME"].sum().reset_index(),
            x=region_col,
            y="INCOME",
            color=region_col,   # 🔥 adds color
            title="Revenue by Region"
        )
        g1.plotly_chart(fig1, use_container_width=True)

    # ---------------- VISUAL 2 — Units Sold by Region ----------------
    if region_col:
        fig2 = px.bar(
            df.groupby(region_col)["SOLD UNITS"].sum().reset_index(),
            x=region_col,
            y="SOLD UNITS",
            color=region_col,   # 🔥 adds color
            title="Units Sold by Region"
        )
        g2.plotly_chart(fig2, use_container_width=True)

    # ---------------- VISUAL 3 — Marginal Revenue Trend ----------------
    fig3 = px.line(
        df,
        y="Marginal_Revenue",
        color=region_col if region_col else None,  # 🔥 color by region if exists
        title="Marginal Revenue Trend"
    )
    g3.plotly_chart(fig3, use_container_width=True)

    # ---------------- VISUAL 4 — Income vs Units Sold ----------------
    fig4 = px.scatter(
        df,
        x="SOLD UNITS",
        y="INCOME",
        color=region_col if region_col else None,  # 🔥 color by region
        size="TOTAL SALES" if "TOTAL SALES" in df.columns else None,
        title="Income vs Units Sold"
    )
    g4.plotly_chart(fig4, use_container_width=True)
    # -----------------------------
    # REGION FILTER
    # -----------------------------
    st.header("🌎 Region Filter")
    st.markdown(
    "<p style='color: gray; font-size: 15px;'>Filtering by region will also filter the vendor list below. The Vendor Lookup section only shows vendors from the selected region.</p>",
    unsafe_allow_html=True
    )
    # Detect region column again
    region_col = None
    for candidate in ["REGION", "Region", "region"]:
        if candidate in df.columns:
                region_col = candidate
        break

    if region_col:
        regions = sorted(df[region_col].dropna().unique())
        selection = st.selectbox("Select a region:", regions)

        df_filtered = df[df[region_col] == selection]

        st.write(f"### Region: {selection}")
        st.dataframe(df_filtered, width="stretch")
    else:
        st.warning("No REGION column detected.")

    # -----------------------------
    # VENDOR LOOKUP
    # -----------------------------
    st.markdown("<h2 style='color:#FF7F50;'>🔎 Vendor Lookup</h2>", unsafe_allow_html=True)
    # Detect vendor column (case-insensitive)
    vendor_col = None
    for candidate in ["NAME", "Name", "name"]:
        if candidate in df.columns:
            vendor_col = candidate
            break

    if vendor_col:
        vendors = sorted(df_filtered[vendor_col].dropna().unique())
        vendor_selected = st.selectbox("Select a vendor:", vendors)

        df_vendor = df_filtered[df_filtered[vendor_col] == vendor_selected]

        st.subheader(f"Results for: **{vendor_selected}**")

        # Colorful table
        st.dataframe(
            df_vendor.style.background_gradient(cmap="viridis"),
            use_container_width=True
        )
    else:
        st.warning("⚠️ There is no NAME column in the dataset.")

    # ===================================================================
    # DOWNLOAD CSV
    # ===================================================================
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download Full CSV",
        data=csv_data,
        file_name="sellers_converted.csv",
        mime="text/csv"
    )
