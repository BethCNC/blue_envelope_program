# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project visualizes adoption of the **Blue Envelope Program** across the United States, a traffic-stop communication initiative for neurodivergent drivers. The project generates both static and interactive maps showing where the program has been adopted statewide or locally.

## Essential Commands

### Environment Setup
```bash
pip install -r requirements.txt
```

### Generate Maps
```bash
# Generate static map (saves to assets/output_map.png)
python scripts/plot_static_map.py

# Generate interactive map (saves to assets/interactive_map.html)  
python scripts/plot_interactive_map.py
```

## Data Architecture

### Core Data Source
- **Primary dataset**: `data/blue_envelope_data.csv` and `data/blue_envelope_data.json` contain the same data in different formats
- **Schema**:
  - `state`: State name or abbreviation
  - `adopted`: Boolean indicating any program exists
  - `adoption_type`: One of "Statewide", "Local", "Pending Statewide", or "None"
  - `localities`: Comma-separated list of counties/towns with local programs
  - `implementation_year`: Year program was introduced
  - `notes`: Additional context and details

### Data Integrity Rules
1. **NEVER** invent or fabricate program adoption data
2. Always read from the CSV/JSON files - do not hardcode locations
3. When updating data, modify the source files after verification
4. The scripts expect a column mismatch: they look for `coverage_type` but data uses `adoption_type`

## Code Architecture

### Static Map Generation (`scripts/plot_static_map.py`)
- Uses **GeoPandas** to load US state boundaries from remote GeoJSON
- Uses **Matplotlib** for rendering
- Color scheme: Green (Statewide), Gold (Local), Light Grey (None)
- Outputs to `assets/output_map.png`

### Interactive Map Generation (`scripts/plot_interactive_map.py`)  
- Uses **Plotly Express** for choropleth mapping
- Same color scheme as static map
- Outputs to `assets/interactive_map.html`

### Key Dependencies
- `pandas` - Data manipulation
- `geopandas` - Geospatial data handling
- `matplotlib` - Static plotting
- `plotly` - Interactive visualizations
- `shapely` - Geometric operations
- `contextily` - Basemap tiles

## Current Issues to Address

### Data Column Mismatch
The Python scripts reference `coverage_type` but the actual data uses `adoption_type`. This needs to be corrected in either the data files or the scripts for proper functionality.

### Missing Assets Directory
The scripts save outputs to `assets/` directory which may not exist and needs to be created.

## Color Standards

Current implementation uses:
- **Statewide adoption**: Green (`#2E8B57` in static, "green" in interactive)
- **Local adoption**: Gold (`#FFD700` in static, "gold" in interactive) 
- **No adoption**: Light Grey (`#D3D3D3` in static, "lightgrey" in interactive)

Note: Legacy documentation mentions blue color schemes, but current scripts implement green/gold.