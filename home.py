import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title='The Art of War: A Comprehensive Visualization of World Military Strength',
    page_icon='🛡️',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://ssbcrackexams.com/wp-content/uploads/2024/06/Indian-Army.jpg');
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ The Art of War")
st.markdown("""
**An interactive data visualization that unveils the hidden dynamics of global defense. By seamlessly integrating trade data, missile inventories, military manpower, defense budgets, and power indexes.**

**Join us as we decode complex defense data into an engaging visual story of strength, strategy, and global influence.**
""", unsafe_allow_html=True)

# Load data
@st.cache_data

def load_data():
    exports_imports = pd.read_csv("exports_imports_final.csv")
    military_strength = pd.read_csv("military_strength_cleaned.csv")
    missiles = pd.read_csv("missiles_cleaned.csv")
    defence_budget = pd.read_csv("defence_budget_cleaned.csv", index_col=0)
    exports_imports['trade_balance'] = exports_imports['export'] - exports_imports['import']
    return exports_imports, military_strength, missiles, defence_budget

exports_imports, military_strength, missiles, defence_budget = load_data()

# Tabs for each section
trade_tab, military_tab, missile_tab, budget_tab = st.tabs(["📦 Trade Analysis", "🪖 Military Strength", "🚀 Missile Data", "💰 Defence Budget"])

# Trade Analysis
with trade_tab:
    st.header("📦 Trade Analysis: Exports, Imports, Trade Balance")
    country_list = exports_imports['country'].unique().tolist()
    year_range = (exports_imports['year'].min(), exports_imports['year'].max())

    selected_countries = st.multiselect("Select Countries", country_list, default=country_list[:5])
    selected_years = st.slider("Select Year Range", int(year_range[0]), int(year_range[1]), (int(year_range[0]), int(year_range[1])))

    filtered_df = exports_imports[(exports_imports['country'].isin(selected_countries)) & (exports_imports['year'].between(*selected_years))]

    st.subheader("📈 Exports and Imports Over Time")
    fig = px.line(filtered_df, x='year', y=['export', 'import'], color='country', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🗺️ Trade Balance by Country (Latest Year)")
    latest_year = exports_imports['year'].max()
    latest_df = exports_imports[exports_imports['year'] == latest_year]

    fig_map = px.choropleth(latest_df,
                            locations="country",
                            locationmode="country names",
                            color="trade_balance",
                            color_continuous_scale="RdBu",
                            title=f"Trade Balance (Exports - Imports) in {latest_year}",
                            hover_name="country")
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("🏆 Top Exporting and Importing Countries")
    top_exports = latest_df.nlargest(10, 'export')
    top_imports = latest_df.nlargest(10, 'import')

    col1, col2 = st.columns(2)
    with col1:
        fig_exp = px.bar(top_exports, x='country', y='export', color='export', title='Top Exporting Countries')
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        fig_imp = px.bar(top_imports, x='country', y='import', color='import', title='Top Importing Countries')
        st.plotly_chart(fig_imp, use_container_width=True)

    st.subheader("🔮 Export/Import Growth Forecast (Linear Trend)")
    selected_country = st.selectbox("Select a country to forecast", country_list)
    country_df = exports_imports[exports_imports['country'] == selected_country]

    def forecast_trend(y_col):
        model = LinearRegression()
        X = country_df['year'].values.reshape(-1, 1)
        y = country_df[y_col].values
        model.fit(X, y)
        future_years = np.arange(exports_imports['year'].max() + 1, exports_imports['year'].max() + 6).reshape(-1, 1)
        future_preds = model.predict(future_years)
        return future_years.flatten(), future_preds

    exp_years, exp_forecast = forecast_trend('export')
    imp_years, imp_forecast = forecast_trend('import')

    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=country_df['year'], y=country_df['export'], mode='lines+markers', name='Exports'))
    fig_pred.add_trace(go.Scatter(x=exp_years, y=exp_forecast, mode='lines', name='Export Forecast'))
    fig_pred.add_trace(go.Scatter(x=country_df['year'], y=country_df['import'], mode='lines+markers', name='Imports'))
    fig_pred.add_trace(go.Scatter(x=imp_years, y=imp_forecast, mode='lines', name='Import Forecast'))
    fig_pred.update_layout(title=f"{selected_country} - Export/Import Forecast", xaxis_title="Year", yaxis_title="Value")
    st.plotly_chart(fig_pred, use_container_width=True)

# Military Strength
with military_tab:
    st.header("🪖 Military Strength")
    metric = st.selectbox("Select a metric to compare", ["active_service_military_manpower", "total_military_aircraft_strength", "total_national_populations", "pwr_index"])
    fig = px.bar(military_strength.sort_values(metric, ascending=False).head(20),
                 x='country', y=metric, color='country', title=f"Top 20 Countries by {metric}")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Power Index vs Military Manpower")
    fig2 = px.scatter(military_strength, x='active_service_military_manpower', y='pwr_index',
                      color='country', size='total_military_aircraft_strength',
                      hover_name='country', title="Military Power Index Scatter Plot")
    st.plotly_chart(fig2, use_container_width=True)

# Missile Data
with missile_tab:
    st.header("🚀 Missile Data")
    family = st.selectbox("Select Missile Family", missiles['Family'].unique())
    df = missiles[missiles['Family'] == family]
    fig = px.bar(df, x='Name', y='Maximum range', color='Status', hover_data=['Type', 'Speed'],
                 title=f"Missile Ranges - {family}")
    st.plotly_chart(fig, use_container_width=True)

# Defence Budget
with budget_tab:
    st.header("💰 Defence Budget Trends")
    defence_budget.index.name = 'country'
    countries = defence_budget.index.tolist()
    selected = st.multiselect("Select countries", countries, default=[countries[0], countries[1]])
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

st.markdown("---")
