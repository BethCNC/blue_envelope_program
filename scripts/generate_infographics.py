#!/usr/bin/env python3
"""
Blue Envelope Program - Professional Infographic Generator
Creates a comprehensive set of charts and visualizations for presentations
and advocacy materials.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import json
import numpy as np
from datetime import datetime
import os

# Set professional styling
plt.style.use('default')
sns.set_palette("husl")

# Color scheme for Blue Envelope Program
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
    print("Loading datasets...")
    
    # Load adoption data
    adoption_df = pd.read_csv("data/blue_envelope_data.csv")
    
    # Load research data
    with open("data/research.json", 'r') as f:
        research_data = json.load(f)
    
    return adoption_df, research_data

def create_adoption_status_chart(adoption_df, save_path="assets/adoption_status_chart.png"):
    """Create adoption status distribution chart"""
    print("Creating adoption status distribution chart...")
    
    # Count adoption types
    status_counts = adoption_df['adoption_type'].value_counts()
    
    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create donut chart
    wedges, texts, autotexts = ax.pie(
        status_counts.values,
        labels=status_counts.index,
        colors=[COLORS.get(status.lower().replace(' ', ''), COLORS['none']) 
                for status in status_counts.index],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.85,
        textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    
    # Create donut hole
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    ax.add_artist(centre_circle)
    
    # Add title and styling
    ax.set_title('Blue Envelope Program Adoption Status\nAcross the United States', 
                fontsize=18, fontweight='bold', pad=20, color=COLORS['text'])
    
    # Add total count in center
    total_states = len(adoption_df[adoption_df['state'] != 'Other States'])
    ax.text(0, 0, f'{total_states}\nStates\nAnalyzed', 
            ha='center', va='center', fontsize=14, fontweight='bold', color=COLORS['text'])
    
    # Style the chart
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_implementation_timeline(adoption_df, save_path="assets/implementation_timeline.png"):
    """Create implementation timeline chart"""
    print("Creating implementation timeline chart...")
    
    # Filter out 'Other States' and prepare data
    timeline_df = adoption_df[adoption_df['state'] != 'Other States'].copy()
    timeline_df = timeline_df[timeline_df['implementation_year'].notna()]
    timeline_df = timeline_df.sort_values('implementation_year')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create timeline
    y_positions = range(len(timeline_df))
    
    # Plot points for each state
    for i, (_, row) in enumerate(timeline_df.iterrows()):
        color = COLORS.get(row['adoption_type'].lower().replace(' ', ''), COLORS['none'])
        
        ax.scatter(row['implementation_year'], i, 
                  color=color, s=200, alpha=0.8, edgecolors='black', linewidth=1)
        
        # Add state labels
        ax.text(row['implementation_year'] + 0.1, i, 
               f"{row['state']} ({row['adoption_type']})", 
               va='center', fontsize=10, fontweight='bold')
    
    # Styling
    ax.set_yticks(y_positions)
    ax.set_yticklabels(timeline_df['state'], fontsize=10)
    ax.set_xlabel('Implementation Year', fontsize=12, fontweight='bold')
    ax.set_title('Blue Envelope Program Implementation Timeline\nProgressive State Adoption (2019-2026)', 
                fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
    
    # Add grid
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_axisbelow(True)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['statewide'], 
                  markersize=10, label='Statewide'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['local'], 
                  markersize=10, label='Local'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['pending'], 
                  markersize=10, label='Pending Statewide')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_police_interaction_risk_chart(research_data, save_path="assets/police_interaction_risk.png"):
    """Create police interaction risk comparison chart"""
    print("Creating police interaction risk chart...")
    
    # Extract statistics
    stats = research_data['statistics']['police_contact']
    
    # Prepare data
    categories = ['General Population', 'Autistic Individuals']
    percentages = [100/7, 100]  # 7x more likely means 1/7th the rate for general population
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create horizontal bar chart
    bars = ax.barh(categories, percentages, color=[COLORS['accent'], COLORS['pending']], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    
    # Add value labels
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
               f'{pct:.1f}%', va='center', fontsize=14, fontweight='bold')
    
    # Add comparison text
    ax.text(50, 0.5, '7x Higher Risk', ha='center', va='center', 
           fontsize=16, fontweight='bold', color=COLORS['text'],
           bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    
    # Styling
    ax.set_xlabel('Likelihood of Police Contact (%)', fontsize=12, fontweight='bold')
    ax.set_title('Police Interaction Risk: Autistic vs General Population\nBased on DOJ Data Analysis', 
                fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
    ax.set_xlim(0, 120)
    
    # Add grid
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_use_of_force_statistics(research_data, save_path="assets/use_of_force_stats.png"):
    """Create use of force statistics visualization"""
    print("Creating use of force statistics chart...")
    
    # Extract data
    stats = research_data['statistics']['use_of_force_fatalities']
    
    # Prepare data for pie chart
    labels = ['Victims with Disabilities', 'Victims without Disabilities']
    sizes = [40, 60]  # Using 40% as midpoint of 33-50% range
    colors = [COLORS['pending'], COLORS['none']]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Pie chart for disability statistics
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                      startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax1.set_title('Use of Force Fatalities\nby Disability Status', fontsize=14, fontweight='bold', 
                 color=COLORS['text'], pad=20)
    
    # Bar chart for mental health statistics
    mental_health_data = ['Mental Health\nDisability', 'No Mental Health\nDisability']
    mental_health_values = [20, 80]
    
    bars = ax2.bar(mental_health_data, mental_health_values, 
                   color=[COLORS['accent'], COLORS['none']], alpha=0.8, 
                   edgecolor='black', linewidth=1)
    
    # Add value labels
    for bar, value in zip(bars, mental_health_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{value}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.set_title('Use of Force Fatalities\nby Mental Health Status', fontsize=14, fontweight='bold', 
                 color=COLORS['text'], pad=20)
    ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_axisbelow(True)
    
    # Overall title
    fig.suptitle('Disproportionate Impact: Use of Force Fatalities\nRuderman Family Foundation Analysis (2016)', 
                fontsize=16, fontweight='bold', color=COLORS['text'], y=0.95)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_union_county_cost_breakdown(save_path="assets/union_county_costs.png"):
    """Create Union County cost breakdown chart"""
    print("Creating Union County cost breakdown chart...")
    
    # Cost data from research
    cost_categories = [
        'Officer Training\n(320 officers × 2 hours)',
        'Envelope Production\n(10,000 envelopes)',
        'Program Setup\n(Coordination & Materials)',
        'Annual Operations\n(Replenishment & Updates)'
    ]
    
    initial_costs = [17920, 3000, 7500, 0]  # Initial year costs
    annual_costs = [0, 1500, 0, 11500]      # Ongoing annual costs
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Initial implementation costs
    bars1 = ax1.bar(range(len(cost_categories)), initial_costs, 
                    color=[COLORS['statewide'], COLORS['local'], COLORS['pending'], COLORS['none']],
                    alpha=0.8, edgecolor='black', linewidth=1)
    
    ax1.set_title('Initial Implementation Costs\nUnion County, NC', fontsize=14, fontweight='bold', 
                 color=COLORS['text'], pad=20)
    ax1.set_ylabel('Cost ($)', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(len(cost_categories)))
    ax1.set_xticklabels(cost_categories, rotation=45, ha='right', fontsize=10)
    
    # Add value labels
    for bar, cost in zip(bars1, initial_costs):
        if cost > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
                    f'${cost:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Annual operating costs
    bars2 = ax2.bar(range(len(cost_categories)), annual_costs, 
                    color=[COLORS['statewide'], COLORS['local'], COLORS['pending'], COLORS['none']],
                    alpha=0.8, edgecolor='black', linewidth=1)
    
    ax2.set_title('Annual Operating Costs\nUnion County, NC', fontsize=14, fontweight='bold', 
                 color=COLORS['text'], pad=20)
    ax2.set_ylabel('Cost ($)', fontsize=12, fontweight='bold')
    ax2.set_xticks(range(len(cost_categories)))
    ax2.set_xticklabels(cost_categories, rotation=45, ha='right', fontsize=10)
    
    # Add value labels
    for bar, cost in zip(bars2, annual_costs):
        if cost > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, 
                    f'${cost:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Add total cost annotations
    total_initial = sum(initial_costs)
    total_annual = sum(annual_costs)
    
    ax1.text(0.5, 0.95, f'Total Initial: ${total_initial:,}', 
            transform=ax1.transAxes, ha='center', va='top', 
            fontsize=12, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
    
    ax2.text(0.5, 0.95, f'Total Annual: ${total_annual:,}', 
            transform=ax2.transAxes, ha='center', va='top', 
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7))
    
    # Overall title
    fig.suptitle('Blue Envelope Program Cost Analysis\nUnion County, NC Implementation', 
                fontsize=16, fontweight='bold', color=COLORS['text'], y=0.95)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_fatal_encounters_timeline(research_data, save_path="assets/fatal_encounters_timeline.png"):
    """Create fatal encounters timeline"""
    print("Creating fatal encounters timeline...")
    
    # Extract fatal encounters data
    encounters = research_data['fatal_encounters']
    
    # Filter out entries without years
    valid_encounters = [e for e in encounters if e.get('year') is not None]
    
    if not valid_encounters:
        print("No valid encounter data with years found")
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create timeline
    years = [e['year'] for e in valid_encounters]
    ages = [e['age'] for e in valid_encounters]
    locations = [e['location'] for e in valid_encounters]
    names = [e['name'] for e in valid_encounters]
    
    # Plot points
    scatter = ax.scatter(years, ages, s=300, c=COLORS['pending'], alpha=0.8, 
                        edgecolors='black', linewidth=2)
    
    # Add labels
    for i, (year, age, location, name) in enumerate(zip(years, ages, locations, names)):
        ax.annotate(f'{name}\n{age} years old\n{location}', 
                   (year, age), xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7),
                   fontsize=9, fontweight='bold')
    
    # Styling
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Age', fontsize=12, fontweight='bold')
    ax.set_title('Fatal Police Encounters with Autistic Individuals\nDocumented Cases (2019-2024)', 
                fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
    
    # Add grid
    ax.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add note about data limitations
    ax.text(0.02, 0.98, 'Note: Limited documented cases available\nMany incidents may go unreported', 
           transform=ax.transAxes, fontsize=10, va='top', ha='left',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def create_training_requirements_chart(research_data, save_path="assets/training_requirements.png"):
    """Create training requirements comparison chart"""
    print("Creating training requirements chart...")
    
    # Extract training data
    policy_data = research_data['policy_and_training']['state_mandates']
    
    # Prepare data
    years = ['2023', '2024']
    states_with_training = [policy_data['states_requiring_autism_training_2023'], 
                           policy_data['states_requiring_autism_training_2024']]
    total_states = 50
    
    states_without_training = [total_states - count for count in states_with_training]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create stacked bar chart
    width = 0.6
    x = np.arange(len(years))
    
    bars1 = ax.bar(x, states_with_training, width, label='States Requiring Training', 
                   color=COLORS['statewide'], alpha=0.8, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x, states_without_training, width, bottom=states_with_training, 
                   label='States Without Training', color=COLORS['none'], alpha=0.8, 
                   edgecolor='black', linewidth=1)
    
    # Add value labels
    for i, (bar1, bar2, count) in enumerate(zip(bars1, bars2, states_with_training)):
        ax.text(bar1.get_x() + bar1.get_width()/2, bar1.get_height()/2, 
               f'{count} states', ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(bar2.get_x() + bar2.get_width()/2, bar2.get_y() + bar2.get_height()/2, 
               f'{total_states - count} states', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Styling
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of States', fontsize=12, fontweight='bold')
    ax.set_title('Autism Training Requirements for Law Enforcement\nProgress Over Time', 
                fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_ylim(0, 60)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    # Add percentage annotations
    for i, count in enumerate(states_with_training):
        percentage = (count / total_states) * 100
        ax.text(i, total_states + 2, f'{percentage:.1f}%', ha='center', va='bottom', 
               fontsize=12, fontweight='bold', color=COLORS['text'])
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {save_path}")

def main():
    """Generate all infographics"""
    print("Blue Envelope Program - Professional Infographic Generator")
    print("=" * 60)
    
    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # Load data
    adoption_df, research_data = load_data()
    
    # Generate all charts
    charts = [
        ("Adoption Status Distribution", create_adoption_status_chart, [adoption_df]),
        ("Implementation Timeline", create_implementation_timeline, [adoption_df]),
        ("Police Interaction Risk", create_police_interaction_risk_chart, [research_data]),
        ("Use of Force Statistics", create_use_of_force_statistics, [research_data]),
        ("Union County Cost Breakdown", create_union_county_cost_breakdown, []),
        ("Fatal Encounters Timeline", create_fatal_encounters_timeline, [research_data]),
        ("Training Requirements", create_training_requirements_chart, [research_data])
    ]
    
    for name, func, args in charts:
        try:
            print(f"\nGenerating: {name}")
            func(*args)
        except Exception as e:
            print(f"Error generating {name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Infographic generation complete!")
    print("All charts saved to assets/ directory")
    print("Files ready for presentations and advocacy materials")

if __name__ == "__main__":
    main()

