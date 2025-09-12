import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse
import json
from datetime import datetime
import os

class MonroePoliceWebsiteScanner:
    def __init__(self, base_url="https://www.monroenc.org"):
        self.base_url = base_url
        self.police_section_url = "https://www.monroenc.org/250/Police"
        self.visited_urls = set()
        self.pages_data = []
        self.total_mentions = {
            'autism': 0,
            'disability': 0,
            'disabled': 0,
            'disabled_rights': 0,
            'ada': 0,
            'americans_with_disabilities': 0,
            'accessibility': 0,
            'accommodation': 0
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def is_valid_url(self, url):
        """Check if URL is valid and belongs to Monroe, NC domain"""
        try:
            parsed = urlparse(url)
            return (parsed.netloc == 'www.monroenc.org' and 
                    parsed.scheme in ['http', 'https'] and
                    not any(ext in url.lower() for ext in ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3']))
        except:
            return False
    
    def extract_text_content(self, soup):
        """Extract all text content from the page"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
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
    
    def scan_page(self, url, page_name=""):
        """Scan a single page for keywords"""
        try:
            print(f"Scanning: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = self.extract_text_content(soup)
            
            # Count keywords
            keyword_counts = self.count_keywords(text_content)
            
            # Get page title
            title = soup.find('title')
            page_title = title.get_text().strip() if title else page_name or "No Title"
            
            # Store page data
            page_data = {
                'url': url,
                'title': page_title,
                'page_name': page_name,
                'word_count': len(text_content.split()),
                'keyword_counts': keyword_counts,
                'has_content': len(text_content) > 100,
                'text_sample': text_content[:500] + "..." if len(text_content) > 500 else text_content
            }
            
            self.pages_data.append(page_data)
            
            # Add to total counts
            for category, count in keyword_counts.items():
                self.total_mentions[category] += count
            
            return page_data
            
        except Exception as e:
            print(f"Error scanning {url}: {str(e)}")
            return None
    
    def find_police_related_links(self, soup, current_url):
        """Find links related to police department"""
        links = set()
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            
            if self.is_valid_url(full_url):
                # Look for police-related pages
                link_text = link.get_text().lower()
                url_lower = full_url.lower()
                
                police_keywords = [
                    'police', 'law enforcement', 'sheriff', 'public safety',
                    'crime', 'safety', 'emergency', '911', 'dispatch',
                    'community', 'watch', 'patrol', 'investigation',
                    'training', 'recruitment', 'accreditation', 'complaint'
                ]
                
                if any(keyword in link_text or keyword in url_lower for keyword in police_keywords):
                    links.add(full_url)
        
        return links
    
    def scan_monroe_police_website(self, max_pages=20):
        """Scan Monroe Police Department website"""
        print(f"Starting scan of Monroe Police Department website")
        print(f"Base URL: {self.base_url}")
        print(f"Police section: {self.police_section_url}")
        print(f"Maximum pages to scan: {max_pages}")
        
        # Start with the police section page
        urls_to_visit = [self.police_section_url]
        pages_scanned = 0
        
        while urls_to_visit and pages_scanned < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            self.visited_urls.add(current_url)
            
            # Determine page name based on URL
            page_name = self.get_page_name_from_url(current_url)
            
            page_data = self.scan_page(current_url, page_name)
            
            if page_data and page_data['has_content']:
                pages_scanned += 1
                
                # Get links from this page for further scanning
                try:
                    response = self.session.get(current_url, timeout=15)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    new_links = self.find_police_related_links(soup, current_url)
                    
                    # Add new links to visit queue
                    for link in new_links:
                        if link not in self.visited_urls and link not in urls_to_visit:
                            urls_to_visit.append(link)
                            
                except Exception as e:
                    print(f"Error getting links from {current_url}: {str(e)}")
            
            # Be respectful - add delay between requests
            time.sleep(1)
        
        print(f"\nScan complete! Scanned {pages_scanned} pages.")
        return self.pages_data
    
    def get_page_name_from_url(self, url):
        """Extract page name from URL"""
        if 'police' in url.lower():
            if 'community' in url.lower():
                return 'Community Programs'
            elif 'training' in url.lower():
                return 'Training'
            elif 'recruitment' in url.lower():
                return 'Recruitment'
            elif 'accreditation' in url.lower():
                return 'Accreditation'
            elif 'complaint' in url.lower():
                return 'Complaints'
            else:
                return 'Police Department'
        elif 'sheriff' in url.lower():
            return 'Sheriff Office'
        elif 'public-safety' in url.lower():
            return 'Public Safety'
        else:
            return 'General Page'
    
    def generate_report(self):
        """Generate a comprehensive report"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'website': self.base_url,
            'police_section': self.police_section_url,
            'total_pages_scanned': len(self.pages_data),
            'total_mentions': self.total_mentions,
            'pages_with_mentions': [],
            'summary_statistics': {},
            'detailed_pages': []
        }
        
        # Find pages with mentions
        for page in self.pages_data:
            total_page_mentions = sum(page['keyword_counts'].values())
            if total_page_mentions > 0:
                report['pages_with_mentions'].append({
                    'url': page['url'],
                    'title': page['title'],
                    'page_name': page['page_name'],
                    'total_mentions': total_page_mentions,
                    'keyword_counts': page['keyword_counts']
                })
        
        # Calculate summary statistics
        total_words_scanned = sum(page['word_count'] for page in self.pages_data)
        total_mentions_all = sum(self.total_mentions.values())
        
        report['summary_statistics'] = {
            'total_words_scanned': total_words_scanned,
            'total_mentions_found': total_mentions_all,
            'mentions_per_1000_words': round((total_mentions_all / total_words_scanned) * 1000, 2) if total_words_scanned > 0 else 0,
            'pages_with_any_mentions': len(report['pages_with_mentions']),
            'percentage_pages_with_mentions': round((len(report['pages_with_mentions']) / len(self.pages_data)) * 100, 2) if self.pages_data else 0
        }
        
        # Add detailed page information
        report['detailed_pages'] = self.pages_data
        
        return report
    
    def save_report(self, filename='monroe_police_scan_report.json'):
        """Save the report to a JSON file"""
        report = self.generate_report()
        
        with open(f'data/{filename}', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to data/{filename}")
        return report
    
    def print_summary(self):
        """Print a summary of findings"""
        report = self.generate_report()
        
        print("\n" + "="*70)
        print("MONROE POLICE DEPARTMENT WEBSITE SCAN RESULTS")
        print("="*70)
        
        print(f"\n📊 SCAN SUMMARY:")
        print(f"   • Total pages scanned: {report['total_pages_scanned']}")
        print(f"   • Total words scanned: {report['summary_statistics']['total_words_scanned']:,}")
        print(f"   • Pages with mentions: {report['summary_statistics']['pages_with_any_mentions']}")
        print(f"   • Percentage of pages with mentions: {report['summary_statistics']['percentage_pages_with_mentions']}%")
        
        print(f"\n🔍 KEYWORD MENTIONS FOUND:")
        for keyword, count in self.total_mentions.items():
            if count > 0:
                print(f"   ✅ {keyword.replace('_', ' ').title()}: {count}")
            else:
                print(f"   ❌ {keyword.replace('_', ' ').title()}: 0")
        
        print(f"\n📈 STATISTICS:")
        print(f"   • Total mentions: {report['summary_statistics']['total_mentions_found']}")
        print(f"   • Mentions per 1,000 words: {report['summary_statistics']['mentions_per_1000_words']}")
        
        if report['pages_with_mentions']:
            print(f"\n📄 PAGES WITH MENTIONS:")
            for page in report['pages_with_mentions']:
                print(f"   • {page['page_name']} ({page['total_mentions']} mentions)")
                print(f"     URL: {page['url']}")
                for keyword, count in page['keyword_counts'].items():
                    if count > 0:
                        print(f"     - {keyword.replace('_', ' ').title()}: {count}")
                print()
        else:
            print(f"\n📄 NO PAGES WITH MENTIONS FOUND")
            print("   This indicates a significant gap in autism/disability awareness")
        
        print("="*70)

def main():
    """Main function to run the Monroe Police website scan"""
    print("🔍 Monroe Police Department Website Scanner")
    print("Scanning for autism, disability, and accessibility mentions...")
    
    scanner = MonroePoliceWebsiteScanner()
    
    # Scan the website
    pages_data = scanner.scan_monroe_police_website(max_pages=15)
    
    # Generate and save report
    report = scanner.save_report()
    
    # Print summary
    scanner.print_summary()
    
    return report

if __name__ == "__main__":
    main()
