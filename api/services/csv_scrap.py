

import csv
import re
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import requests
from bs4 import BeautifulSoup
import pdfkit
# n=0


def extract_urls_from_csv(file_path):
    """
    Extract URLs from a CSV file, searching in all columns.
    
    Parameters:
    file_path (str): The path to the CSV file.
    
    Returns:
    list: A list of URLs extracted from the CSV file.
    """
    urls = []

    try:
        # Check if the file is an Excel file (XLS or XLSX)
        if file_path.lower().endswith(('.xlsx')):
            # Convert Excel file to CSV
            csv_file_path = file_path.replace('.xlsx', '.csv')
            excel_to_csv(file_path, csv_file_path)
            file_path = csv_file_path
        elif file_path.lower().endswith(('.xls')):
            # Convert Excel file to CSV
            csv_file_path = file_path.replace('.xls', '.csv')
            excel_to_csv(file_path, csv_file_path)
            file_path = csv_file_path

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                for item in row:
                    # Use a regular expression to find URLs in the item
                    url_matches = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', item)
                    if url_matches:
                        urls.extend(url_matches)

    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    url_list =list(set(urls))
    return url_list

def excel_to_csv(input_file, output_file):
    """
    Convert an Excel file (XLS or XLSX) to a CSV file.
    
    Parameters:
    input_file (str): The path to the input Excel file.
    output_file (str): The path where the CSV file will be saved.
    
    Returns:
    None
    """
    try:
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(input_file)
        
        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        print("Conversion successful. CSV file saved at:", output_file)
    
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
# file_path = "C:/Users/Akash/Downloads/Caliber Collision LInks.xlsx"  # Replace with the actual file path

# url_list = extract_urls_from_csv(file_path)
# print("Extracted URLs:")

# print(len(url_list))
# print(url_list[107])

def scrape_websites_and_generate_pdf(urls):
    """
    Scrape data from a list of websites and generate a single PDF containing the combined data.
    
    Parameters:
    urls (list): A list of URLs to scrape.
    output_pdf_path (str): The path where the PDF will be saved.
    
    Returns:
    None
    """
    combined_data = ''
    error_urls = []
    # n=0
    for url in urls:
        
        # print(n)
        # n+=1
        try:
            # Send a request to the URL and get the HTML content
            response = requests.get(url)
            # response.raise_for_status()  # Raise an exception for bad requests

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all text content
            text_content = soup.get_text()
            combined_data += text_content + '\n\n'

        except requests.exceptions.RequestException as e:
            print("1",url)
            print(f"Error for URL '{url}': {str(e)}")
            error_urls.append(url)
            continue

        except Exception as e:
            print("1",url)
            print(f"An error occurred for URL '{url}': {str(e)}")
            error_urls.append(url)
            continue
    # print("data scraped >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(combined_data)
    # if combined_data:
    #     # Create a PDF containing the combined data from all successful URLs
    #     pdfkit.from_string(combined_data, output_pdf_path)
    #     print("PDF created successfully:", output_pdf_path)

    # if error_urls:
    #     print("URLs with errors:")
    #     for error_url in error_urls:
    #         print(error_url)
    return combined_data

# Example usage
# urls = url_list
# output_pdf_path = "output.pdf"  # Replace with the desired output PDF file path


# combine_data = scrape_websites_and_generate_pdf(urls)
# print("PDF created successfully:", output_pdf_path)



def convert_string_to_pdf(string_content, output_pdf_path):
    """
    Convert a string to a PDF and save it to the specified path.
    
    Parameters:
    string_content (str): The content to be included in the PDF.
    output_pdf_path (str): The path where the PDF will be saved.
    
    Returns:
    None
    """
    # Create a PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

    # Create a list to hold the content (can include paragraphs, images, etc.)
    content = []

    # Create a style for the content
    style = getSampleStyleSheet()["Normal"]

    # Add the string content to the PDF
    content.append(Paragraph(string_content, style))

    # Build the PDF
    doc.build(content)
    return output_pdf_path
# Example usage
# string_content = "This is a sample string content that will be converted to PDF."
# output_pdf_path = "output.pdf"

def scrap_main(file_path):
    url_list=extract_urls_from_csv(file_path)

    scrap_data=scrape_websites_and_generate_pdf(url_list)
    output_pdf_path=convert_string_to_pdf(scrap_data,"api/services/data_scrap/output.pdf")
    return output_pdf_path