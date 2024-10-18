import requests
from bs4 import BeautifulSoup
import psycopg2
import json
from datetime import datetime
from keys import POSTGRES_PASSWORD, POSTGRES_HOST
# Function to get article content from a Fox News article page
def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # For Fox News, let's focus on <p> tags inside <div> with class "article-body".
        paragraphs = soup.find_all('div', class_='article-body')

        if paragraphs:
            article_text = "\n".join([para.get_text(strip=True) for para in paragraphs[0].find_all('p')])
            return article_text
        else:
            return ""
    else:
        print(f"Failed to retrieve article content from {url}")
        return ""

# Function to scrape Fox News headlines and news content
def scrape_fox_news():
    url = "https://www.foxnews.com/politics"  # Politics section of Fox News

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
                        'content': article_content,
                        'collect_date': datetime.now().strftime('%Y-%m-%d')  # Capture collection date
                    })

        return news_list
    else:
        print(f"Failed to retrieve Fox News page. Status code: {response.status_code}")
        return []

# Function to store the news data into the PostgreSQL database
def store_news_in_db(news_list):
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",  # Replace with your DB name
            user="postgres",      # Replace with your DB user
            password=POSTGRES_PASSWORD,  # Replace with your DB password
            host=POSTGRES_HOST,      # Replace with your DB host (e.g., localhost or IP)
            port="5432"            # Replace with your DB port (default is 5432)
        )
        cur = conn.cursor()

        # Insert each news article into the News table
        for news in news_list:
            cur.execute("""
                INSERT INTO News (Link, Title, Content, Source, CollectDate)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (Link) DO NOTHING;
            """, (news['link'], news['title'], news['content'], news['source'], news['collect_date']))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()
        print("News data stored successfully in the database.")

    except Exception as e:
        print(f"Failed to store news in the database: {e}")

# Run the Fox News scraper and store the data
news_data = scrape_fox_news()
store_news_in_db(news_data)

# Keep the part that stores the data in JSON
# Convert and write JSON object to file
with open("../news/foxnews.json", "w") as outfile:
    json.dump(news_data, outfile)

print("News data stored successfully in the JSON file.")
