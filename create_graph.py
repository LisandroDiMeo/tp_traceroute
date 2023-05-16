# Importing libraries
import matplotlib.colors
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
from matplotlib.cm import get_cmap

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
#colors = list(matplotlib.colors.TABLEAU_COLORS.values())
cmap = get_cmap("tab20", 28)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors[0:len(df["ip"].unique())]

lines_per_target = {}
dfs_per_target = {}
for target in categories:
    values_of_target = df[df['target'] == target].geometry.values.tolist()
    dfs_per_target["target"] = df[df['target'] == target]
    lines_per_target[target] = LineString(values_of_target)



color_by_ip = {}
for category, color in zip(df["ip"].unique(), colors):
    color_by_ip[category] = color
    df[df['ip'] == category].plot(ax=ax, markersize=100, color=color, alpha=0.7, label=category)

# Plot the line connecting the dots
for line, color in zip(lines_per_target.values(), colors):
    gpd.GeoSeries([line]).plot(ax=ax, linewidth=2, linestyle='-', color=color, alpha=0.5)

colors_df = pd.DataFrame({"ip": list(color_by_ip.keys()), "color": list(color_by_ip.values())})
colors_df.to_csv("colors.csv", index=False)


def separate_dataframe(df_input):
    num_segments = len(df_input) - 1  # Calculate the number of segments based on the DataFrame length
    result = {}

    for i in range(num_segments):
        segment_df = df_input.iloc[i: i + 2]  # Extract two rows for each segment
        segment_name = f"segment{i + 1}"  # Generate a segment name
        result[segment_name] = segment_df  # Add the segment DataFrame to the result dictionary

    return result


# aux_colors = list(matplotlib.colors.TABLEAU_COLORS.values())
# for dft in dfs_per_target.values():
#     segments = separate_dataframe(dft)
#     for segment in segments.values():
#         values = segment.geometry.values.tolist()
#         line = LineString(values)
#         gpd.GeoSeries([line]).plot(ax=ax, linewidth=2, linestyle='-', color=aux_colors.pop(), alpha=0.5)
#     break

# Show the plot with a legend
plt.title('Dots on World Map')
plt.legend()
plt.show()