# Importing libraries
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

# Plot the dots on the world map
df.plot(ax=ax, color='red', alpha=0.6, markersize=100)

# Show the plot
plt.title('Dots on World Map')
plt.show()
