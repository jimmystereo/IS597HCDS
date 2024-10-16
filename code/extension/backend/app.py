from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import anthropic
import os
import json
from keys import OPENAIKEY, ANTHROPIC_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAIKEY
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
class Rater:
    def __init__(self):
        self.rate = None
    def rate(self):
        pass
    def set_rater(self, name):
        if name == 'gpt':
            self.rate = self.rate_gpt

        elif name == 'claude':
            self.rate = self.rate_claude
    def rate_gpt(self, news_content):
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant to determine political bias of websites."},
                {
                    "role": "user",
                    "content": "carefully evaluate that whether this content political is biased?"
                               "Don't consider the source of the news. pretend you don't know about it."
                               "output -2~2 from far left to far right political biased, 0 for non-biased"
                               "Please output in this format, strictly:"
                               "Score: score"
                               "Reasons: (in short bullet point)"
                               f"""{news_content}"""
                }
            ],
            temperature=0,  # Set to 0 for deterministic output
            top_p=1,        # Default value
            n=1
        )
        # compute entropy
        return completion.choices[0].message.dict()['content']
    def rate_claude(self, news_content):
        client = anthropic.Anthropic()

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            system="You are an assistant to determine political bias of websites.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "carefully evaluate that whether this content political is biased?"
                                    "Don't consider the source of the news. pretend you don't know about it."
                                    "output -2~2 from far left to far right political biased, 0 for non-biased"
                                    "Please output in this format, strictly:"
                                    "Score: score"
                                    "Reasons: (in short bullet point)"
                                    f"""{news_content}"""
                        }
                    ]
                }
            ]
        )
        return message.content[0].text


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/scrape', methods=['POST'])
def scrape_page():
    data = request.get_json()  # Get the JSON data from the request
    url = data.get('url')  # Extract the URL from the JSON
    model = data.get('model')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # The article content is usually within <div> or <section> tags with specific classes.
        # For CNN, let's focus on <div> with class "l-container" or individual <p> tags for paragraphs.
        paragraphs = soup.find_all('div', class_='article__content-container')

        # Collect and join all paragraphs
        article_text = "\n".join([para.get_text(strip=True) for para in paragraphs])
        rater = Rater()
        rater.set_rater(model)
        result = rater.rate(article_text)
        score = result.split('\n')[0].replace('*','').split(' ')[-1]
        print(result)
        return jsonify({
            'result': result,
            'score': score
        })

    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
