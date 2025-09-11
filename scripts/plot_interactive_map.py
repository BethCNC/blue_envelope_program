import pandas as pd
import plotly.express as px

print("Loading dataset...")
# Load dataset
df = pd.read_csv("data/blue_envelope_data.csv")
print(f"Loaded {len(df)} rows of data")
print(f"Data columns: {df.columns.tolist()}")
print(f"Unique adoption types: {df['adoption_type'].unique()}")

print("Creating interactive choropleth map...")
# Create interactive choropleth map
fig = px.choropleth(
    df,
    locations="state",
    locationmode="USA-states",
    color="adoption_type",
    color_discrete_map={
        "Statewide": "green",
        "Local": "gold",
        "Pending Statewide": "orange",
        "None": "lightgrey"
    },
    scope="usa",
    title="Blue Envelope Program Adoption (Interactive)",
    hover_data=["localities", "implementation_year", "notes"]
)

fig.update_layout(
    title_font=dict(size=22, family="Arial"),
    legend_title_text="Adoption Type"
)

print("Saving interactive map to assets/interactive_map.html...")
fig.write_html("assets/interactive_map.html")
print("Interactive map saved successfully!")
