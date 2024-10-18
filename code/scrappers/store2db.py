import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from keys import POSTGRES_PASSWORD, POSTGRES_HOST

# Define the database connection string
DATABASE_URL = f"postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/postgres"

# Define the base class for declarative models
Base = declarative_base()

# Define the News model
class News(Base):
    __tablename__ = 'news'
    link = Column(String, primary_key=True)
    title = Column(String)
    content = Column(String)
    source = Column(String)
    collectdate = Column(DateTime)

# Function to store the news data into the PostgreSQL database
def store_news_in_db(news_list):
    try:
        # Create a database engine
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)  # Create the table if it doesn't exist
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insert each news article into the News table
        for news in news_list:
            existing_article = session.query(News).filter_by(link=news['link']).first()
            if existing_article is None:
                article = News(
                    link=news['link'],
                    title=news['title'],
                    content=news['content'],
                    source=news['source'],
                    collectdate=datetime.now().strftime('%Y-%m-%d')
                )
                session.add(article)

        session.commit()  # Commit the transaction
        session.close()  # Close the session
        print("News data stored successfully in the database.")

    except Exception as e:
        print(f"Failed to store news in the database: {e}")

# Main execution block
if __name__ == "__main__":
    with open('../news/cnn.json', 'r') as f:
        news_data = json.load(f)
    store_news_in_db(news_data)

    print("News data stored successfully in the JSON file.")
