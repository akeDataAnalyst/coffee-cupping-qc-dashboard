"""
Specialty Coffee Cupping QC Dashboard
Professional Lab Tool for Volcafe Specialty Analyst
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import BASE_DIR
from src.data_loader import load_cupping_data, validate_cupping_data
from src.utils import get_score_summary, get_region_performance

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Cupping QC Dashboard | Volcafe",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Coffee Cupping QC Dashboard")
st.markdown("**Modern Sensory Evaluation System • Aligned with SCA & ECX Standards**")

# ====================== LOAD DATA ======================
@st.cache_data
def get_data():
    df = load_cupping_data()
    return validate_cupping_data(df)

df = get_data()

# ====================== SIDEBAR FILTERS ======================
st.sidebar.header("Filter Cupping Records")

selected_regions = st.sidebar.multiselect(
    "Region", 
    options=df['region'].unique(),
    default=df['region'].unique()
)

selected_processing = st.sidebar.multiselect(
    "Processing Method",
    options=df['processing_method'].unique(),
    default=df['processing_method'].unique()
)

min_score = st.sidebar.slider(
    "Minimum Total Score", 
    min_value=80.0, 
    max_value=94.0, 
    value=85.0, 
    step=0.5
)

# Apply filters
filtered_df = df[
    (df['region'].isin(selected_regions)) &
    (df['processing_method'].isin(selected_processing)) &
    (df['total_score'] >= min_score)
]

# ====================== METRICS ======================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Samples", len(filtered_df))
with col2:
    st.metric("Avg SCA Score", f"{filtered_df['total_score'].mean():.2f}")
with col3:
    st.metric("Outstanding (88+)", len(filtered_df[filtered_df['total_score'] >= 88]))
with col4:
    st.metric("Avg Defects", f"{filtered_df['defects_per_300g'].mean():.1f}")

st.divider()

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["Score Overview", "Regional", "Detailed Records", "Export"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(filtered_df, x='total_score', color='quality_tier',
                          title="SCA Score Distribution", nbins=12)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(filtered_df, names='quality_tier', title="Quality Tier Breakdown")
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    region_perf = get_region_performance(filtered_df)
    st.dataframe(region_perf, use_container_width=True)

    fig3 = px.bar(
        filtered_df.groupby('region')['total_score'].mean().reset_index(),
        x='region', y='total_score', color='region',
        title="Average Score by Region"
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    display_cols = ['sample_id', 'lot_id', 'supplier_name', 'region', 'processing_method',
                   'total_score', 'quality_tier', 'defects_per_300g', 'flavor_notes']

    st.dataframe(
        filtered_df.sort_values('total_score', ascending=False)[display_cols],
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("Export Cupping Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "cupping_records.csv", "text/csv")

st.divider()

# Footer
st.caption("**Aklilu Abera | Specialty Analyst | Built with ECX, ICO & SCA Standards**")
