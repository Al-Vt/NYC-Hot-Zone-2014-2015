import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st


# Loading the dataset containing all months
df = pd.read_csv("hot_zones.csv", low_memory=False)
# Loading NYC geographic zones
# And converting them to latitude and longitude
taxi_gdf = gpd.read_file("taxi_zones/taxi_zones.shp").to_crs("EPSG:4326")
# Converting the GeoDataFrame into GeoJSON format
geojson = json.loads(taxi_gdf.to_json())


# Streamlit
# Creating the sidebar filters section
st.sidebar.title("Filtres")
# Allowing the user to select the year
year = st.sidebar.radio("Année", [2014, 2015])
# Months depend on the selected year
months = df[df["source"] == year]["month"].unique().tolist()
month = st.sidebar.selectbox("Mois", months)
# Retrieving available hours
all_hours = sorted(df[(df["source"] == year) & (df["month"] == month)]["heure"].unique().tolist())
# The model is trained on 30-minute time intervals
hours = [h for h in all_hours if h.endswith(":00") or h.endswith(":30")]
# Slider to select the hour
heure = st.sidebar.select_slider("Heure", options=hours)


# Selecting a specific time window within a day
df_sel = df[(df["source"] == year) & (df["month"] == month) & (df["heure"] == heure)]
# Aggregating trips per zone and identifying hot zones
df_agg = df_sel.groupby("zone", as_index=False).agg(count=("count", "sum"), is_hot=("is_hot", "max"))


# Dynamic title
st.title(f"Uber Hot Zones NYC: {month} {year} to {heure}")

# Computing total Uber demand volume at a specific time
col1, col2, col3 = st.columns(3)
col1.metric("Trajets", int(df_agg["count"].sum()))
col2.metric("Hot zones", int(df_agg["is_hot"].sum()))
# Defining the most active zone
if not df_agg.empty:
    col3.metric("Most active zones", df_agg.loc[df_agg["count"].idxmax(), "zone"])

# Safety check if no data is available
if df_agg.empty:
    st.info("Aucune donnée pour cette sélection.")
else:
    # Interactive map based on zones
    fig = px.choropleth_mapbox(
        df_agg, geojson=geojson, locations="zone", featureidkey="properties.zone",
        color="count", color_continuous_scale="YlOrRd", mapbox_style="carto-positron",
        zoom=9.5, center={"lat": 40.7128, "lon": -74.0060}, opacity=0.7,
        hover_data={"zone": True, "count": True, "is_hot": True},
        labels={"count": "Trajets", "is_hot": "Hot zone"},
    )
    # Removing margins 
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600)
    st.plotly_chart(fig, use_container_width=True)
