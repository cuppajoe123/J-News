import subprocess
import sys
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

def pullHeadlines():
    url = "https://phys.org/biology-news/"
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='sorted-article')
    news_links = [article.find('a', class_='news-link') for article in articles]
    return news_links

def chooseHeadlines(links):

    # read in choose_article_prompt file, the second command line argument
    with open(sys.argv[2], 'r', encoding='utf-8') as file:
        prompt = file.read()

    filtered_links = ''.join(c for c in str(links) if ord(c) < 128)  # Keeps only ASCII characters    

    # Send to OpenAI, not the most expensive model!
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
            "role": "user",
                "content": prompt + '\n' + filtered_links
            }
        ]
    )
    
    return completion.choices[0].message.content.splitlines()

def extractLinks():
    all_headlines = pullHeadlines()
    best_headlines = chooseHeadlines(all_headlines)

    urls = []

    for headline in best_headlines:
        matching_a = next((a for a in all_headlines if a.get_text(strip=True) == headline.strip()), None)

        # Check the result
        if matching_a:
            urls.append(matching_a.get('href'))
        else:
            print("No matching <a> tag found.")
    return urls
    
def summarizeArticle(url):  
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

    # read in summary prompt file
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


urls = extractLinks()

for url in urls:
    summarizeArticle(url)
    print("\n")
