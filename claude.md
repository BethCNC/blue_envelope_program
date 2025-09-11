# Blue Envelope Program Infographic – Claude Code Agent Guide

## Overview

This guide explains how to build a data‑driven map for the **Blue Envelope Program**, a traffic–stop communication initiative for neurodivergent drivers.  You will be working in a Python environment to produce both static and interactive visualisations that highlight where the program has been adopted across the United States.

The finished deliverable should show:

* **Statewide adoption** — colour entire states **blue** when the program has been rolled out statewide.
* **Local adoption** — plot **blue dots** at the approximate location of each county or town that runs a local programme, while leaving their host states grey.
* **No adoption** — leave states with no programme in a neutral light‑grey tone.

## Data Source

The project relies on the enhanced dataset provided in `data/blue_envelope_data.csv`.  Each row describes a US state and includes:

| Column             | Description                                                                                                      |
|--------------------|------------------------------------------------------------------------------------------------------------------|
| `state`            | Two‑letter postal abbreviation or full name of the state.                                                        |
| `adopted`          | Boolean indicating whether any Blue Envelope programme exists in that state.                                      |
| `adoption_type`    | One of `Statewide`, `Local`, `Pending`, or `None`.  Use this to decide whether to colour the whole state.        |
| `localities`       | Comma‑ or semicolon‑separated list of counties or towns that operate a local programme (empty if none).           |
| `implementation_year` | Year the programme was introduced in that jurisdiction (optional for context).                                  |
| `notes`            | Free‑form notes summarising notable facts or legislation about the programme in that state.                       |

Always read from this file — do **not** invent locations or alter adoption statuses in code.  When updating the data, modify the CSV only after verifying new programmes.

## Recommended Libraries

The existing code uses `geopandas` and `matplotlib` for static maps and `plotly.express` for interactive choropleths.  For a richer interactive experience with point markers we recommend switching to **Folium**:

* **Pandas** – for CSV ingestion and data wrangling.
* **GeoPandas** – to load US state boundaries as polygons.
* **Matplotlib** – to create a simple static image where statewide states are filled blue and local states remain grey with overlaid points.
* **Folium** – to build an interactive leaflet map with hover/click tooltips.  Folium makes it straightforward to colour polygons and place markers.
* **Geopy** (optional) – to geocode county or town names into latitude/longitude coordinates.  If offline or geocoding is unavailable, approximate coordinates can be supplied manually.

Add the following line to `requirements.txt` if Folium is not yet installed:

```
folium
geopy
```

## Workflow for the Claude Code Agent

Follow the steps below to generate the infographic.  Each step can be encapsulated as a separate function or script for clarity.

### 1 – Environment Setup

1. Ensure the Python environment has the necessary packages installed.  Run:
   ```bash
   pip install -r requirements.txt
   ```
   If `folium` or `geopy` are missing, append them to `requirements.txt` and reinstall.
2. Confirm that `data/blue_envelope_data.csv` exists in the repository and matches the expected schema.

### 2 – Load Data

1. Read the CSV using `pandas.read_csv("data/blue_envelope_data.csv")`.
2. Create three lists based on the `adoption_type` column:
   * `statewide_states` — states where `adoption_type` equals `Statewide`.
   * `local_states` — states where `adoption_type` equals `Local`.
   * `pending_states` — states where `adoption_type` equals `Pending` (optional special colour or pattern).

### 3 – Parse Localities

For states with local programmes (`adoption_type == 'Local'`), parse the `localities` field into a list of county/town names.  Strip whitespace and ignore empty values.  If geocoding is available, resolve each locality to coordinates:

```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="blue-envelope-mapper")

def geocode_locality(locality, state):
    try:
        location = geolocator.geocode(f"{locality}, {state}", timeout=10)
        return (location.latitude, location.longitude) if location else None
    except Exception:
        return None

locality_coords = []
for _, row in df.iterrows():
    if row['adoption_type'] == 'Local' and isinstance(row['localities'], str):
        for place in [p.strip() for p in row['localities'].replace(';', ',').split(',') if p.strip()]:
            coords = geocode_locality(place, row['state'])
            if coords:
                locality_coords.append({
                    'state': row['state'],
                    'place': place,
                    'lat': coords[0],
                    'lon': coords[1]
                })
```

