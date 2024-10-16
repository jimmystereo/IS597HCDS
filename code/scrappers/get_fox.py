import requests
from bs4 import BeautifulSoup
import json

# Function to get article content from a Fox News article page
def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # The article content is usually within <div> or <section> tags with specific classes.
        # For Fox News, let's focus on <p> tags inside <div> with class "article-body".
        paragraphs = soup.find_all('div', class_='article-body')

        # Collect and join all paragraphs
        article_text = "\n".join([para.get_text(strip=True) for para in paragraphs[0].find_all('p')])
        return article_text
    else:
        print(f"Failed to retrieve article content from {url}")
        return ""

# Function to scrape Fox News headlines and news content
def scrape_fox_news():
    url = "https://www.foxnews.com/politics"  # Politics section of Fox News

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all article elements with links and headlines
        articles = soup.find_all('article', {'class': 'article'})

        news_list = []
        for article in articles:
            # Get the headline and link from the <a> tag within the article
            headline_tag = article.find(attrs={'class': 'title'}, recursive=True)
            if headline_tag:
                headline = headline_tag.get_text(strip=True)
                link_tag = article.find('a', href=True)
                if link_tag:
                    link = link_tag['href']
                    if '/video/' in link:
                        continue
                    full_link = "https://www.foxnews.com" + link if link[0] == '/' else link
                    # Get the content of the article
                    article_content = get_article_content(full_link)
                    # Append the article title, link, and content
                    news_list.append({
                        'source': 'foxnews',
                        'title': headline,
                        'link': full_link,
                        'content': article_content
                    })

        return news_list
    else:
        print(f"Failed to retrieve Fox News page. Status code: {response.status_code}")
        return []

# Run the Fox News scraper
news_data = scrape_fox_news()

# Print the scraped news articles along with their content
for idx, news in enumerate(news_data, 1):
    print(f"{idx}. {news['title']}")
    print(f"   Link: {news['link']}")
    print(f"   Content: {news['content'][:300]}...")  # Print the first 300 characters of the content
    print("\n")

# Convert and write JSON object to file
with open("../news/foxnews.json", "w") as outfile:
    json.dump(news_data, outfile)
