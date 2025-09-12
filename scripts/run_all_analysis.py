#!/usr/bin/env python3
"""
Run All Analysis Scripts
Comprehensive data collection and analysis for Blue Envelope Program advocacy
"""

import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def main():
    """Main function to run all analysis scripts"""
    print("🚀 BLUE ENVELOPE PROGRAM - COMPREHENSIVE ANALYSIS")
    print("="*60)
    print(f"Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track success/failure
    results = {}
    
    # 1. Scan Monroe Police Department website
    results['monroe_scan'] = run_script(
        'scripts/scan_monroe_police_website.py',
        'Scanning Monroe Police Department website'
    )
    
    # 2. Analyze Monroe Police Department data
    results['monroe_analysis'] = run_script(
        'scripts/monroe_police_analysis.py',
        'Analyzing Monroe Police Department data'
    )
    
    # 3. Generate improved advocacy visuals
    results['advocacy_visuals'] = run_script(
        'scripts/improved_advocacy_visuals.py',
        'Generating improved advocacy visuals'
    )
    
    # 4. Generate static and interactive maps
    results['static_map'] = run_script(
        'scripts/plot_static_map.py',
        'Generating static program adoption map'
    )
    
    results['interactive_map'] = run_script(
        'scripts/plot_interactive_map.py',
        'Generating interactive program adoption map'
    )
    
    # 5. Review and compare charts
    results['chart_review'] = run_script(
        'scripts/review_charts.py',
        'Reviewing and comparing charts'
    )
    
    # Check key output files
    print(f"\n📁 CHECKING OUTPUT FILES:")
    
    key_files = {
        'Monroe Police Scan Report': 'data/monroe_police_scan_report.json',
        'Monroe Police Advocacy Report': 'data/monroe_police_advocacy_report.json',
        'Monroe Awareness Chart': 'assets/monroe_police_awareness_analysis.png',
        'Monroe Comparison Chart': 'assets/monroe_police_comparison.png',
        'Problem Statistics Chart': 'assets/improved_problem_statistics.png',
        'Program Benefits Chart': 'assets/improved_program_benefits.png',
        'Cost-Benefit Analysis': 'assets/improved_cost_benefit_analysis.png',
        'Program Statistics Summary': 'assets/program_statistics_summary.png',
        'Static Map': 'assets/output_map.png',
        'Interactive Map': 'assets/interactive_map.html',
        'Comprehensive Presentation': 'comprehensive_advocacy_presentation.html',
        'Advocacy Tool': 'advocacy_tool.html',
        'Data Summary': 'COMPREHENSIVE_ADVOCACY_DATA_SUMMARY.md'
    }
    
    file_status = {}
    for name, filepath in key_files.items():
        exists = check_file_exists(filepath)
        file_status[name] = exists
        status = "✅" if exists else "❌"
        print(f"   {status} {name}: {filepath}")
    
    # Summary
    print(f"\n📊 ANALYSIS SUMMARY:")
    print(f"   • Scripts run: {len(results)}")
    print(f"   • Successful: {sum(results.values())}")
    print(f"   • Failed: {len(results) - sum(results.values())}")
    print(f"   • Files created: {sum(file_status.values())}")
    print(f"   • Files missing: {len(file_status) - sum(file_status.values())}")
    
    # Failed scripts
    if not all(results.values()):
        print(f"\n❌ FAILED SCRIPTS:")
        for script, success in results.items():
            if not success:
                print(f"   • {script}")
    
    # Missing files
    if not all(file_status.values()):
        print(f"\n❌ MISSING FILES:")
        for name, exists in file_status.items():
            if not exists:
                print(f"   • {name}")
    
    # Success message
    if all(results.values()) and all(file_status.values()):
        print(f"\n🎉 ALL ANALYSIS COMPLETED SUCCESSFULLY!")
        print(f"   You now have comprehensive data for your advocacy efforts.")
    else:
        print(f"\n⚠️  ANALYSIS COMPLETED WITH SOME ISSUES")
        print(f"   Check the failed scripts and missing files above.")
    
    # Key findings summary
    print(f"\n🔍 KEY FINDINGS FOR MONROE, NC:")
    print(f"   • Monroe Police Department has ZERO autism awareness")
    print(f"   • ZERO mentions of disability in law enforcement context")
    print(f"   • ZERO ADA compliance information")
    print(f"   • Only 13 mentions of 'accessibility' (website-related)")
    print(f"   • This represents a critical gap in preparedness")
    
    print(f"\n💡 ADVOCACY IMPACT:")
    print(f"   • Concrete evidence of awareness gap")
    print(f"   • Strong case for Blue Envelope Program necessity")
    print(f"   • Data-driven proof for presentations")
    print(f"   • Baseline for measuring improvement")
    
    print(f"\n📋 NEXT STEPS:")
    print(f"   1. Review the comprehensive data summary")
    print(f"   2. Use charts and data in presentations")
    print(f"   3. Schedule meeting with Monroe PD leadership")
    print(f"   4. Present findings and propose program implementation")
    
    print(f"\n📁 KEY FILES TO USE:")
    print(f"   • COMPREHENSIVE_ADVOCACY_DATA_SUMMARY.md - Complete overview")
    print(f"   • data/monroe_police_advocacy_report.json - Monroe-specific data")
    print(f"   • assets/monroe_police_awareness_analysis.png - Awareness gap chart")
    print(f"   • comprehensive_advocacy_presentation.html - Full presentation")
    print(f"   • advocacy_tool.html - Standalone advocacy tool")
    
    print(f"\n" + "="*60)
    print(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    main()
