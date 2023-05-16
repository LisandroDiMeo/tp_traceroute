import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.cm import get_cmap


data = pd.read_csv("./output_geo.csv")
df = pd.DataFrame(data)
fig, ax = plt.subplots()

# get a color map
cmap = get_cmap("tab20", 28)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list

ips = df['ip']
mean_rtt = df['mean_rtt']

ax.bar(ips, mean_rtt, color=colors)
ax.set_ylabel('Mean RTT in ms')
ax.set_title('Mean RTT for each hop between ips')


plt.xticks(rotation=15)
plt.show()