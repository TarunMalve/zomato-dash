import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils.data_loader import load_data

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Zomato Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
)

ZOMATO_RED = "#E23744"

# ── Data loading ────────────────────────────────────────────────────────────

@st.cache_data
def get_data() -> pd.DataFrame:
    return load_data("data/zomato.csv")


df_raw = get_data()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<h1 style='color:{ZOMATO_RED};'>🍽️ Zomato</h1>"
        "<p style='color:gray;font-size:14px;'>Analytics Dashboard</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Location filter
    all_locations = sorted(df_raw["location"].dropna().unique().tolist())
    selected_locations = st.multiselect(
        "📍 Location",
        options=all_locations,
        default=all_locations,
        help="Filter by restaurant location.",
    )

    # Listed-in type filter
    type_col = "listed_in(type)"
    all_types = sorted(df_raw[type_col].dropna().unique().tolist())
    selected_types = st.multiselect(
        "🗂️ Listed In (Type)",
        options=all_types,
        default=all_types,
        help="Filter by dining category.",
    )

    # Online order filter
    online_filter = st.radio(
        "🛵 Online Order",
        options=["All", "Yes", "No"],
        index=0,
        horizontal=True,
    )

    st.divider()

# ── Apply filters ────────────────────────────────────────────────────────────
df = df_raw.copy()

if selected_locations:
    df = df[df["location"].isin(selected_locations)]
if selected_types:
    df = df[df[type_col].isin(selected_types)]
if online_filter != "All":
    df = df[df["online_order"] == online_filter]

# Sidebar record count expander
with st.sidebar:
    with st.expander("ℹ️ Data Info"):
        st.metric("Records after filter", len(df))

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    f"<h1 style='color:{ZOMATO_RED};'>🍽️ Zomato Analytics Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown("Actionable insights into Bangalore's dining landscape.")
st.divider()

# ── Section 1: KPI Cards ─────────────────────────────────────────────────────
st.subheader("📊 Executive Summary")

cost_col = "approx_cost(for two people)"

total_restaurants = df["name"].nunique()
total_votes = int(df["votes"].sum()) if "votes" in df.columns else 0
avg_votes = round(df["votes"].mean(), 1) if "votes" in df.columns else 0.0
median_cost = df[cost_col].median() if cost_col in df.columns else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("🏠 Total Restaurants", f"{total_restaurants:,}")
kpi2.metric("👍 Total Votes", f"{total_votes:,}")
kpi3.metric("📈 Avg Votes / Restaurant", f"{avg_votes:,.1f}")
kpi4.metric("💰 Median Cost for Two", f"₹{median_cost:,.0f}")

st.divider()

# ── Section 2: Market Segmentation ───────────────────────────────────────────
st.subheader("🏪 Market Segmentation")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Service Analysis** – Online Order × Book Table")
    service_df = (
        df.groupby(["online_order", "book_table"])
        .size()
        .reset_index(name="count")
    )
    fig_service = px.bar(
        service_df,
        x="online_order",
        y="count",
        color="book_table",
        barmode="group",
        labels={
            "online_order": "Online Order",
            "count": "Number of Restaurants",
            "book_table": "Book Table",
        },
        color_discrete_map={"Yes": ZOMATO_RED, "No": "#AAAAAA"},
    )
    fig_service.update_layout(legend_title_text="Book Table", height=380)
    st.plotly_chart(fig_service, use_container_width=True)

with col_right:
    st.markdown("**Restaurant Type Distribution** – Top 15")
    if "rest_type" in df.columns:
        rest_type_counts = (
            df["rest_type"]
            .value_counts()
            .head(15)
            .reset_index()
        )
        rest_type_counts.columns = ["rest_type", "count"]
        rest_type_counts = rest_type_counts.sort_values("count")
        fig_rest = px.bar(
            rest_type_counts,
            x="count",
            y="rest_type",
            orientation="h",
            labels={"rest_type": "Restaurant Type", "count": "Count"},
            color_discrete_sequence=[ZOMATO_RED],
        )
        fig_rest.update_layout(height=380)
        st.plotly_chart(fig_rest, use_container_width=True)

st.divider()

