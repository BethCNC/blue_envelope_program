import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

print("Loading dataset...")
# Load dataset
df = pd.read_csv("data/blue_envelope_data.csv")
print(f"Loaded {len(df)} rows of data")

print("Loading U.S. state boundaries...")
# Load U.S. state boundaries (GeoJSON)
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
states = gpd.read_file(url)
print(f"Loaded {len(states)} states")

# Identify program adoption status
statewide_states = df[df["adoption_type"] == "Statewide"]["state"].unique()
local_states = df[df["adoption_type"] == "Local"]["state"].unique()
print(f"Statewide states: {statewide_states}")
print(f"Local states: {local_states}")

states["adoption_status"] = states["name"].apply(
    lambda x: "Statewide" if x in statewide_states
    else ("Local" if x in local_states else "None")
)

# Color mapping
colors = {"Statewide": "#2E8B57", "Local": "#FFD700", "None": "#D3D3D3"}

print("Creating map plot...")
# Plot the map
fig, ax = plt.subplots(figsize=(16, 10))
states.plot(ax=ax, color=states["adoption_status"].map(colors),
            edgecolor="black", linewidth=0.6)

# Add title and legend
for status, color in colors.items():
    ax.scatter([], [], color=color, label=status)
plt.legend(title="Blue Envelope Adoption", loc="lower left")
plt.title("Blue Envelope Program Adoption in the U.S. (2025)", fontsize=18, fontweight="bold")

print("Saving map to assets/output_map.png...")
plt.savefig("assets/output_map.png", dpi=300, bbox_inches='tight')
print("Static map saved successfully!")
