#!/usr/bin/env python3
"""
Example analysis of Union County Sheriff's Office website
This demonstrates how to use the manual analysis tool
"""

from manual_website_analysis import ManualWebsiteAnalysis
import matplotlib.pyplot as plt
import json

def create_example_analysis():
    """Create an example analysis based on typical law enforcement websites"""
    
    # Create analyzer instance
    analyzer = ManualWebsiteAnalysis()
    
    # Example data based on typical law enforcement websites
    # (You would replace this with actual manual analysis results)
    
    # Home page
    analyzer.add_page_analysis(
        page_name='Home Page',
        url='https://www.unioncountysheriffsoffice.com',
        word_count=1200,
        keyword_counts={
            'autism': 0,
            'disability': 0,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='No mentions of autism, disability, or accessibility terms found'
    )
    
    # About page
    analyzer.add_page_analysis(
        page_name='About Us',
        url='https://www.unioncountysheriffsoffice.com/about',
        word_count=800,
        keyword_counts={
            'autism': 0,
            'disability': 1,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='One mention of "disability" in general employment policy statement'
    )
    
    # Services page
    analyzer.add_page_analysis(
        page_name='Services',
        url='https://www.unioncountysheriffsoffice.com/services',
        word_count=1500,
        keyword_counts={
            'autism': 0,
            'disability': 0,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='No disability-related services or programs mentioned'
    )
    
    # Community programs
    analyzer.add_page_analysis(
        page_name='Community Programs',
        url='https://www.unioncountysheriffsoffice.com/community',
        word_count=1000,
        keyword_counts={
            'autism': 0,
            'disability': 0,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='No autism or disability-specific community programs'
    )
    
    # Training page
    analyzer.add_page_analysis(
        page_name='Training',
        url='https://www.unioncountysheriffsoffice.com/training',
        word_count=900,
        keyword_counts={
            'autism': 0,
            'disability': 0,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='No autism or disability training programs mentioned'
    )
    
    # Policies page
    analyzer.add_page_analysis(
        page_name='Policies',
        url='https://www.unioncountysheriffsoffice.com/policies',
        word_count=2000,
        keyword_counts={
            'autism': 0,
            'disability': 1,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 1,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        },
        notes='One mention each of "disability" and "ADA" in general policy statements'
    )
    
    # Add key findings
    analyzer.add_finding(
        'awareness_gap',
        'Zero mentions of autism or autism spectrum disorder across all pages',
        'high'
    )
    
    analyzer.add_finding(
        'limited_disability_awareness',
        'Only 3 total mentions of disability-related terms across entire website',
        'high'
    )
    
    analyzer.add_finding(
        'no_specific_programs',
        'No autism or disability-specific programs, services, or training mentioned',
        'high'
    )
    
    analyzer.add_finding(
        'no_accessibility_info',
        'No information about accessibility accommodations or services',
        'medium'
    )
    
    # Add advocacy implications
    analyzer.add_advocacy_implication(
        'Critical need for autism awareness training',
        'Zero mentions of autism indicates complete lack of awareness and preparedness for serving autistic community members'
    )
    
    analyzer.add_advocacy_implication(
        'Blue Envelope Program would fill significant gap',
        'No existing programs or protocols for autism/disability interactions means Blue Envelope would be first structured approach'
    )
    
    analyzer.add_advocacy_implication(
        'Strong evidence for program necessity',
        'Website analysis provides concrete proof of need for disability awareness and training programs'
    )
    
    return analyzer

def create_awareness_gap_chart(analyzer):
    """Create a chart showing the awareness gap"""
    
    # Get the data
    total_mentions = analyzer.analysis_data['total_mentions']
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Union County Sheriff\'s Office: Disability Awareness Analysis', 
                 fontsize=16, fontweight='bold')
    
    # Chart 1: Keyword mentions
    keywords = list(total_mentions.keys())
    counts = list(total_mentions.values())
    colors = ['#e74c3c' if count == 0 else '#f39c12' if count <= 2 else '#27ae60' for count in counts]
    
    bars = ax1.bar(range(len(keywords)), counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.set_title('Keyword Mentions Across Website', fontweight='bold', fontsize=14)
    ax1.set_xlabel('Keywords', fontweight='bold')
    ax1.set_ylabel('Number of Mentions', fontweight='bold')
    ax1.set_xticks(range(len(keywords)))
    ax1.set_xticklabels([k.replace('_', '\n').title() for k in keywords], rotation=45, ha='right')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Chart 2: Awareness level assessment
    awareness_levels = ['Autism\nAwareness', 'Disability\nAwareness', 'ADA\nCompliance', 'Accessibility\nServices']
    awareness_scores = [0, 1, 1, 0]  # Based on findings
    colors2 = ['#e74c3c', '#f39c12', '#f39c12', '#e74c3c']
    
    bars2 = ax2.bar(awareness_levels, awareness_scores, color=colors2, alpha=0.8, edgecolor='black', linewidth=1)
    ax2.set_title('Awareness Level Assessment', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Awareness Score (0-3)', fontweight='bold')
    ax2.set_ylim(0, 3)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, score in zip(bars2, awareness_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{score}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Add legend
    legend_elements = [
        plt.Rectangle((0,0),1,1, facecolor='#e74c3c', alpha=0.8, label='No Awareness (0)'),
        plt.Rectangle((0,0),1,1, facecolor='#f39c12', alpha=0.8, label='Limited Awareness (1-2)'),
        plt.Rectangle((0,0),1,1, facecolor='#27ae60', alpha=0.8, label='Good Awareness (3+)')
    ]
    ax1.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('assets/union_county_awareness_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return 'assets/union_county_awareness_analysis.png'

def main():
    """Main function to run the example analysis"""
    print("🔍 Union County Sheriff's Office - Example Analysis")
    print("="*60)
    print("This is an EXAMPLE analysis based on typical law enforcement websites.")
    print("Replace this data with your actual manual analysis results.")
    print()
    
    # Create example analysis
    analyzer = create_example_analysis()
    
    # Print summary
    analyzer.print_analysis_summary()
    
    # Save analysis
    report = analyzer.save_analysis('union_county_example_analysis.json')
    
    # Create awareness gap chart
    chart_path = create_awareness_gap_chart(analyzer)
    print(f"\n📊 Awareness gap chart created: {chart_path}")
    
    # Print executive summary
    print(f"\n📋 EXECUTIVE SUMMARY:")
    print(report['executive_summary'])
    
    print(f"\n💡 RECOMMENDATIONS:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print(f"\n🎯 ADVOCACY IMPACT:")
    print("This analysis provides concrete evidence that:")
    print("• Union County Sheriff's Office has minimal awareness of autism/disability issues")
    print("• There's a critical need for training and education")
    print("• The Blue Envelope Program would fill a significant gap")
    print("• This data can be used to demonstrate the necessity of the program")
    
    print(f"\n📝 NEXT STEPS:")
    print("1. Conduct actual manual analysis of the website")
    print("2. Replace example data with real findings")
    print("3. Use results in advocacy presentations")
    print("4. Include in Blue Envelope Program proposals")

if __name__ == "__main__":
    main()
