import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Global Defense Dashboard", layout="wide")

# Load data
@st.cache_data

def load_data():
    exports_imports = pd.read_csv("exports_imports_final.csv")
    military_strength = pd.read_csv("military_strength_cleaned.csv")
    missiles = pd.read_csv("missiles_cleaned.csv")
    defence_budget = pd.read_csv("defence_budget_cleaned.csv", index_col=0)
    return exports_imports, military_strength, missiles, defence_budget

exports_imports, military_strength, missiles, defence_budget = load_data()

st.title("🌍 Global Defense Data Visualization Dashboard")

# Sidebar
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Trade Analysis", "Military Strength", "Missile Data", "Defence Budget"])

# Trade Analysis
if section == "Trade Analysis":
    st.header("📦 Trade Analysis")
    countries = exports_imports['country'].unique()
    country = st.selectbox("Select a country", countries)
    df = exports_imports[exports_imports['country'] == country]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['financial_year(start)'], y=df['export'], mode='lines+markers', name='Export'))
    fig.add_trace(go.Scatter(x=df['financial_year(start)'], y=df['import'], mode='lines+markers', name='Import'))
    fig.add_trace(go.Scatter(x=df['financial_year(start)'], y=df['trade_balance'], mode='lines+markers', name='Trade Balance'))
    fig.update_layout(title=f"Trade Metrics Over Time - {country}", xaxis_title="Year", yaxis_title="USD (Millions)")
    st.plotly_chart(fig, use_container_width=True)

# Military Strength
elif section == "Military Strength":
    st.header("🪖 Military Strength")
    metric = st.selectbox("Select a metric to compare", [
        "active_service_military_manpower",
        "total_military_aircraft_strength",
        "total_national_populations",
        "pwr_index"])

    fig = px.bar(military_strength.sort_values(metric, ascending=False).head(20),
                 x='country', y=metric, color='country', title=f"Top 20 Countries by {metric}")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Power Index vs Military Manpower")
    fig2 = px.scatter(military_strength, x='active_service_military_manpower', y='pwr_index',
                      color='country', size='total_military_aircraft_strength',
                      hover_name='country', title="Military Power Index Scatter Plot")
    st.plotly_chart(fig2, use_container_width=True)

# Missile Data
elif section == "Missile Data":
    st.header("🚀 Missile Data")
    family = st.selectbox("Select Missile Family", missiles['Family'].unique())
    df = missiles[missiles['Family'] == family]
    fig = px.bar(df, x='Name', y='Maximum range', color='Status', hover_data=['Type', 'Speed'],
                 title=f"Missile Ranges - {family}")
    st.plotly_chart(fig, use_container_width=True)

# Defence Budget
elif section == "Defence Budget":
    st.header("💰 Defence Budget Trends")
    defence_budget.index.name = 'country'
    countries = defence_budget.index.tolist()
    selected = st.multiselect("Select countries", countries, default=countries[:2])
    df = defence_budget.loc[selected].T
    df.index.name = "Year"
    df = df.reset_index()
    df_melt = df.melt(id_vars='Year', var_name='Country', value_name='Budget %')

    fig = px.line(df_melt, x='Year', y='Budget %', color='Country', markers=True,
                  title="Defence Budget Over Years")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Heatmap of Budgets")
    heatmap_df = defence_budget.loc[selected].dropna(axis=1, how='all')
    fig2 = px.imshow(heatmap_df, labels=dict(x="Year", y="Country", color="Budget %"),
                     aspect="auto")
    st.plotly_chart(fig2, use_container_width=True)
