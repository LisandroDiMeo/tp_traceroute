# Importing libraries
import matplotlib.colors
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

data = pd.read_csv("./output_geo.csv")

df = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['long'], data['lat']))

# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the world map
world.plot(ax=ax, color='lightgray')

# Plot the dots on the world map with different colors based on the 'Category' column
categories = df['ip'].unique()
colors = list(matplotlib.colors.TABLEAU_COLORS.values())

for category, color in zip(categories, colors):
    df[df['ip'] == category].plot(ax=ax, markersize=100, color=color, alpha=0.7, label=category)

# Show the plot with a legend
plt.title('Dots on World Map')
plt.legend()
plt.show()