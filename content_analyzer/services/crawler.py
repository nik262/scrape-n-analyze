import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from django.utils import timezone
from content_analyzer.models import ContentSource, ContentItem

class WebCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def crawl_url(self, content_source):
        try:
            # Fetch the webpage
            response = self.session.get(content_source.url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = ' '.join([p.get_text().strip() for p in soup.find_all('p')])
            
            # Create ContentItem for the main text
            ContentItem.objects.create(
                source=content_source,
                content_type='text',
                raw_content=text_content
            )
            
            # Update ContentSource status
            content_source.status = 'active'
            content_source.last_crawled = timezone.now()
            content_source.save()
            
            return True
            
        except Exception as e:
            content_source.status = 'error'
            content_source.save()
            print(f"Error crawling {content_source.url}: {str(e)}")
            return False