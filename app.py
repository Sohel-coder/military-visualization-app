import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df_trade = pd.read_csv("exports_imports_cleaned.csv")
    df_military = pd.read_csv("military_strength_cleaned.csv")
    df_missiles = pd.read_csv("missiles_cleaned.csv")
    df_budget = pd.read_csv("defence_budget_cleaned.csv")
    return df_trade, df_military, df_missiles, df_budget

df_trade, df_military, df_missiles, df_budget = load_data()

st.set_page_config(layout="wide")
st.title("🌍 Global Military & Trade Intelligence Dashboard")

# Trade Tab
st.header("📦 Trade Analysis")
country = st.selectbox("Select Country", sorted(df_trade['Country'].unique()))
df_country = df_trade[df_trade['Country'] == country]
st.line_chart(df_country.set_index("Year")[["Exports", "Imports", "Trade Balance"]])

# Military Tab
st.header("🪖 Military Strength Comparison")
strength_metric = st.selectbox("Select Strength Metric", ["Air Power", "Naval Power", "Manpower", "Power Index"])
fig = px.bar(df_military.sort_values(by=strength_metric, ascending=True).tail(10),
             x=strength_metric, y="Country", orientation='h', title=f"Top 10 Countries by {strength_metric}")
st.plotly_chart(fig, use_container_width=True)

# Missile Tab
st.header("🚀 Missile Overview")
missile_family = st.selectbox("Select Missile Family", df_missiles["Missile Family"].unique())
df_missile = df_missiles[df_missiles["Missile Family"] == missile_family]
st.dataframe(df_missile)
fig2 = px.scatter(df_missile, x="Range (km)", y="Speed (Mach)", color="Type",
                  hover_data=["Name"], title=f"{missile_family} Missile Capabilities")
st.plotly_chart(fig2, use_container_width=True)

# Defence Budget Tab
st.header("💰 Defence Budget by Country")
country_budgets = df_budget["Country"].unique()
countries_selected = st.multiselect("Select Countries", country_budgets, default=country_budgets[:3])
df_budget_filtered = df_budget[df_budget["Country"].isin(countries_selected)]
fig3 = px.line(df_budget_filtered, x="Year", y="Budget", color="Country", markers=True,
               title="Defense Budget Over Time")
st.plotly_chart(fig3, use_container_width=True)
