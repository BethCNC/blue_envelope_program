# Project Rules & Workflow

## Rules for Cursor AI Agent
1. Always read data from `data/blue_envelope_data.csv`.
2. Never invent data — only use verified program adoption info.
3. Save generated maps into `assets/`.
4. Use consistent color codes:
   - **Green** = Statewide
   - **Yellow** = Local
   - **Grey** = None

## Workflow
### Step 1 — Environment Setup
```bash
pip install -r requirements.txt
```

### Step 2 — Generate Static Map
```bash
python scripts/plot_static_map.py
```

### Step 3 — Generate Interactive Map
```bash
python scripts/plot_interactive_map.py
```

### Step 4 — Update Dataset
- Add new counties/states in `data/blue_envelope_data.csv` when verified.

### Step 5 — Save Outputs
- Static → `assets/output_map.png`
- Interactive → `assets/interactive_map.html`

## Cursor AI Prompts

**Update Dataset**
```
Open `data/blue_envelope_data.csv` and add any newly confirmed states or counties where the Blue Envelope Program is officially adopted.
```

**Generate Static Map**
```
Run `scripts/plot_static_map.py` and save to `assets/output_map.png`.
```

**Generate Interactive Map**
```
Run `scripts/plot_interactive_map.py` and save to `assets/interactive_map.html`.
```
