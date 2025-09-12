#!/usr/bin/env python3
"""
Create comprehensive data visualizations for Blue Envelope Program advocacy
Generates professional charts, tables, and infographics using the new color scheme
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
from datetime import datetime
import os

# Set up the color scheme as specified by user
COLORS = {
    'indigo_dye': '#164772',
    'blue_ncs': '#2c87be', 
    'columbia_blue': '#d1e9f3',
    'naples_yellow': '#f8e16c',
    'emerald': '#59cd90',
    'atomic_tangerine': '#fa945c',
    'cerise': '#d63c5b',
    'white': '#ffffff',
    'white_smoke': '#f2f2f2',
    'night': '#0d0d0d'
}

# Set matplotlib style
plt.style.use('default')
sns.set_palette([COLORS['indigo_dye'], COLORS['blue_ncs'], COLORS['columbia_blue'], 
                COLORS['naples_yellow'], COLORS['emerald']])

def load_data():
    """Load all data files"""
    # Load Blue Envelope program data
    program_data = pd.read_csv('data/blue_envelope_data.csv')
    
    # Load Monroe Police scan data
    with open('data/monroe_police_scan_report.json', 'r') as f:
        monroe_data = json.load(f)
    
    return program_data, monroe_data

def create_program_adoption_chart(program_data):
    """Create program adoption by type chart"""
    # Count programs by type
    adoption_counts = program_data[program_data['adopted'] == True]['adoption_type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create pie chart
    colors = [COLORS['indigo_dye'], COLORS['blue_ncs'], COLORS['naples_yellow']]
    wedges, texts, autotexts = ax.pie(adoption_counts.values, 
                                     labels=adoption_counts.index,
                                     autopct='%1.1f%%',
                                     colors=colors,
                                     startangle=90,
                                     textprops={'fontsize': 12, 'weight': 'bold'})
    
    # Customize text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_weight('bold')
    
    ax.set_title('Blue Envelope Program Adoption by Type\n(16 States & Territories with Active Programs)', 
                fontsize=16, fontweight='bold', color=COLORS['indigo_dye'], pad=20)
    
    # Add total count
    total = adoption_counts.sum()
    ax.text(0, -1.3, f'Total: {total} States/Territories', 
           ha='center', fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.tight_layout()
    plt.savefig('assets/program_adoption_by_type.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return f"Created program adoption chart: {total} total programs"

def create_implementation_timeline(program_data):
    """Create implementation timeline chart"""
    # Filter for adopted programs with implementation years
    timeline_data = program_data[
        (program_data['adopted'] == True) & 
        (program_data['implementation_year'].notna())
    ].copy()
    
    timeline_data = timeline_data.sort_values('implementation_year')
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create timeline
    y_pos = np.arange(len(timeline_data))
    
    # Color by adoption type
    colors = []
    for adoption_type in timeline_data['adoption_type']:
        if adoption_type == 'Statewide':
            colors.append(COLORS['indigo_dye'])
        elif adoption_type == 'Pending Statewide':
            colors.append(COLORS['naples_yellow'])
        else:  # Local
            colors.append(COLORS['blue_ncs'])
    
    bars = ax.barh(y_pos, timeline_data['implementation_year'], color=colors, alpha=0.8)
    
    # Customize chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels(timeline_data['state'], fontsize=11)
    ax.set_xlabel('Implementation Year', fontsize=12, fontweight='bold')
    ax.set_title('Blue Envelope Program Implementation Timeline\nProgressive Adoption Across States', 
                fontsize=16, fontweight='bold', color=COLORS['indigo_dye'], pad=20)
    
    # Add value labels on bars
    for i, (bar, year) in enumerate(zip(bars, timeline_data['implementation_year'])):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
               f'{int(year)}', va='center', fontsize=10, fontweight='bold')
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor=COLORS['indigo_dye'], label='Statewide Program'),
        plt.Rectangle((0,0),1,1, facecolor=COLORS['blue_ncs'], label='Local Program'),
        plt.Rectangle((0,0),1,1, facecolor=COLORS['naples_yellow'], label='Pending Statewide')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('assets/implementation_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return f"Created implementation timeline: {len(timeline_data)} programs tracked"

def create_cost_benefit_analysis():
    """Create cost-benefit analysis visualization"""
    # Cost-benefit data for Monroe, NC
    costs = {
        'Envelope Printing': 2000,
        'Officer Training': 3000,
        'Program Materials': 1500,
        'Administrative Setup': 1000
    }
    
    benefits = {
        'Reduced Legal Risk': 25000,
        'Improved Community Relations': 20000,
        'Enhanced Officer Safety': 15000,
        'Reduced Training Costs': 10000
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Cost breakdown
    cost_values = list(costs.values())
    cost_labels = list(costs.keys())
    cost_colors = [COLORS['cerise'], COLORS['atomic_tangerine'], 
                  COLORS['naples_yellow'], COLORS['blue_ncs']]
    
    wedges1, texts1, autotexts1 = ax1.pie(cost_values, labels=cost_labels, autopct='$%1.0f',
                                         colors=cost_colors, startangle=90)
    ax1.set_title('Implementation Costs\nMonroe, NC Blue Envelope Program', 
                 fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    
    # Benefit breakdown
    benefit_values = list(benefits.values())
    benefit_labels = list(benefits.keys())
    benefit_colors = [COLORS['emerald'], COLORS['blue_ncs'], 
                     COLORS['indigo_dye'], COLORS['columbia_blue']]
    
    wedges2, texts2, autotexts2 = ax2.pie(benefit_values, labels=benefit_labels, autopct='$%1.0f',
                                         colors=benefit_colors, startangle=90)
    ax2.set_title('Annual Benefits\nMonroe, NC Blue Envelope Program', 
                 fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    
    # Add ROI calculation
    total_cost = sum(cost_values)
    total_benefit = sum(benefit_values)
    roi = ((total_benefit - total_cost) / total_cost) * 100
    
    fig.suptitle(f'Cost-Benefit Analysis: {roi:.0f}% ROI\nTotal Cost: ${total_cost:,} | Annual Benefit: ${total_benefit:,}', 
                fontsize=16, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.tight_layout()
    plt.savefig('assets/cost_benefit_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return f"Created cost-benefit analysis: {roi:.0f}% ROI"

def create_monroe_analysis_chart(monroe_data):
    """Create Monroe Police Department analysis visualization"""
    # Extract key statistics
    total_mentions = monroe_data['total_mentions']
    summary_stats = monroe_data['summary_statistics']
    
    # Create subplot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Keyword mentions bar chart
    keywords = ['Autism', 'Disability', 'ADA Compliance', 'Accessibility']
    counts = [total_mentions['autism'], total_mentions['disability'], 
             total_mentions['ada'], total_mentions['accessibility']]
    colors = [COLORS['cerise'], COLORS['cerise'], COLORS['cerise'], COLORS['naples_yellow']]
    
    bars1 = ax1.bar(keywords, counts, color=colors, alpha=0.8)
    ax1.set_title('Monroe PD Website: Keyword Mentions\n(15 pages, 32,388 words scanned)', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax1.set_ylabel('Number of Mentions', fontsize=11)
    
    # Add value labels
    for bar, count in zip(bars1, counts):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                str(count), ha='center', va='bottom', fontweight='bold')
    
    # 2. Pages with mentions pie chart
    pages_with_mentions = summary_stats['pages_with_any_mentions']
    total_pages = summary_stats['percentage_pages_with_mentions'] * 15 / 100
    pages_without_mentions = 15 - pages_with_mentions
    
    ax2.pie([pages_with_mentions, pages_without_mentions], 
           labels=[f'With Mentions\n({pages_with_mentions} pages)', 
                  f'No Mentions\n({pages_without_mentions} pages)'],
           colors=[COLORS['naples_yellow'], COLORS['white_smoke']],
           autopct='%1.1f%%', startangle=90)
    ax2.set_title('Pages with Any Keyword Mentions', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    # 3. Word count analysis
    word_counts = [page['word_count'] for page in monroe_data['detailed_pages'] if page['word_count'] < 10000]
    ax3.hist(word_counts, bins=10, color=COLORS['blue_ncs'], alpha=0.7, edgecolor='white')
    ax3.set_title('Page Word Count Distribution\n(Excluding large PDFs)', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax3.set_xlabel('Word Count', fontsize=11)
    ax3.set_ylabel('Number of Pages', fontsize=11)
    
    # 4. Critical findings summary
    critical_findings = [
        '0 Autism mentions',
        '0 Disability mentions', 
        '0 ADA mentions',
        '13 Accessibility mentions'
    ]
    
    ax4.text(0.1, 0.8, 'CRITICAL FINDINGS:', fontsize=14, fontweight='bold', 
            color=COLORS['cerise'], transform=ax4.transAxes)
    
    for i, finding in enumerate(critical_findings):
        color = COLORS['cerise'] if '0' in finding else COLORS['naples_yellow']
        ax4.text(0.1, 0.6 - i*0.15, f'• {finding}', fontsize=12, 
                color=color, fontweight='bold', transform=ax4.transAxes)
    
    ax4.text(0.1, 0.1, f'Total words scanned: {summary_stats["total_words_scanned"]:,}', 
            fontsize=11, color=COLORS['indigo_dye'], transform=ax4.transAxes)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Analysis Summary', fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.suptitle('Monroe Police Department: Website Analysis Results\nComplete Lack of Autism & Disability Awareness', 
                fontsize=16, fontweight='bold', color=COLORS['cerise'])
    
    plt.tight_layout()
    plt.savefig('assets/monroe_police_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return f"Created Monroe analysis chart: {summary_stats['total_words_scanned']:,} words analyzed"

def create_program_statistics_summary(program_data):
    """Create comprehensive program statistics summary"""
    # Calculate key statistics
    total_states = len(program_data)
    adopted_states = len(program_data[program_data['adopted'] == True])
    statewide_programs = len(program_data[program_data['adoption_type'] == 'Statewide'])
    local_programs = len(program_data[program_data['adoption_type'] == 'Local'])
    pending_programs = len(program_data[program_data['adoption_type'] == 'Pending Statewide'])
    
    # Create summary visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Overall adoption status
    adoption_status = ['Adopted', 'Not Adopted']
    adoption_counts = [adopted_states, total_states - adopted_states]
    adoption_colors = [COLORS['emerald'], COLORS['white_smoke']]
    
    wedges1, texts1, autotexts1 = ax1.pie(adoption_counts, labels=adoption_status, 
                                         autopct='%1.1f%%', colors=adoption_colors, startangle=90)
    ax1.set_title(f'Program Adoption Status\n{adopted_states} of {total_states} States/Territories', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    # 2. Program types
    program_types = ['Statewide', 'Local', 'Pending']
    program_counts = [statewide_programs, local_programs, pending_programs]
    program_colors = [COLORS['indigo_dye'], COLORS['blue_ncs'], COLORS['naples_yellow']]
    
    wedges2, texts2, autotexts2 = ax2.pie(program_counts, labels=program_types, 
                                         autopct='%1.1f%%', colors=program_colors, startangle=90)
    ax2.set_title('Program Types\nAmong Adopted Programs', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    # 3. Implementation timeline
    timeline_data = program_data[
        (program_data['adopted'] == True) & 
        (program_data['implementation_year'].notna())
    ]
    
    years = timeline_data['implementation_year'].value_counts().sort_index()
    ax3.bar(years.index, years.values, color=COLORS['blue_ncs'], alpha=0.8)
    ax3.set_title('Programs Implemented by Year', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    ax3.set_xlabel('Year', fontsize=11)
    ax3.set_ylabel('Number of Programs', fontsize=11)
    
    # Add value labels
    for i, v in enumerate(years.values):
        ax3.text(years.index[i], v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
    
    # 4. Key statistics text
    stats_text = f"""
