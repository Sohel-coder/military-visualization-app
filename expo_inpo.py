!pip install streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Trade Dashboard", layout="wide")

# Load data
df = pd.read_csv("/content/exports_imports_final.csv")

# Derived column: Trade Balance
df['trade_balance'] = df['export'] - df['import']

st.title("🌍 Global Trade Dashboard")
st.markdown("Analyze Exports, Imports, and Trade Balance Trends by Country")

# Sidebar filters
country_list = df['country'].unique().tolist()
year_range = (df['year'].min(), df['year'].max())  # Get numerical min/max years

selected_countries = st.sidebar.multiselect("Select Countries", country_list, default=country_list[:5])

# Use numerical year values for the slider
selected_years = st.sidebar.slider("Select Year Range", int(year_range[0]), int(year_range[1]), (int(year_range[0]), int(year_range[1]))) 

filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'].between(*selected_years))]

# Line Chart: Exports and Imports
st.subheader("📈 Exports and Imports Over Time")
fig = px.line(filtered_df, x='year', y=['export', 'import'], color='country', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Trade Balance Choropleth Map
st.subheader("🗺️ Trade Balance by Country (Latest Year)")
latest_year = df['year'].max()
latest_df = df[df['year'] == latest_year]

fig_map = px.choropleth(latest_df,
                        locations="country",
                        locationmode="country names",
                        color="trade_balance",
                        color_continuous_scale="RdBu",
                        title=f"Trade Balance (Exports - Imports) in {latest_year}",
                        hover_name="country")
st.plotly_chart(fig_map, use_container_width=True)

# Top Exporters and Importers
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

# Export/Import Trend Forecast (Simple Linear Prediction)
st.subheader("🔮 Export/Import Growth Forecast (Linear Trend)")
selected_country = st.selectbox("Select a country to forecast", country_list)
country_df = df[df['country'] == selected_country]

import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_trend(y_col):
    model = LinearRegression()
    X = country_df['year'].values.reshape(-1, 1)
    y = country_df[y_col].values
    model.fit(X, y)
    future_years = np.arange(df['year'].max() + 1, df['year'].max() + 6).reshape(-1, 1)
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

st.markdown("---")
st.markdown("Developed by Abhi & Sohel 🌐")
