import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_sitemaps(url):
    sitemaps = set()  # To store unique sitemap URLs

    # Send an HTTP request to the URL
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the content from {url}")
        return sitemaps

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all 'sitemap' elements
    for element in soup.find_all('sitemap'):
        loc = element.find('loc')
        if loc:
            sitemap_url = loc.text.strip()
            sitemaps.add(sitemap_url)

    # Find all 'urlset' elements with child 'url' elements
    for element in soup.find_all('urlset'):
        for url_element in element.find_all('url'):
            loc = url_element.find('loc')
            if loc:
                sitemap_url = loc.text.strip()
                sitemaps.add(sitemap_url)

    # Ensure all URLs are absolute
    sitemaps = [urljoin(url, sitemap) for sitemap in sitemaps]

    return sitemaps

# # Example usage
# url = "https://www.sitemaps.org/sitemap.xml"
# sitemaps = extract_sitemaps(url)
# print("Sitemaps found:")

# for sitemap in sitemaps:
    # print(sitemap)
from bs4 import BeautifulSoup
import requests

def extract_urls_from_html(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = []

    # Extract URLs from <a> tags
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']

        # Check if the URL starts with 'http' or 'https' to ensure it's web-scrapable
        if href.startswith('http') or href.startswith('https'):
            urls.append(href)


    return urls

