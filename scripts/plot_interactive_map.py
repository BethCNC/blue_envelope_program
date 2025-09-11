import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/blue_envelope_data.csv")

# Create interactive choropleth map
fig = px.choropleth(
    df,
    locations="state",
    locationmode="USA-states",
    color="coverage_type",
    color_discrete_map={
        "Statewide": "green",
        "Local": "gold",
        "None": "lightgrey"
    },
    scope="usa",
    title="Blue Envelope Program Adoption (Interactive)"
)

fig.update_layout(
    title_font=dict(size=22, family="Arial"),
    legend_title_text="Adoption Type"
)

fig.write_html("assets/interactive_map.html")
fig.show()
