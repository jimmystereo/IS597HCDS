import requests
from bs4 import BeautifulSoup
import psycopg2
import json
from datetime import datetime
from keys import POSTGRES_PASSWORD, POSTGRES_HOST

# Function to get article content from an ABC News article page
def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # The article content might be within <div> or <section> tags with specific classes.
        paragraphs = soup.find_all('p')

        # Collect and join all paragraphs
        article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])
        return article_text
    else:
        print(f"Failed to retrieve article content from {url}")
        return ""

# Function to scrape ABC News headlines and content
def scrape_abc():
    url = "https://abcnews.go.com/elections"  # The ABC News Elections page

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', class_='ContentRoll__Headline')

        news_list = []
        for article in articles:
            article_inner = article.find('a', class_='AnchorLink')
            headline = article_inner.get_text(strip=True)
            link = article_inner['href']
            if link == '/':
                continue
            full_link = "https://abcnews.go.com" + link if link.startswith('/') else link

            if '/video/' in full_link or '/Video' in full_link or 'playlists' in full_link:
                continue

            article_content = get_article_content(full_link)

            news_list.append({
                'source': 'abcnews',
                'title': headline,
                'link': full_link,
                'content': article_content,
                'collect_date': datetime.now().strftime('%Y-%m-%d')  # Capture the collection date
            })

        return news_list
    else:
        print(f"Failed to retrieve ABC News page. Status code: {response.status_code}")
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

        conn.commit()  # Commit the transaction
        cur.close()
        conn.close()
        print("News data stored successfully in the database.")

    except Exception as e:
        print(f"Failed to store news in the database: {e}")

# Run the ABC News scraper and store the data
news_data = scrape_abc()
store_news_in_db(news_data)

# Convert and write JSON object to file
with open("../news/abcnews.json", "w") as outfile:
    json.dump(news_data, outfile)

print("News data stored successfully in the JSON file.")
