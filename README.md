# Blue Envelope Program Visualization

## Overview
This project visualizes adoption of the **Blue Envelope Program** across the United States, highlighting where it has been adopted **statewide** or **locally**.

### Goals
- 📊 Create a **static US map** showing program adoption status.
- 🗺️ Build an **interactive dashboard** for exploration.
- 📂 Maintain clean repo structure for easy automation using Cursor AI.

## Repository Structure
```
blue-envelope-visualization/
├── data/
│   ├── blue_envelope_data.csv
├── scripts/
│   ├── plot_static_map.py
│   ├── plot_interactive_map.py
├── prompts/
│   └── PROJECT_RULES.md
├── assets/
│   ├── output_map.png
│   ├── interactive_map.html
├── README.md
└── requirements.txt
```

## Setup Instructions
```bash
pip install -r requirements.txt
```

## Generate Static Map
```bash
python scripts/plot_static_map.py
```

## Generate Interactive Map
```bash
python scripts/plot_interactive_map.py
```

## Output
- Static map → `assets/output_map.png`
- Interactive map → `assets/interactive_map.html`
