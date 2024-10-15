import requests
from bs4 import BeautifulSoup
import json

# Function to get article content from an ABC News article page
def get_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # The article content might be within <div> or <section> tags with specific classes.
        # For ABC News, you may need to adjust the tag and class based on the HTML structure.
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

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all headlines. Adjust the tag and class to match the site's structure
        articles = soup.find_all('div', class_='ContentRoll__Headline')

        news_list = []
        for article in articles:
            # Get the headline text and link
            article_inner = article.find('a', class_='AnchorLink')
            headline = article_inner.get_text(strip=True)
            link = article_inner['href']
            if link == '/':
                continue
            full_link = "https://abcnews.go.com" + link if link.startswith('/') else link  # Construct full URL

            # Skip video or other non-article links if necessary
            if '/video/' in full_link or '/Video' in full_link or 'playlists' in full_link:
                continue

            # Get the content of the article
            article_content = get_article_content(full_link)

            # Append the article title, link, and content
            news_list.append({
                'title': headline,
                'link': full_link,
                'content': article_content
            })

        return news_list
    else:
        print(f"Failed to retrieve ABC News page. Status code: {response.status_code}")
        return []

# Run the ABC News scraper
news_data = scrape_abc()

# Print the scraped news articles along with their content
for idx, news in enumerate(news_data, 1):
    print(f"{idx}. {news['title']}")
    print(f"   Link: {news['link']}")
    print(f"   Content: {news['content'][:300]}...")  # Print the first 300 characters of the content
    print("\n")

# Convert and write JSON object to file
with open("../news/abcnews.json", "w") as outfile:
    json.dump(news_data, outfile)
