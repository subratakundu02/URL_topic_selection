import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import syllables
import time

# global set variable to store all stop words
all_stop_words = set()
# positive and negative word dictionaries
positive_words = dict()
negative_words = dict()

# Function to extract article title and text from URL
def extract_article(url, url_id):
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url} with status code: {response.status_code}")
        return None, None
    
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

# Function to perform text analysis
def text_analysis(text):
    word_list = re.findall(r'\w+', text.lower())
    syllable_count = sum(syllables.estimate(w) for w in word_list)
    
    # You can implement other analyses such as positive/negative score, polarity score, etc. here.
    # This is just a placeholder for demonstration.
    analysis = {
        'WORD_COUNT': len(word_list),
        'SYLLABLE_PER_WORD': syllable_count / len(word_list) if len(word_list) > 0 else 0,
    }
    
    return analysis

# Read the input Excel file
input_file = 'input.xlsx'
df = pd.read_excel(input_file)

# Create a directory to save the extracted articles
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# Loop through each URL, extract content, save to file, and perform analysis
results = []
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    title, article = extract_article(url, url_id)
    
    if title and article:
        file_path = os.path.join(output_dir, f'{url_id}.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n\n{article}")
        print(f"Saved: {file_path}")
        
        # Perform text analysis and collect results
        analysis_results = text_analysis(article)
        analysis_results['URL_ID'] = url_id
        results.append(analysis_results)
    else:
        print(f"Failed to extract content for URL_ID: {url_id}")

# Save analysis results to a new Excel file
output_analysis_file = 'output_analysis.xlsx'
analysis_df = pd.DataFrame(results)
analysis_df.to_excel(output_analysis_file, index=False)

print("Extraction and analysis completed.")
