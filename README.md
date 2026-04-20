# Uber NYC Hot Zones

Identifying high-demand pickup areas across New York City using Uber trip data from April 2014 to June 2015.

## Overview

The goal of this project is to detect spatial clusters of Uber activity — referred to as "hot zones" — and visualize how demand shifts throughout the day across NYC taxi zones.

The analysis covers two datasets with different structures:
- **2014** (Apr–Sep): raw GPS coordinates, clustered using DBSCAN
- **2015** (Jan–Jun): zone-level data with LocationIDs, aggregated directly

## Approach

Raw trip records are grouped into 30-minute time windows. For the 2014 data, DBSCAN (`eps=0.01`, `min_samples=14`) is applied to each window to identify dense pickup areas. Each cluster is then mapped to its corresponding NYC taxi zone via a spatial join with the official TLC shapefile.

The 2015 data already includes zone identifiers, so it only requires aggregation and a merge with the shapefile centroids.

Both datasets are combined into a single table used by the Streamlit dashboard.

## Dashboard

An interactive choropleth map lets you explore pickup intensity by year, month, and 30-minute time slot.

Live demo: [huggingface.co/spaces/Alvlt/uber-hot-zones](https://huggingface.co/spaces/Alvlt/uber-hot-zones)

## Machine Learning

A binary classifier (XGBoost) is trained to predict whether a zone qualifies as a hot zone based on its location, time of day, and whether the date falls on a US public holiday. The dataset is heavily imbalanced (~3% hot zones), handled via `scale_pos_weight`.

The model reaches 84% accuracy with balanced precision and recall. That said, without features like weather or local event data, its predictive value beyond what the visualization already shows is limited.

## Stack

- **Clustering**: scikit-learn DBSCAN
- **Geospatial**: GeoPandas, NYC TLC shapefiles
- **Dashboard**: Streamlit, Plotly
- **ML**: XGBoost, scikit-learn Pipeline
- **Deployment**: Hugging Face Spaces (Docker)

## Data

- [Uber trip data — Kaggle](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city)
- [NYC TLC taxi zone shapefile](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)
