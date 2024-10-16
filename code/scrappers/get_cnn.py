import requests
from bs4 import BeautifulSoup
import json

# Function to get article content from a CNN article page
def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # The article content is usually within <div> or <section> tags with specific classes.
        # For CNN, let's focus on <div> with class "l-container" or individual <p> tags for paragraphs.
        paragraphs = soup.find_all('div', class_='article__content-container')

        # Collect and join all paragraphs
        article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])
        return article_text
    else:
        print(f"Failed to retrieve article content from {url}")
        return ""

# Function to scrape CNN headlines and news content

# Function to scrape CNN headlines and news content
def scrape_cnn():
    url = "https://www.cnn.com/election/2024"  # Example: World news section (you can adjust this)

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all divs with 'data-open-link' attribute containing article links
        articles = soup.find_all('div', {'data-open-link': True})

        news_list = []
        for article in articles:
            # Get the headline and link from the 'data-open-link' attribute
            headline = article.find('span', class_='container__headline-text').get_text(strip=True)
            link = article['data-open-link']
            full_link = "https://www.cnn.com" + link if link[0]=='/' else link # Construct full URL
            if '/video/' in full_link:
                continue
            # Get the content of the article
            article_content = get_article_content(full_link)

            # Append the article title, link, and content
            news_list.append({
                'source': 'cnn',
                'title': headline,
                'link': full_link,
                'content': article_content
            })

        return news_list
    else:
        print(f"Failed to retrieve CNN page. Status code: {response.status_code}")
        return []

# Run the CNN scraper
news_data = scrape_cnn()
# Print the scraped news articles along with their content
for idx, news in enumerate(news_data, 1):
    print(f"{idx}. {news['title']}")
    print(f"   Link: {news['link']}")
    print(f"   Content: {news['content'][:300]}...")  # Print the first 300 characters of the content
    print("\n")

# Convert and write JSON object to file
with open("../news/cnn.json", "w") as outfile:
    json.dump(news_data, outfile)