If internet access is unavailable or geocoding fails, you may choose to define a small dictionary of latitude/longitude centroids for known counties or towns.  Approximate coordinates are sufficient for visual context.

### 4 – Load Geospatial Boundaries

Use GeoPandas to load a US states GeoJSON file:

```python
import geopandas as gpd
states = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")

# Create a mapping from state name or abbreviation to adoption status
def classify_state(name):
    if name in statewide_states:
        return 'Statewide'
    elif name in local_states:
        return 'Local'
    elif name in pending_states:
        return 'Pending'
    else:
        return 'None'

states['adoption_status'] = states['name'].apply(classify_state)
```

### 5 – Generate Static Map

1. Define a colour palette:
   * Statewide → `#1e90ff` (DodgerBlue) – full fill.
   * Local → `#d3d3d3` (LightGrey) – neutral fill.
   * Pending → `#b0c4de` (LightSteelBlue) – optional distinct fill.
   * None → `#f0f0f0` (VeryLightGrey).
2. Plot the states using `states.plot` in `matplotlib`, colouring by `adoption_status` using the palette above.
3. Loop through `locality_coords` and overlay each as a small blue marker on the map:
   ```python
   for loc in locality_coords:
       ax.plot(loc['lon'], loc['lat'], marker='o', markersize=4, color='#1e90ff')
   ```
4. Add a legend explaining colours and save the figure to `assets/state_local_map.png`.

### 6 – Generate Interactive Map

1. Create a Folium map centred on the continental US:
   ```python
   import folium
   m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles='CartoDB positron')
   ```
2. Convert `states` to GeoJSON and add a `folium.Choropleth` layer:
   ```python
   choropleth = folium.Choropleth(
       geo_data=states.__geo_interface__,
       name='States',
       data=states,
       columns=['name', 'adoption_status'],
       key_on='feature.properties.name',
       fill_color='Blues',
       fill_opacity=0.6,
       line_opacity=0.5,
       legend_name='Blue Envelope Adoption'
   )
   choropleth.add_to(m)
   ```
   You can customise the palette or supply a dictionary mapping statuses to colours for finer control.
3. Add markers for local programmes:
   ```python
   for loc in locality_coords:
       folium.CircleMarker(
           location=(loc['lat'], loc['lon']),
           radius=5,
           color='#1e90ff',
           fill=True,
           fill_color='#1e90ff',
           fill_opacity=0.8,
           tooltip=f"{loc['place']}, {loc['state']}"
       ).add_to(m)
   ```
4. Save the interactive map to `assets/state_local_map.html` using `m.save()`.

### 7 – Automation Rules

* **Data integrity** – Always load adoption data from `data/blue_envelope_data.csv`.  Do not fabricate or infer programme locations.  When updates occur, commit them to the CSV via a separate data‑updating process.
* **Colour consistency** – Use the specified blue (`#1e90ff`) for both statewide fills and locality markers.  Use neutral greys for states without programmes.  Document any additional colour choices in comments.
* **Output locations** – Save the static image and interactive HTML into the `assets/` directory.  Do not overwrite unrelated files.
* **Reusability** – Encapsulate map creation logic in functions (e.g., `create_static_map()` and `create_interactive_map()`) so they can be imported by automation scripts or notebooks.
* **Logging** – When geocoding fails for a locality, log a warning and continue.  It is acceptable for a few markers to be missing; the map will still show statewide adoption correctly.

## Further Enhancements

* **Tooltips and Popups** – Extend the interactive map by displaying additional metadata (implementation year, notes) in a pop‑up when a state or locality is clicked.  Folium’s `GeoJson` layer supports custom JavaScript callbacks for this purpose.
* **Multiple Layers** – Add layers to toggle between statewide shading, local markers, and programme notes.  Users can then customise their view.
* **Dashboard Integration** – Embed the HTML map into a Streamlit or Dash app to allow filtering by year or region.

By following this guide, a Claude code agent can autonomously build a polished Blue Envelope Programme infographic, update it as new adoption data emerges, and maintain consistent design standards across static and interactive outputs.