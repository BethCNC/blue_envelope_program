#!/usr/bin/env python3
"""
Simple, reliable chart generation for Blue Envelope Program
"""

import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Set up the color scheme
COLORS = {
    'indigo_dye': '#164772',
    'blue_ncs': '#2c87be', 
    'columbia_blue': '#d1e9f3',
    'naples_yellow': '#f8e16c',
    'emerald': '#59cd90',
    'cerise': '#d63c5b'
}

def create_program_adoption_chart():
    """Create program adoption by type chart"""
    # Data
    types = ['Statewide', 'Local', 'Pending Statewide']
    counts = [8, 8, 1]
    colors = [COLORS['indigo_dye'], COLORS['blue_ncs'], COLORS['naples_yellow']]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(counts, labels=types, autopct='%1.1f%%',
                                     colors=colors, startangle=90)
    
    # Style the text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_weight('bold')
    
    ax.set_title('Blue Envelope Program Adoption by Type\n(17 States & Territories with Active Programs)', 
                fontsize=14, fontweight='bold', color=COLORS['indigo_dye'], pad=20)
    
    plt.tight_layout()
    plt.savefig('assets/program_adoption_by_type.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created program adoption chart")

def create_monroe_analysis_chart():
    """Create Monroe Police Department analysis chart"""
    # Data from Monroe scan
    keywords = ['Autism', 'Disability', 'ADA', 'Accessibility']
    counts = [0, 0, 0, 13]
    colors = [COLORS['cerise'], COLORS['cerise'], COLORS['cerise'], COLORS['naples_yellow']]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars = ax.bar(keywords, counts, color=colors, alpha=0.8)
    ax.set_title('Monroe PD Website: Keyword Analysis\n(15 pages, 32,388 words scanned)', 
                fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    ax.set_ylabel('Number of Mentions', fontsize=12)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
               str(count), ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Add critical findings text
    ax.text(0.02, 0.98, 'CRITICAL FINDINGS:\n• 0 Autism mentions\n• 0 Disability awareness\n• 0 ADA compliance\n• Only 13 accessibility mentions', 
           transform=ax.transAxes, fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS['columbia_blue'], alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('assets/monroe_analysis_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created Monroe analysis chart")

def create_cost_benefit_chart():
    """Create cost-benefit analysis chart"""
    # Cost data
    cost_items = ['Envelopes', 'Training', 'Materials', 'Setup']
    costs = [2000, 3000, 1500, 1000]
    
    # Benefit data
    benefit_items = ['Legal Risk', 'Community Relations', 'Officer Safety', 'Training Savings']
    benefits = [25000, 20000, 15000, 10000]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Costs
    bars1 = ax1.bar(cost_items, costs, color=COLORS['cerise'], alpha=0.8)
    ax1.set_title('Implementation Costs\nMonroe, NC Blue Envelope Program', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax1.set_ylabel('Cost ($)', fontsize=11)
    
    for bar, cost in zip(bars1, costs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'${cost:,}', ha='center', va='bottom', fontweight='bold')
    
    # Benefits
    bars2 = ax2.bar(benefit_items, benefits, color=COLORS['emerald'], alpha=0.8)
    ax2.set_title('Annual Benefits\nMonroe, NC Blue Envelope Program', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax2.set_ylabel('Benefit ($)', fontsize=11)
    
    for bar, benefit in zip(bars2, benefits):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                f'${benefit:,}', ha='center', va='bottom', fontweight='bold')
    
    # Calculate and display ROI
    total_cost = sum(costs)
    total_benefit = sum(benefits)
    roi = ((total_benefit - total_cost) / total_cost) * 100
    
    fig.suptitle(f'Cost-Benefit Analysis: {roi:.0f}% ROI\nTotal Cost: ${total_cost:,} | Annual Benefit: ${total_benefit:,}', 
                fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.tight_layout()
    plt.savefig('assets/cost_benefit_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created cost-benefit analysis chart")

def create_implementation_timeline():
    """Create implementation timeline chart"""
    # Timeline data
    states = ['Connecticut', 'Massachusetts', 'Vermont', 'Maine', 'Arizona', 'Rhode Island', 'Virginia', 'Delaware', 'Arkansas']
    years = [2020, 2023, 2024, 2024, 2024, 2025, 2025, 2025, 2026]
    types = ['Statewide', 'Statewide', 'Statewide', 'Statewide', 'Statewide', 'Statewide', 'Statewide', 'Statewide', 'Pending']
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Color by type
    colors = [COLORS['indigo_dye'] if t == 'Statewide' else COLORS['naples_yellow'] for t in types]
    
    bars = ax.barh(states, years, color=colors, alpha=0.8)
    ax.set_xlabel('Implementation Year', fontsize=12, fontweight='bold')
    ax.set_title('Blue Envelope Program Implementation Timeline\nProgressive Adoption Across States', 
                fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    
    # Add year labels
    for bar, year in zip(bars, years):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
               str(year), va='center', fontweight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLORS['indigo_dye'], label='Statewide Program'),
                      Patch(facecolor=COLORS['naples_yellow'], label='Pending Statewide')]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('assets/implementation_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created implementation timeline")

def create_program_statistics():
    """Create program statistics summary"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Overall adoption
    adopted = 17
    not_adopted = 33
    ax1.pie([adopted, not_adopted], labels=['Adopted', 'Not Adopted'], 
           autopct='%1.1f%%', colors=[COLORS['emerald'], COLORS['white_smoke']])
    ax1.set_title(f'Program Adoption\n{adopted} of 50 States/Territories', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    # 2. Program types
    statewide = 8
    local = 8
    pending = 1
    ax2.pie([statewide, local, pending], labels=['Statewide', 'Local', 'Pending'], 
           autopct='%1.1f%%', colors=[COLORS['indigo_dye'], COLORS['blue_ncs'], COLORS['naples_yellow']])
    ax2.set_title('Program Types\nAmong Adopted Programs', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    # 3. Implementation by year
    years = [2020, 2023, 2024, 2025, 2026]
    counts = [1, 1, 3, 3, 1]
    ax3.bar(years, counts, color=COLORS['blue_ncs'], alpha=0.8)
    ax3.set_title('Programs Implemented by Year', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Number of Programs')
    
    # 4. Key statistics
    stats_text = f"""KEY STATISTICS:

• Total States/Territories: 50
• Programs Adopted: {adopted}
• Adoption Rate: {(adopted/50)*100:.1f}%

• Statewide Programs: {statewide}
• Local Programs: {local}
• Pending Programs: {pending}

• First Implementation: 2020
• Latest Implementation: 2026
• Growth Trend: Rapid expansion"""
    
    ax4.text(0.05, 0.95, stats_text, fontsize=10, color=COLORS['indigo_dye'], 
            fontweight='bold', transform=ax4.transAxes, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS['columbia_blue'], alpha=0.3))
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Program Statistics Summary', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.suptitle('Blue Envelope Program: National Implementation Statistics', 
                fontsize=16, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.tight_layout()
    plt.savefig('assets/program_statistics_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created program statistics summary")

def main():
    """Create all charts"""
    print("Creating Blue Envelope Program charts...")
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Create all charts
    create_program_adoption_chart()
    create_monroe_analysis_chart()
    create_cost_benefit_chart()
    create_implementation_timeline()
    create_program_statistics()
    
    print("\n" + "="*50)
    print("ALL CHARTS CREATED SUCCESSFULLY!")
    print("="*50)
    print("Charts saved to assets/ directory")
    print("Using color scheme:")
    print(f"• Primary Blue: {COLORS['indigo_dye']}")
    print(f"• Secondary Blue: {COLORS['blue_ncs']}")
    print(f"• Light Blue: {COLORS['columbia_blue']}")
    print(f"• Yellow Accent: {COLORS['naples_yellow']}")
    print(f"• Error Color: {COLORS['cerise']}")

if __name__ == "__main__":
    main()
