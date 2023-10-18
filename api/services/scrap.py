import requests
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

def scrape_website(url):
    """
    Scrape all text content from a website.
    
    Parameters:
    url (str): The URL of the website to scrape.
    
    Returns:
    str: All text content from the website.
    """
    # Send a request to the URL and get the HTML content
    response = requests.get(url)
    html = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract all text content
    text_content = soup.get_text()
    output_pdf_path="output.pdf"
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

    # Create a list to hold the content (can include paragraphs, images, etc.)
    content = []

    # Create a style for the content
    style = getSampleStyleSheet()["Normal"]

    # Add the string content to the PDF
    content.append(Paragraph(text_content, style))

    # Build the PDF
    doc.build(content)
    return output_pdf_path

    # return text_content


# # Example usage
# url = "https://www.caliber.com/find-a-location"
# scraped_text = scrape_website(url)
# print("Scraped text:")
# print(scraped_text)