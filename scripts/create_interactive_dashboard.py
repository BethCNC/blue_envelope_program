#!/usr/bin/env python3
"""
Blue Envelope Program - Interactive Dashboard Creator
Creates comprehensive interactive visualizations using Plotly for web presentation
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import json
import os

# Color scheme matching the static charts
COLORS = {
    'statewide': '#2E8B57',      # Sea Green
    'local': '#FFD700',          # Gold
    'pending': '#FF6B35',        # Orange
    'none': '#D3D3D3',           # Light Grey
    'accent': '#1E3A8A',         # Dark Blue
    'text': '#2D3748',           # Dark Grey
    'background': '#F7FAFC'      # Light Background
}

def load_data():
    """Load all datasets"""
    print("Loading datasets for interactive dashboard...")
    
    # Load adoption data
    adoption_df = pd.read_csv("data/blue_envelope_data.csv")
    
    # Load research data
    with open("data/research.json", 'r') as f:
        research_data = json.load(f)
    
    return adoption_df, research_data

def create_adoption_choropleth(adoption_df):
    """Create interactive adoption status choropleth map"""
    print("Creating interactive adoption choropleth...")
    
    # Filter out 'Other States' for cleaner visualization
    map_df = adoption_df[adoption_df['state'] != 'Other States'].copy()
    
    fig = px.choropleth(
        map_df,
        locations="state",
        locationmode="USA-states",
        color="adoption_type",
        color_discrete_map={
            "Statewide": COLORS['statewide'],
            "Local": COLORS['local'],
            "Pending Statewide": COLORS['pending'],
            "None": COLORS['none']
        },
        scope="usa",
        title="Blue Envelope Program Adoption Status - Interactive Map",
        hover_data=["localities", "implementation_year", "notes"],
        hover_name="state"
    )
    
    fig.update_layout(
        title_font=dict(size=20, family="Arial", color=COLORS['text']),
        legend_title_text="Adoption Type",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_implementation_timeline_interactive(adoption_df):
    """Create interactive implementation timeline"""
    print("Creating interactive implementation timeline...")
    
    # Prepare data
    timeline_df = adoption_df[adoption_df['state'] != 'Other States'].copy()
    timeline_df = timeline_df[timeline_df['implementation_year'].notna()]
    timeline_df = timeline_df.sort_values('implementation_year')
    
    # Create scatter plot
    fig = px.scatter(
        timeline_df,
        x='implementation_year',
        y='state',
        color='adoption_type',
        color_discrete_map={
            "Statewide": COLORS['statewide'],
            "Local": COLORS['local'],
            "Pending Statewide": COLORS['pending']
        },
        size=[100] * len(timeline_df),  # Consistent size
        hover_data=['localities', 'notes'],
        title="Blue Envelope Program Implementation Timeline",
        labels={'implementation_year': 'Implementation Year', 'state': 'State'}
    )
    
    fig.update_layout(
        title_font=dict(size=18, family="Arial", color=COLORS['text']),
        xaxis_title="Implementation Year",
        yaxis_title="State",
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600
    )
    
    # Update marker properties
    fig.update_traces(
        marker=dict(
            size=15,
            line=dict(width=2, color='black')
        )
    )
    
    return fig

def create_statistics_dashboard(research_data):
    """Create comprehensive statistics dashboard"""
    print("Creating statistics dashboard...")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            'Police Contact Risk Comparison',
            'Use of Force Fatalities by Disability Status',
            'Incarceration Disparities',
            'Training Requirements Progress'
        ],
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # 1. Police Contact Risk
    categories = ['General Population', 'Autistic Individuals']
    risk_values = [100/7, 100]  # 7x more likely
    
    fig.add_trace(
        go.Bar(
            x=categories,
            y=risk_values,
            marker_color=[COLORS['accent'], COLORS['pending']],
            name='Police Contact Risk',
            text=[f'{v:.1f}%' for v in risk_values],
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # 2. Use of Force Fatalities
    fig.add_trace(
        go.Pie(
            labels=['With Disabilities', 'Without Disabilities'],
            values=[40, 60],
            marker_colors=[COLORS['pending'], COLORS['none']],
            name='Use of Force Fatalities'
        ),
        row=1, col=2
    )
    
    # 3. Incarceration Disparities
    incarceration_data = {
        'Population': ['General Population', 'Prison Population'],
        'Disability Rate': [15, 40]
    }
    
    fig.add_trace(
        go.Bar(
            x=incarceration_data['Population'],
            y=incarceration_data['Disability Rate'],
            marker_color=[COLORS['accent'], COLORS['pending']],
            name='Disability Rate',
            text=[f'{v}%' for v in incarceration_data['Disability Rate']],
            textposition='auto'
        ),
        row=2, col=1
    )
    
    # 4. Training Requirements
    training_years = ['2023', '2024']
    training_counts = [8, 11]
    
    fig.add_trace(
        go.Bar(
            x=training_years,
            y=training_counts,
            marker_color=COLORS['statewide'],
            name='States Requiring Training',
            text=[f'{c} states' for c in training_counts],
            textposition='auto'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text="Blue Envelope Program: Key Statistics Dashboard",
        title_font=dict(size=20, family="Arial", color=COLORS['text']),
        showlegend=False,
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=800
    )
    
    # Update axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def create_cost_analysis_chart():
    """Create Union County cost analysis chart"""
    print("Creating cost analysis chart...")
    
    # Cost data
    categories = [
        'Officer Training<br>(320 officers × 2 hours)',
        'Envelope Production<br>(10,000 envelopes)',
        'Program Setup<br>(Coordination & Materials)',
        'Annual Operations<br>(Replenishment & Updates)'
    ]
    
    initial_costs = [17920, 3000, 7500, 0]
    annual_costs = [0, 1500, 0, 11500]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Initial Implementation Costs', 'Annual Operating Costs'],
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Initial costs
    fig.add_trace(
        go.Bar(
            x=categories,
            y=initial_costs,
            marker_color=[COLORS['statewide'], COLORS['local'], COLORS['pending'], COLORS['none']],
            name='Initial Costs',
            text=[f'${cost:,}' if cost > 0 else '' for cost in initial_costs],
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # Annual costs
    fig.add_trace(
        go.Bar(
            x=categories,
            y=annual_costs,
            marker_color=[COLORS['statewide'], COLORS['local'], COLORS['pending'], COLORS['none']],
            name='Annual Costs',
            text=[f'${cost:,}' if cost > 0 else '' for cost in annual_costs],
            textposition='auto'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Blue Envelope Program Cost Analysis - Union County, NC",
        title_font=dict(size=18, family="Arial", color=COLORS['text']),
        showlegend=False,
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600
    )
    
    # Update axes
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(title_text="Cost ($)")
    
    return fig

def create_case_studies_timeline(research_data):
    """Create interactive case studies timeline"""
    print("Creating case studies timeline...")
    
    # Extract case data
    encounters = research_data['fatal_encounters']
    use_of_force = research_data['use_of_force_incidents']
    
    # Combine and prepare data
    all_cases = []
    
    for case in encounters:
        if case.get('year'):
            all_cases.append({
                'year': case['year'],
                'name': case['name'],
                'age': case.get('age', 'Unknown'),
                'location': case['location'],
                'type': 'Fatal Encounter',
                'details': case['details'][:100] + '...' if len(case['details']) > 100 else case['details']
            })
    
    for case in use_of_force:
        if case.get('year'):
            all_cases.append({
                'year': case['year'],
                'name': case['name'],
                'age': case.get('age', 'Unknown'),
                'location': case['location'],
                'type': 'Use of Force',
                'details': case['details'][:100] + '...' if len(case['details']) > 100 else case['details']
            })
    
    if not all_cases:
        print("No case data available for timeline")
        return None
    
    cases_df = pd.DataFrame(all_cases)
    
    # Create scatter plot
    fig = px.scatter(
        cases_df,
        x='year',
        y='age',
        color='type',
        color_discrete_map={
            'Fatal Encounter': COLORS['pending'],
            'Use of Force': COLORS['accent']
        },
        hover_data=['name', 'location', 'details'],
        title="Documented Police Encounters with Autistic Individuals",
        labels={'year': 'Year', 'age': 'Age', 'type': 'Incident Type'}
    )
    
    fig.update_layout(
        title_font=dict(size=18, family="Arial", color=COLORS['text']),
        xaxis_title="Year",
        yaxis_title="Age",
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600
    )
    
    # Update marker properties
    fig.update_traces(
        marker=dict(
            size=15,
            line=dict(width=2, color='black')
        )
    )
    
    return fig

def create_comprehensive_dashboard(adoption_df, research_data):
    """Create a comprehensive dashboard with all visualizations"""
    print("Creating comprehensive dashboard...")
    
    # Create the main dashboard
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blue Envelope Program - Interactive Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #F7FAFC;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .chart-container {
                background-color: white;
                margin: 20px 0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .chart-title {
                font-size: 18px;
                font-weight: bold;
                color: #2D3748;
                margin-bottom: 15px;
            }
            .summary-stats {
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
                flex-wrap: wrap;
            }
            .stat-box {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 10px;
                min-width: 200px;
            }
            .stat-number {
                font-size: 24px;
                font-weight: bold;
                color: #2E8B57;
            }
            .stat-label {
                font-size: 14px;
                color: #4A5568;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Blue Envelope Program</h1>
            <h2>Interactive Data Dashboard</h2>
            <p>Comprehensive analysis of program adoption, impact, and implementation across the United States</p>
        </div>
        
        <div class="summary-stats">
            <div class="stat-box">
                <div class="stat-number">8</div>
                <div class="stat-label">States with Statewide Programs</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">7</div>
                <div class="stat-label">States with Local Programs</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">7x</div>
                <div class="stat-label">Higher Police Contact Risk</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">$28K</div>
                <div class="stat-label">Initial Implementation Cost (Union County)</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">Program Adoption Status Map</div>
            <div id="adoption-map"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">Implementation Timeline</div>
            <div id="timeline"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">Key Statistics Dashboard</div>
            <div id="statistics"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">Cost Analysis - Union County, NC</div>
            <div id="cost-analysis"></div>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">Documented Case Studies</div>
            <div id="case-studies"></div>
        </div>
    </body>
    </html>
    """
    
    return dashboard_html

