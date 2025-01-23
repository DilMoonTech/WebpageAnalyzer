import requests
from bs4 import BeautifulSoup
from collections import Counter
from typing import Dict, List, Any

class WebpageAnalyzer:
    def __init__(self, url: str):
        self.url = url
        self.soup = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_page(self) -> None:
        """Fetch the webpage content"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch webpage: {str(e)}")

    def analyze(self) -> Dict[str, Any]:
        """Analyze the webpage structure and return statistics"""
        if not self.soup:
            self.fetch_page()

        stats = {
            'tag_count': self._count_tags(),
            'meta_info': self._analyze_meta(),
            'links_analysis': self._analyze_links(),
            'heading_structure': self._analyze_headings(),
            'images': self._analyze_images(),
            'text_stats': self._analyze_text()
        }

        return stats

    def _count_tags(self) -> Dict[str, int]:
        """Count occurrence of each HTML tag"""
        all_tags = self.soup.find_all(True)
        return dict(Counter(tag.name for tag in all_tags))

    def _analyze_meta(self) -> Dict[str, str]:
        """Analyze meta tags"""
        meta_info = {}
        for meta in self.soup.find_all('meta'):
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                meta_info[name] = content
        return meta_info

    def _analyze_links(self) -> Dict[str, Any]:
        """Analyze links in the webpage"""
        links = self.soup.find_all('a')
        internal_links = []
        external_links = []
        
        for link in links:
            href = link.get('href', '')
            if href.startswith('http'):
                external_links.append(href)
            elif href and not href.startswith('#'):
                internal_links.append(href)

        return {
            'total_links': len(links),
            'internal_links_count': len(internal_links),
            'external_links_count': len(external_links)
        }

    def _analyze_headings(self) -> Dict[str, int]:
        """Analyze heading structure"""
        headings = {}
        for i in range(1, 7):
            count = len(self.soup.find_all(f'h{i}'))
            if count > 0:
                headings[f'h{i}'] = count
        return headings

    def _analyze_images(self) -> Dict[str, Any]:
        """Analyze images in the webpage"""
        images = self.soup.find_all('img')
        return {
            'total_images': len(images),
            'images_with_alt': len([img for img in images if img.get('alt')])
        }

    def _analyze_text(self) -> Dict[str, Any]:
        """Analyze text content"""
        text = self.soup.get_text()
        words = text.split()
        return {
            'word_count': len(words),
            'character_count': len(text)
        }