# ── Section 3: Performance & Rating Analytics ─────────────────────────────────
st.subheader("⭐ Performance & Rating Analytics")

# 3a — Cuisine Leaderboard (full width)
st.markdown("**Cuisine Leaderboard** – Top 15 by Average Rating")
if "cuisines" in df.columns:
    cuisine_df = df[["cuisines", "rate"]].dropna(subset=["rate"])
    cuisine_df = cuisine_df.copy()
    cuisine_df["cuisine_split"] = cuisine_df["cuisines"].str.split(",")
    cuisine_exploded = cuisine_df.explode("cuisine_split")
    cuisine_exploded["cuisine_split"] = cuisine_exploded["cuisine_split"].str.strip()
    cuisine_avg = (
        cuisine_exploded.groupby("cuisine_split")["rate"]
        .mean()
        .reset_index()
        .rename(columns={"cuisine_split": "Cuisine", "rate": "Avg Rating"})
        .nlargest(15, "Avg Rating")
        .sort_values("Avg Rating")
    )
    fig_cuisine = px.bar(
        cuisine_avg,
        x="Avg Rating",
        y="Cuisine",
        orientation="h",
        color="Avg Rating",
        color_continuous_scale="YlOrRd",
        labels={"Avg Rating": "Average Rating"},
    )
    fig_cuisine.update_layout(coloraxis_showscale=True, height=420)
    st.plotly_chart(fig_cuisine, use_container_width=True)

col3a, col3b = st.columns(2)

with col3a:
    st.markdown("**Correlation Heatmap**")
    numeric_cols = [c for c in [cost_col, "votes", "rate"] if c in df.columns]
    corr_df = df[numeric_cols].dropna()
    if len(corr_df) > 1:
        corr_matrix = corr_df.corr()
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            labels={"color": "Pearson r"},
        )
        fig_heat.update_layout(height=380)
        st.plotly_chart(fig_heat, use_container_width=True)

with col3b:
    st.markdown("**Location Performance** – Top 15 by Avg Rating")
    city_col = "listed_in(city)"
    if city_col in df.columns:
        loc_avg = (
            df.groupby(city_col)["rate"]
            .mean()
            .dropna()
            .reset_index()
            .rename(columns={city_col: "City", "rate": "Avg Rating"})
            .nlargest(15, "Avg Rating")
            .sort_values("Avg Rating")
        )
        fig_loc = px.bar(
            loc_avg,
            x="Avg Rating",
            y="City",
            orientation="h",
            color="Avg Rating",
            color_continuous_scale="YlOrRd",
            labels={"Avg Rating": "Average Rating"},
        )
        fig_loc.update_layout(height=380)
        st.plotly_chart(fig_loc, use_container_width=True)

st.divider()

# ── Section 4: Deep Dive Explorations ─────────────────────────────────────────
st.subheader("🔍 Deep Dive Explorations")
col4a, col4b = st.columns(2)

with col4a:
    st.markdown("**Cost Distribution by Online Order Status**")
    cost_df = df[[cost_col, "online_order"]].dropna(subset=[cost_col])
    fig_hist = px.histogram(
        cost_df,
        x=cost_col,
        color="online_order",
        nbins=30,
        barmode="overlay",
        opacity=0.75,
        labels={cost_col: "Approx Cost for Two (₹)", "online_order": "Online Order"},
        color_discrete_map={"Yes": ZOMATO_RED, "No": "#AAAAAA"},
    )
    fig_hist.update_layout(legend_title_text="Online Order", height=380)
    st.plotly_chart(fig_hist, use_container_width=True)

with col4b:
    st.markdown("**Votes vs. Rating**")
    scatter_df = df[["votes", "rate", type_col, "name"]].dropna(
        subset=["votes", "rate"]
    )
    fig_scatter = px.scatter(
        scatter_df,
        x="votes",
        y="rate",
        color=type_col,
        hover_name="name",
        labels={
            "votes": "Total Votes",
            "rate": "Rating",
            type_col: "Listed In (Type)",
        },
        opacity=0.8,
    )
    fig_scatter.update_layout(height=380)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Zomato Analytics Dashboard © 2026 | Built with Streamlit & Plotly")