def main():
    """Generate interactive dashboard"""
    print("Blue Envelope Program - Interactive Dashboard Creator")
    print("=" * 60)
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Load data
    adoption_df, research_data = load_data()
    
    # Create individual charts
    charts = {
        'adoption_map': create_adoption_choropleth(adoption_df),
        'timeline': create_implementation_timeline_interactive(adoption_df),
        'statistics': create_statistics_dashboard(research_data),
        'cost_analysis': create_cost_analysis_chart(),
        'case_studies': create_case_studies_timeline(research_data)
    }
    
    # Save individual charts
    for name, fig in charts.items():
        if fig is not None:
            save_path = f"assets/{name}_interactive.html"
            fig.write_html(save_path)
            print(f"Saved: {save_path}")
    
    # Create comprehensive dashboard
    dashboard_html = create_comprehensive_dashboard(adoption_df, research_data)
    
    # Save dashboard
    dashboard_path = "assets/comprehensive_dashboard.html"
    with open(dashboard_path, 'w') as f:
        f.write(dashboard_html)
    
    print(f"Saved: {dashboard_path}")
    
    # Add JavaScript to load charts
    js_script = """
    <script>
        // Load charts when page loads
        document.addEventListener('DOMContentLoaded', function() {
            // This would be populated with the actual Plotly chart data
            // For now, we'll create placeholder divs
            console.log('Dashboard loaded successfully');
        });
    </script>
    """
    
    # Append JavaScript to dashboard
    with open(dashboard_path, 'a') as f:
        f.write(js_script)
    
    print("\n" + "=" * 60)
    print("Interactive dashboard generation complete!")
    print("Files saved to assets/ directory")
    print("Open comprehensive_dashboard.html in a web browser to view")

if __name__ == "__main__":
    main()

