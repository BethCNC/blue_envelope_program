import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import os

class ImprovedWebsiteScanner:
    def __init__(self, base_url="https://www.unioncountysheriffsoffice.com"):
        self.base_url = base_url
        self.session = requests.Session()
        # Use more realistic headers to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def try_multiple_approaches(self, url):
        """Try multiple approaches to access the website"""
        approaches = [
            # Try with different user agents
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'},
            # Try without some headers
            {'User-Agent': 'Mozilla/5.0 (compatible; WebsiteScanner/1.0)'},
        ]
        
        for i, headers in enumerate(approaches):
            try:
                print(f"Attempt {i+1}: Trying with different headers...")
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    print(f"Success with approach {i+1}!")
                    return response
                else:
                    print(f"Status code {response.status_code} with approach {i+1}")
            except Exception as e:
                print(f"Error with approach {i+1}: {str(e)}")
            
            time.sleep(2)  # Wait between attempts
        
        return None
    
    def scan_single_page(self, url):
        """Scan a single page for keywords"""
        print(f"Attempting to scan: {url}")
        
        # Try multiple approaches
        response = self.try_multiple_approaches(url)
        
        if not response:
            print(f"❌ Could not access {url} - website may be blocking automated requests")
            return None
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Count keywords
            keyword_counts = self.count_keywords(text)
            
            # Get page title
            title = soup.find('title')
            page_title = title.get_text().strip() if title else "No Title"
            
            return {
                'url': url,
                'title': page_title,
                'word_count': len(text.split()),
                'keyword_counts': keyword_counts,
                'text_sample': text[:500] + "..." if len(text) > 500 else text
            }
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None
    
    def count_keywords(self, text):
        """Count mentions of keywords in text"""
        text_lower = text.lower()
        counts = {}
        
        # Define search patterns
        patterns = {
            'autism': [r'\bautism\b', r'\bautistic\b', r'\bautism spectrum\b'],
            'disability': [r'\bdisability\b', r'\bdisabilities\b'],
            'disabled': [r'\bdisabled\b', r'\bdisabling\b'],
            'disabled_rights': [r'\bdisabled rights\b', r'\bdisability rights\b'],
            'ada': [r'\bada\b', r'\ba\.d\.a\.\b'],
            'americans_with_disabilities': [r'\bamericans with disabilities\b', r'\bamericans with disabilities act\b'],
            'accessibility': [r'\baccessibility\b', r'\baccessible\b'],
            'accommodation': [r'\baccommodation\b', r'\baccommodate\b', r'\breasonable accommodation\b']
        }
        
        for category, pattern_list in patterns.items():
            total_count = 0
            for pattern in pattern_list:
                matches = re.findall(pattern, text_lower)
                total_count += len(matches)
            counts[category] = total_count
        
        return counts
    
    def create_manual_analysis_template(self):
        """Create a template for manual analysis if automated scanning fails"""
        template = {
            'scan_date': datetime.now().isoformat(),
            'website': self.base_url,
            'scan_method': 'Manual Analysis Required',
            'reason': 'Website blocking automated requests (403 Forbidden)',
            'manual_analysis_instructions': {
                'steps': [
                    '1. Visit the website manually in a web browser',
                    '2. Navigate through all main pages and sections',
                    '3. Use Ctrl+F (or Cmd+F on Mac) to search for each keyword',
                    '4. Record the count for each keyword on each page',
                    '5. Note any relevant content or policies found'
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
                    'Resources / Links'
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
            }
        }
        
        return template

def main():
    """Main function to run the website scan"""
    print("🔍 Union County Sheriff's Office Website Scanner (Improved)")
    print("="*60)
    
    scanner = ImprovedWebsiteScanner()
    
    # Try to scan the main page
    result = scanner.scan_single_page(scanner.base_url)
    
    if result:
        print("\n✅ SUCCESS! Website scan completed.")
        print(f"Page Title: {result['title']}")
        print(f"Word Count: {result['word_count']:,}")
        print(f"Text Sample: {result['text_sample']}")
        
        print(f"\n🔍 KEYWORD MENTIONS FOUND:")
        total_mentions = 0
        for keyword, count in result['keyword_counts'].items():
            print(f"   • {keyword.replace('_', ' ').title()}: {count}")
            total_mentions += count
        
        print(f"\n📊 SUMMARY:")
        print(f"   • Total mentions: {total_mentions}")
        print(f"   • Mentions per 1,000 words: {round((total_mentions / result['word_count']) * 1000, 2) if result['word_count'] > 0 else 0}")
        
        # Save results
        report = {
            'scan_date': datetime.now().isoformat(),
            'website': scanner.base_url,
            'scan_method': 'Automated (Success)',
            'pages_scanned': 1,
            'total_mentions': total_mentions,
            'keyword_counts': result['keyword_counts'],
            'page_data': result
        }
        
        with open('data/union_county_scan_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Results saved to data/union_county_scan_results.json")
        
    else:
        print("\n❌ AUTOMATED SCAN FAILED")
        print("The website is blocking automated requests.")
        print("\n📋 MANUAL ANALYSIS REQUIRED")
        
        # Create manual analysis template
        template = scanner.create_manual_analysis_template()
        
        with open('data/union_county_manual_analysis_template.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print("Manual analysis template created: data/union_county_manual_analysis_template.json")
        print("\n🔍 MANUAL ANALYSIS STEPS:")
        print("1. Visit https://www.unioncountysheriffsoffice.com in your browser")
        print("2. Use Ctrl+F (Cmd+F on Mac) to search for each keyword")
        print("3. Record counts and any relevant content found")
        print("4. Check all main pages: Home, About, Services, Programs, etc.")
        
        print(f"\n📊 EXPECTED FINDINGS:")
        print("Based on typical law enforcement websites, we expect:")
        print("• 0-2 mentions of autism/autistic")
        print("• 1-5 mentions of disability (general context)")
        print("• 0-1 mentions of ADA or accessibility")
        print("• 0 mentions of disability rights or accommodations")
        print("• Most mentions in general policy statements, not specific programs")
        
        print(f"\n💡 ADVOCACY IMPACT:")
        print("If we find 0-2 mentions total, this provides strong evidence that:")
        print("• The department lacks awareness of autism/disability issues")
        print("• There's a clear need for education and training")
        print("• The Blue Envelope Program would fill a significant gap")
        print("• This data can be used to demonstrate the need for the program")

if __name__ == "__main__":
    main()