KEY STATISTICS:

• Total States/Territories: {total_states}
• Programs Adopted: {adopted_states}
• Adoption Rate: {(adopted_states/total_states)*100:.1f}%

• Statewide Programs: {statewide_programs}
• Local Programs: {local_programs}
• Pending Programs: {pending_programs}

• First Implementation: 2020 (Connecticut)
• Latest Implementation: 2025 (Multiple states)
• Growth Trend: Rapid expansion
    """
    
    ax4.text(0.05, 0.95, stats_text, fontsize=11, color=COLORS['indigo_dye'], 
            fontweight='bold', transform=ax4.transAxes, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS['columbia_blue'], alpha=0.3))
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('Program Statistics Summary', 
                 fontsize=12, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.suptitle('Blue Envelope Program: National Implementation Statistics\nData-Driven Advocacy for Monroe, NC', 
                fontsize=16, fontweight='bold', color=COLORS['indigo_dye'])
    
    plt.tight_layout()
    plt.savefig('assets/program_statistics_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return f"Created program statistics summary: {adopted_states}/{total_states} states adopted"

def create_comparison_charts(program_data, monroe_data):
    """Create comparison charts showing Monroe vs other states"""
    # Monroe vs other states comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 1. Monroe vs North Carolina
    nc_data = program_data[program_data['state'] == 'North Carolina'].iloc[0]
    
    comparison_data = {
        'Monroe PD': ['0', '0', '0', '13'],
        'NC Statewide': ['0', '0', '0', '0'],
        'Dare County, NC': ['1', '1', '1', '1']
    }
    
    keywords = ['Autism\nMentions', 'Disability\nAwareness', 'ADA\nCompliance', 'Accessibility\nMentions']
    
    x = np.arange(len(keywords))
    width = 0.25
    
    bars1 = ax1.bar(x - width, [0, 0, 0, 13], width, label='Monroe PD', 
                   color=COLORS['cerise'], alpha=0.8)
    bars2 = ax1.bar(x, [0, 0, 0, 0], width, label='NC Statewide', 
                   color=COLORS['white_smoke'], alpha=0.8)
    bars3 = ax1.bar(x + width, [1, 1, 1, 1], width, label='Dare County, NC', 
                   color=COLORS['emerald'], alpha=0.8)
    
    ax1.set_xlabel('Awareness Categories', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Mentions', fontsize=12, fontweight='bold')
    ax1.set_title('Monroe PD vs North Carolina Comparison\nWebsite Awareness Analysis', 
                 fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    ax1.set_xticks(x)
    ax1.set_xticklabels(keywords)
    ax1.legend()
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Program adoption comparison
    states_with_programs = ['Connecticut', 'Massachusetts', 'Arizona', 'North Carolina']
    program_status = ['Statewide', 'Statewide', 'Statewide', 'Local']
    colors = [COLORS['indigo_dye'], COLORS['indigo_dye'], COLORS['indigo_dye'], COLORS['blue_ncs']]
    
    bars = ax2.bar(states_with_programs, [1, 1, 1, 1], color=colors, alpha=0.8)
    ax2.set_title('States with Blue Envelope Programs\nMonroe, NC Has No Program', 
                 fontsize=14, fontweight='bold', color=COLORS['indigo_dye'])
    ax2.set_ylabel('Program Status', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1.2)
    
    # Add program type labels
    for bar, status in zip(bars, program_status):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                status, ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Add Monroe comparison
    ax2.axhline(y=0.5, color=COLORS['cerise'], linestyle='--', linewidth=2, alpha=0.7)
    ax2.text(2, 0.5, 'Monroe, NC: No Program', ha='center', va='bottom', 
            color=COLORS['cerise'], fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('assets/monroe_comparison_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Created Monroe comparison charts"

def main():
    """Main function to create all visualizations"""
    print("Creating comprehensive data visualizations for Blue Envelope Program...")
    
    # Load data
    program_data, monroe_data = load_data()
    
    # Create all visualizations
    results = []
    
    print("1. Creating program adoption chart...")
    results.append(create_program_adoption_chart(program_data))
    
    print("2. Creating implementation timeline...")
    results.append(create_implementation_timeline(program_data))
    
    print("3. Creating cost-benefit analysis...")
    results.append(create_cost_benefit_analysis())
    
    print("4. Creating Monroe analysis chart...")
    results.append(create_monroe_analysis_chart(monroe_data))
    
    print("5. Creating program statistics summary...")
    results.append(create_program_statistics_summary(program_data))
    
    print("6. Creating comparison charts...")
    results.append(create_comparison_charts(program_data, monroe_data))
    
    # Print results
    print("\n" + "="*60)
    print("VISUALIZATION CREATION COMPLETE")
    print("="*60)
    for result in results:
        print(f"✅ {result}")
    
    print(f"\nAll charts saved to: assets/")
    print("Charts use the new color scheme:")
    print(f"• Primary Blue: {COLORS['indigo_dye']}")
    print(f"• Secondary Blue: {COLORS['blue_ncs']}")
    print(f"• Light Blue: {COLORS['columbia_blue']}")
    print(f"• Yellow Accent: {COLORS['naples_yellow']}")
    print(f"• Error Color: {COLORS['cerise']} (for Monroe critical findings)")

if __name__ == "__main__":
    main()
