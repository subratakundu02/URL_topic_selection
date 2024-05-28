import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import ssl


# Function to extract article title and text from URL
import requests

# Function to extract article title and text from URL
def extract_article(url):
    try:
        response = requests.get(url, verify=True)  # Set verify=True to enable SSL certificate verification
        response.raise_for_status()  # Raise an error for unsuccessful HTTP responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Modify the selectors below based on the website's structure
        title_element = soup.find('h1')
        article_element = soup.find('div', class_='article-content')
        
        if title_element and article_element:
            title = title_element.get_text(strip=True)
            article = article_element.get_text(separator='\n', strip=True)
            return title, article
        else:
            print(f"Title or article element not found for URL: {url}")
            return None, None
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None, None


# Read the input Excel file
input_file = 'input.xlsx'
df = pd.read_excel(input_file)

# Create a directory to save the extracted articles
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# Loop through each URL, extract content, and save to file
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    title, article = extract_article(url)
    
    if title and article:
        file_path = os.path.join(output_dir, f'{url_id}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n\n{article}")
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to extract content for URL_ID: {url_id}")

print("Extraction completed.")
# Data Cleaning

# Remove HTML tags
cleaned_article = re.sub('<[^<]+?>', '', article)

# Remove special characters
cleaned_article = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_article)

# Convert text to lowercase
cleaned_article = cleaned_article.lower()

# Remove extra whitespaces
cleaned_article = re.sub('\s+', ' ', cleaned_article).strip()

# Save cleaned data to a new Excel file
cleaned_df = df.copy()
cleaned_df['Cleaned_Article'] = cleaned_df['Article'].apply(lambda x: re.sub('<[^<]+?>', '', x))
cleaned_df.to_excel('cleaned_data.xlsx', index=False)

