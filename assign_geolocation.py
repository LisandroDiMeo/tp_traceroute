import geoip2.database
import pandas as pd

traceroute_df = pd.read_csv("./output.csv")
traceroute_df["source_and_target"] = traceroute_df["ip"] + "-" + traceroute_df["target"]

location_dict = {
    "source_and_target": [],
    "lat": [],
    "long": [],
    "city": [],
    "country": [],
}

# This reader object should be reused across lookups as creation of it is
# expensive.
with geoip2.database.Reader('geo.mmdb') as reader:
    for src_and_target in traceroute_df["source_and_target"]:
        split_src = src_and_target.split("-")
        ip = split_src[0]
        target = split_src[1]
        if ip == "192.168.0.1":
            lat = "-34.58881517251069"
            lng = "-58.420968605233796"
            location_dict["source_and_target"].append(src_and_target)
            location_dict["lat"].append(lat)
            location_dict["long"].append(lng)
            location_dict["city"].append("Buenos Aires")
            location_dict["country"].append("Argentina")
            continue
        response = reader.city(ip)
        location_dict["source_and_target"].append(src_and_target)
        location_dict["lat"].append(response.location.latitude)
        location_dict["long"].append(response.location.longitude)
        location_dict["city"].append(response.city.name if response.city.name is not None else "")
        location_dict["country"].append(response.country.name if response.country.name is not None else "")

df = pd.DataFrame(location_dict)

merged = pd.merge(traceroute_df, df, on="source_and_target")
df.to_csv("output_geo_aux.csv", index=False)
merged.to_csv('output_geo.csv', index=False)
