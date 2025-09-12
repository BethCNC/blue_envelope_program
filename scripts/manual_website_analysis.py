import json
from datetime import datetime
import os

class ManualWebsiteAnalysis:
    def __init__(self):
        self.analysis_data = {
            'scan_date': datetime.now().isoformat(),
            'website': 'https://www.unioncountysheriffsoffice.com',
            'analysis_method': 'Manual Analysis',
            'pages_analyzed': [],
            'total_mentions': {
                'autism': 0,
                'disability': 0,
                'disabled': 0,
                'disabled_rights': 0,
                'ada': 0,
                'americans_with_disabilities': 0,
                'accessibility': 0,
                'accommodation': 0
            },
            'key_findings': [],
            'advocacy_implications': []
        }
    
    def add_page_analysis(self, page_name, url, word_count, keyword_counts, notes=""):
        """Add analysis results for a single page"""
        page_data = {
            'page_name': page_name,
            'url': url,
            'word_count': word_count,
            'keyword_counts': keyword_counts,
            'notes': notes,
            'total_mentions': sum(keyword_counts.values())
        }
        
        self.analysis_data['pages_analyzed'].append(page_data)
        
        # Add to total counts
        for keyword, count in keyword_counts.items():
            self.analysis_data['total_mentions'][keyword] += count
    
    def add_finding(self, finding_type, description, impact_level="medium"):
        """Add a key finding"""
        finding = {
            'type': finding_type,
            'description': description,
            'impact_level': impact_level,
            'timestamp': datetime.now().isoformat()
        }
        self.analysis_data['key_findings'].append(finding)
    
    def add_advocacy_implication(self, implication, evidence):
        """Add an advocacy implication"""
        implication_data = {
            'implication': implication,
            'evidence': evidence,
            'timestamp': datetime.now().isoformat()
        }
        self.analysis_data['advocacy_implications'].append(implication_data)
    
    def generate_summary_statistics(self):
        """Generate summary statistics"""
        total_pages = len(self.analysis_data['pages_analyzed'])
        total_words = sum(page['word_count'] for page in self.analysis_data['pages_analyzed'])
        total_mentions = sum(self.analysis_data['total_mentions'].values())
        
        pages_with_mentions = [page for page in self.analysis_data['pages_analyzed'] if page['total_mentions'] > 0]
        
        return {
            'total_pages_analyzed': total_pages,
            'total_words_scanned': total_words,
            'total_mentions_found': total_mentions,
            'pages_with_mentions': len(pages_with_mentions),
            'percentage_pages_with_mentions': round((len(pages_with_mentions) / total_pages) * 100, 2) if total_pages > 0 else 0,
            'mentions_per_1000_words': round((total_mentions / total_words) * 1000, 2) if total_words > 0 else 0
        }
    
    def generate_advocacy_report(self):
        """Generate a report for advocacy purposes"""
        stats = self.generate_summary_statistics()
        
        report = {
            'executive_summary': self.create_executive_summary(stats),
            'detailed_findings': self.analysis_data,
            'statistics': stats,
            'recommendations': self.generate_recommendations(stats)
        }
        
        return report
    
    def create_executive_summary(self, stats):
        """Create an executive summary"""
        total_mentions = stats['total_mentions_found']
        
        if total_mentions == 0:
            summary = "CRITICAL FINDING: The Union County Sheriff's Office website contains ZERO mentions of autism, disability, accessibility, or related terms across all analyzed pages. This represents a significant gap in awareness and preparedness for serving community members with disabilities."
        elif total_mentions <= 2:
            summary = f"MINIMAL AWARENESS: The Union County Sheriff's Office website contains only {total_mentions} mention(s) of autism, disability, or accessibility-related terms. This indicates very limited awareness of disability issues and the need for enhanced training and programs."
        elif total_mentions <= 5:
            summary = f"LIMITED AWARENESS: The Union County Sheriff's Office website contains {total_mentions} mentions of autism, disability, or accessibility-related terms. While some awareness exists, there is significant room for improvement in disability inclusion and training."
        else:
            summary = f"MODERATE AWARENESS: The Union County Sheriff's Office website contains {total_mentions} mentions of autism, disability, or accessibility-related terms. This shows some awareness, but the Blue Envelope Program could still provide valuable structure and training."
        
        return summary
    
    def generate_recommendations(self, stats):
        """Generate recommendations based on findings"""
        total_mentions = stats['total_mentions_found']
        
        recommendations = []
        
        if total_mentions == 0:
            recommendations.extend([
                "Implement comprehensive disability awareness training for all officers",
                "Develop clear policies for interacting with individuals with disabilities",
                "Create accessible communication materials and procedures",
                "Establish partnerships with local disability organizations",
                "Consider the Blue Envelope Program as a structured approach to improving interactions"
            ])
        elif total_mentions <= 2:
            recommendations.extend([
                "Expand existing disability awareness efforts",
                "Develop specific training modules for autism and sensory needs",
                "Create clear protocols for traffic stops involving individuals with disabilities",
                "Implement the Blue Envelope Program to provide structured support"
            ])
        else:
            recommendations.extend([
                "Build upon existing awareness with structured programs",
                "Consider the Blue Envelope Program as an enhancement to current efforts",
                "Develop metrics to measure the effectiveness of disability-related programs"
            ])
        
        return recommendations
    
    def save_analysis(self, filename='union_county_manual_analysis.json'):
        """Save the analysis to a JSON file"""
        report = self.generate_advocacy_report()
        
        with open(f'data/{filename}', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Analysis saved to data/{filename}")
        return report
    
    def print_analysis_summary(self):
        """Print a summary of the analysis"""
        stats = self.generate_summary_statistics()
        
        print("\n" + "="*70)
        print("UNION COUNTY SHERIFF'S OFFICE - MANUAL WEBSITE ANALYSIS")
        print("="*70)
        
        print(f"\n📊 ANALYSIS SUMMARY:")
        print(f"   • Pages analyzed: {stats['total_pages_analyzed']}")
        print(f"   • Total words scanned: {stats['total_words_scanned']:,}")
        print(f"   • Pages with mentions: {stats['pages_with_mentions']}")
        print(f"   • Percentage with mentions: {stats['percentage_pages_with_mentions']}%")
        
        print(f"\n🔍 KEYWORD MENTIONS FOUND:")
        for keyword, count in self.analysis_data['total_mentions'].items():
            status = "❌" if count == 0 else "✅"
            print(f"   {status} {keyword.replace('_', ' ').title()}: {count}")
        
        print(f"\n📈 STATISTICS:")
        print(f"   • Total mentions: {stats['total_mentions_found']}")
        print(f"   • Mentions per 1,000 words: {stats['mentions_per_1000_words']}")
        
        if self.analysis_data['pages_analyzed']:
            print(f"\n📄 PAGES ANALYZED:")
            for page in self.analysis_data['pages_analyzed']:
                if page['total_mentions'] > 0:
                    print(f"   • {page['page_name']} ({page['total_mentions']} mentions)")
                    for keyword, count in page['keyword_counts'].items():
                        if count > 0:
                            print(f"     - {keyword.replace('_', ' ').title()}: {count}")
                else:
                    print(f"   • {page['page_name']} (0 mentions)")
        
        print(f"\n💡 ADVOCACY IMPLICATIONS:")
        for implication in self.analysis_data['advocacy_implications']:
            print(f"   • {implication['implication']}")
            print(f"     Evidence: {implication['evidence']}")
        
        print("="*70)

def create_analysis_template():
    """Create a template for manual analysis"""
    template = {
        'instructions': {
            'how_to_analyze': [
                '1. Visit https://www.unioncountysheriffsoffice.com in your browser',
                '2. Navigate through all main pages and sections',
                '3. For each page, use Ctrl+F (Cmd+F on Mac) to search for keywords',
                '4. Count the number of occurrences for each keyword',
                '5. Note any relevant content or policies found',
                '6. Record your findings using the analysis tool'
            ],
            'keywords_to_search': [
                'autism', 'autistic', 'autism spectrum',
                'disability', 'disabilities', 'disabled',
                'disabled rights', 'disability rights',
                'ADA', 'Americans with Disabilities',
                'accessibility', 'accessible',
                'accommodation', 'accommodate', 'reasonable accommodation'
            ],
            'pages_to_check': [
                'Home page',
                'About Us / About the Sheriff',
                'Services / Programs',
                'Community Programs',
                'Training / Education',
                'Policies / Procedures',
                'Contact / Information',
                'News / Press Releases',
                'Resources / Links',
                'Employment / Careers',
                'Public Safety',
                'Community Outreach'
            ]
        },
        'expected_findings': {
            'hypothesis': 'Based on typical law enforcement websites, we expect to find:',
            'predictions': [
                '0-2 mentions of autism/autistic',
                '1-5 mentions of disability/disabilities (likely in general context)',
                '0-1 mentions of ADA or accessibility',
                '0 mentions of disability rights or accommodations',
                'Most mentions will be in general policy statements, not specific programs'
            ]
        },
        'analysis_tool_usage': {
            'step_1': 'Create an instance: analyzer = ManualWebsiteAnalysis()',
            'step_2': 'Add each page: analyzer.add_page_analysis(page_name, url, word_count, keyword_counts)',
            'step_3': 'Add findings: analyzer.add_finding(type, description)',
            'step_4': 'Add implications: analyzer.add_advocacy_implication(implication, evidence)',
            'step_5': 'Save results: analyzer.save_analysis()',
            'step_6': 'Print summary: analyzer.print_analysis_summary()'
        }
    }
    
    with open('data/manual_analysis_template.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("Manual analysis template created: data/manual_analysis_template.json")
    return template

def main():
    """Main function to demonstrate the manual analysis tool"""
    print("🔍 Union County Sheriff's Office - Manual Analysis Tool")
    print("="*60)
    
    # Create analysis template
    create_analysis_template()
    
    print("\n📋 MANUAL ANALYSIS INSTRUCTIONS:")
    print("Since the website blocks automated requests, you'll need to analyze it manually.")
    print("\n1. Visit https://www.unioncountysheriffsoffice.com in your browser")
    print("2. Use Ctrl+F (Cmd+F on Mac) to search for each keyword")
    print("3. Record the count for each keyword on each page")
    print("4. Use this tool to document your findings")
    
    print("\n🔧 HOW TO USE THE ANALYSIS TOOL:")
    print("```python")
    print("from scripts.manual_website_analysis import ManualWebsiteAnalysis")
    print("")
    print("# Create analyzer")
    print("analyzer = ManualWebsiteAnalysis()")
    print("")
    print("# Add each page you analyzed")
    print("analyzer.add_page_analysis(")
    print("    page_name='Home Page',")
    print("    url='https://www.unioncountysheriffsoffice.com',")
    print("    word_count=1500,")
    print("    keyword_counts={'autism': 0, 'disability': 1, 'ada': 0},")
    print("    notes='Found one mention of disability in general policy'")
    print(")")
    print("")
    print("# Add key findings")
    print("analyzer.add_finding('awareness_gap', 'No autism-specific content found')")
    print("")
    print("# Add advocacy implications")
    print("analyzer.add_advocacy_implication(")
    print("    'Need for training',")
    print("    'Zero mentions of autism indicates lack of awareness'")
    print(")")
    print("")
    print("# Save and print results")
    print("analyzer.save_analysis()")
    print("analyzer.print_analysis_summary()")
    print("```")
    
    print("\n💡 ADVOCACY VALUE:")
    print("This analysis will provide concrete evidence of:")
    print("• Current awareness level of autism/disability issues")
    print("• Gaps in training and preparedness")
    print("• Need for the Blue Envelope Program")
    print("• Baseline for measuring improvement after implementation")

if __name__ == "__main__":
    main()
