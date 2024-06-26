#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
from textblob import TextBlob
import nltk
import re
import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

nltk.download('punkt')

# Define a function to compute text metrics
def compute_text_metrics(article_text):
    if not article_text:
        return {
            'positive_score': 0,
            'negative_score': 0,
            'polarity_score': 0,
            'subjectivity_score': 0,
            'avg_sentence_length': 0,
            'percentage_complex_words': 0,
            'fog_index': 0,
            'avg_words_per_sentence': 0,
            'complex_word_count': 0,
            'word_count': 0,
            'syllables_per_word': 0,
            'personal_pronouns': 0,
            'avg_word_length': 0
        }
    
    blob = TextBlob(article_text)
    sentences = blob.sentences
    words = blob.words
    
    positive_score = sum(1 for sentence in sentences if sentence.sentiment.polarity > 0)
    negative_score = sum(1 for sentence in sentences if sentence.sentiment.polarity < 0)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences) if sentences else 0
    
    # Placeholder for other metrics
    percentage_complex_words = 0
    fog_index = 0
    avg_words_per_sentence = avg_sentence_length
    complex_word_count = 0
    word_count = len(words)
    syllables_per_word = 0
    personal_pronouns = 0
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_words_per_sentence,
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'syllables_per_word': syllables_per_word,
        'personal_pronouns': personal_pronouns,
        'avg_word_length': avg_word_length
    }

# Ensure the output directory exists
output_dir = "C:/Users/Ijaz khan/Downloads/extracted_articles"
os.makedirs(output_dir, exist_ok=True)

def extract_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title and article text
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text().strip()
        else:
            title = "No Title"
        
        paragraphs = soup.find_all('p')
        article_text = "\n".join([p.get_text().strip() for p in paragraphs])
        
        # Sanitize the title for use as a file name
        sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)
        
        return sanitized_title, article_text
    except RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "NO Title", "No Article Text"

# Load the input data
input_file_path = "C:/Users/Ijaz khan/Downloads/Input.xlsx"
input_df = pd.read_excel(input_file_path)

# Prepare output data structure
output_data = []

for index, row in input_df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    title, article_text = extract_article(url)
    
    # Save article text to file
    file_path = os.path.join(output_dir, f"{url_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n{article_text}")
    
    # Compute text metrics
    metrics = compute_text_metrics(article_text)
    
    # Combine input data with computed metrics
    output_row = {**row.to_dict(), **metrics}
    output_data.append(output_row)

# Convert output data to a DataFrame
output_df = pd.DataFrame(output_data)

# Save the DataFrame to an Excel file
output_excel_path = "C:/Users/Ijaz khan/Downloads/Output.xlsx"
output_df.to_excel(output_excel_path, index=False)

print("Output saved to", output_excel_path)


# In[ ]:




