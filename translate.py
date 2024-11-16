import subprocess
import sys
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

def pullHeadlines():
    url = "https://phys.org/chemistry-news/"
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='sorted-article')
    news_links = [article.find('a', class_='news-link') for article in articles]
    for link in news_links:
        print(link)
        print("\n")

url = "https://phys.org/news/2024-11-simple-table-salt-adhesive-polymer.html"
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
response = requests.get(url, headers=headers)
html = response.text
# print(html)

soup = BeautifulSoup(html, 'html.parser')

article = soup.find('div', class_='article-main')
filtered_article = ''.join(c for c in str(article) if ord(c) < 128)  # Keeps only ASCII characters

# Print the content of the div
# if article:
#     print(article)
# else:
#     print("No div with class 'article-main' found.")

# read in prompt file
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    prompt = file.read()

# Send to OpenAI, not the most expensive model!
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt + filtered_article
        }
    ]
)

news = completion.choices[0].message.content

print(news)
