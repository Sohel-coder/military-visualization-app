import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Trade Dashboard", layout="wide")

# Load data
df = pd.read_csv("exports_imports_cleaned.csv")

# Derived column: Trade Balance
df['Trade Balance'] = df['Exports'] - df['Imports']

st.title("🌍 Global Trade Dashboard")
st.markdown("Analyze Exports, Imports, and Trade Balance Trends by Country")

# Sidebar filters
country_list = df['Country'].unique().tolist()
year_range = (df['Year'].min(), df['Year'].max())

selected_countries = st.sidebar.multiselect("Select Countries", country_list, default=country_list[:5])
selected_years = st.sidebar.slider("Select Year Range", year_range[0], year_range[1], (year_range[0], year_range[1]))

filtered_df = df[(df['Country'].isin(selected_countries)) & (df['Year'].between(*selected_years))]

# Line Chart: Exports and Imports
st.subheader("📈 Exports and Imports Over Time")
fig = px.line(filtered_df, x='Year', y=['Exports', 'Imports'], color='Country', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Trade Balance Choropleth Map
st.subheader("🗺️ Trade Balance by Country (Latest Year)")
latest_year = df['Year'].max()
latest_df = df[df['Year'] == latest_year]

fig_map = px.choropleth(latest_df,
                        locations="Country",
                        locationmode="country names",
                        color="Trade Balance",
                        color_continuous_scale="RdBu",
                        title=f"Trade Balance (Exports - Imports) in {latest_year}",
                        hover_name="Country")
st.plotly_chart(fig_map, use_container_width=True)

# Top Exporters and Importers
st.subheader("🏆 Top Exporting and Importing Countries")
top_exports = latest_df.nlargest(10, 'Exports')
top_imports = latest_df.nlargest(10, 'Imports')

col1, col2 = st.columns(2)
with col1:
    fig_exp = px.bar(top_exports, x='Country', y='Exports', color='Exports', title='Top Exporting Countries')
    st.plotly_chart(fig_exp, use_container_width=True)

with col2:
    fig_imp = px.bar(top_imports, x='Country', y='Imports', color='Imports', title='Top Importing Countries')
    st.plotly_chart(fig_imp, use_container_width=True)

# Export/Import Trend Forecast (Simple Linear Prediction)
st.subheader("🔮 Export/Import Growth Forecast (Linear Trend)")
selected_country = st.selectbox("Select a country to forecast", country_list)
country_df = df[df['Country'] == selected_country]

import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_trend(y_col):
    model = LinearRegression()
    X = country_df['Year'].values.reshape(-1, 1)
    y = country_df[y_col].values
    model.fit(X, y)
    future_years = np.arange(df['Year'].max() + 1, df['Year'].max() + 6).reshape(-1, 1)
    future_preds = model.predict(future_years)
    return future_years.flatten(), future_preds

exp_years, exp_forecast = forecast_trend('Exports')
imp_years, imp_forecast = forecast_trend('Imports')

fig_pred = go.Figure()
fig_pred.add_trace(go.Scatter(x=country_df['Year'], y=country_df['Exports'], mode='lines+markers', name='Exports'))
fig_pred.add_trace(go.Scatter(x=exp_years, y=exp_forecast, mode='lines', name='Export Forecast'))
fig_pred.add_trace(go.Scatter(x=country_df['Year'], y=country_df['Imports'], mode='lines+markers', name='Imports'))
fig_pred.add_trace(go.Scatter(x=imp_years, y=imp_forecast, mode='lines', name='Import Forecast'))
fig_pred.update_layout(title=f"{selected_country} - Export/Import Forecast", xaxis_title="Year", yaxis_title="Value")
st.plotly_chart(fig_pred, use_container_width=True)

st.markdown("---")
st.markdown("Developed by [Your Name or Team] 🌐")
