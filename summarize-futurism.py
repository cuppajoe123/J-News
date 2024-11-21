import subprocess
import sys
import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

"""
Headline object is a dictionary with a title element and a link element
"""

def pullHeadlines():
    # Just extract the headline, not the entire HTML element
    url = "https://futurism.com/categories/vr-news"
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('a', class_='block')
#    news_links = [article.find('a', class_='news-link') for article in articles]
    headlines = []
    for article in articles:
        if article.get('title') is not None:
            headlines.append({"title": article.get('title'),
                              "link": "https://futurism.com" + article.get('href')
                              })
    return headlines

def chooseHeadlines(headlines):

    # read in choose_article_prompt file, the first command line argument
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        prompt = file.read()

    titles = []
    for headline in headlines:
        titles.append(headline['title'])

    filtered_links = ''.join(c for c in str(titles) if ord(c) < 128)  # Keeps only ASCII characters

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

# print(pullHeadlines())
# print(chooseHeadlines(pullHeadlines()))

def extractLinks():
    all_headlines = pullHeadlines()
    best_titles = chooseHeadlines(all_headlines)

    urls = []

    for title in best_titles:
        matching_headline = next((headline for headline in all_headlines if headline['title'].strip() == title.strip()), None)

        # Check the result
        if matching_headline:
            urls.append(matching_headline['link'])
        else:
            print("No matching headline found.")
    return urls

# print(extractLinks())
    
def summarizeArticle(url):  
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find_all(class_='post-content')
    filtered_article = ''.join(c for c in str(article) if ord(c) < 128)  # Keeps only ASCII characters

    # Print the content of the div
    # if article:
    #     print(article)
    # else:
    #     print("No div with class 'article-main' found.")

    # read in summary prompt file, second command line argument
    with open(sys.argv[2], 'r', encoding='utf-8') as file:
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

