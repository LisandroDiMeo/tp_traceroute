# Importing libraries
import matplotlib.colors
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

data = pd.read_csv("./output_geo.csv")

df = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['long'], data['lat']))


# Load the world map shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a figure and axes
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the world map
world.plot(ax=ax, color='lightgray')

# Plot the dots on the world map with different colors based on the 'Category' column
categories = df['target'].unique()
colors = list(matplotlib.colors.TABLEAU_COLORS.values())


lines_per_target = {}
for target in categories:
    values_of_target = df[df['target'] == target].geometry.values.tolist()
    lines_per_target[target] = LineString(values_of_target)

for category, color in zip(categories, colors):
    df[df['target'] == category].plot(ax=ax, markersize=100, color=color, alpha=0.7, label=category)

# Plot the line connecting the dots
for line,color in zip(lines_per_target.values(), colors):
    gpd.GeoSeries([line]).plot(ax=ax, linewidth=2, linestyle='-', color=color, alpha=0.5)

# Show the plot with a legend
plt.title('Dots on World Map')
plt.legend()
plt.show()