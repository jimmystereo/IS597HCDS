from openai import OpenAI
import anthropic
import os
import json
from keys import OPENAIKEY, ANTHROPIC_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAIKEY
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.chdir("./models")
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
                    "content":
                        f"""
You are an AI trained to evaluate political bias in news articles. 

Please analyze the news content below and give a political bias score based on the content. Do **NOT** consider the source or any other context, only the content itself.

1. **Bias Score**: Provide a score between -2 and 2:
   - -2 = Far-left bias
   - 2 = Far-right bias
   - 0 = Neutral (no bias)
   
2. **Explanation**: After the score, explain the reasoning in bullet points. Be **brief**, **objective**, and **logical** in your explanation.

Here is the news content:
\"\"\"{news_content}\"\"\"

**Please evaluate the content and output only the score and reasons. Do not repeat the input text.**

"""
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

def rate_all(model_name, data):
    rater = Rater()
    rater.set_rater(model_name)
    rated_result = []
    for news in data:
        if news['content'] == '':
            continue
        print(news['title'])
        news['result'] = rater.rate(news['content'])
        news['score'] = news['result'].split('\n')[0].replace('*','').split(' ')[-1]

        news['model'] = model_name
        rated_result.append(news)
    return rated_result

with open('../news/cnn.json', 'r') as f:
    cnn = json.load(f)
with open('../news/foxnews.json', 'r') as f:
    fox = json.load(f)
with open('../news/abcnews.json', 'r') as f:
    abc = json.load(f)
cnn_rated = rate_all('gpt', cnn) + rate_all('claude', cnn)
abc_rated = rate_all('gpt', abc) + rate_all('claude', abc)
fox_rated = rate_all('gpt', fox) + rate_all('claude', fox)

import pandas as pd
import datetime
cnn_rated_df = pd.DataFrame(cnn_rated)
abc_rated_df = pd.DataFrame(abc_rated)
fox_rated_df = pd.DataFrame(fox_rated)
combined_df = pd.concat([cnn_rated_df, abc_rated_df, fox_rated_df], ignore_index=True)
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
combined_df.to_csv(f'../rated/{today_date}.csv', index=False, encoding = 'utf-8-sig')

import matplotlib.pyplot as plt
import re
def plot_dist(source, title):
    scores = []
    for news in source:
        score = news['result'].split('\n')[0].replace('*','').split(' ')[-1]
        try:
            scores.append(float(score.replace('$', '')))
        except ValueError:
            print(news['result'])
    plt.hist(scores)
    plt.title(title)
    plt.show()

plot_dist(fox_rated, 'fox')
plot_dist(cnn_rated, 'cnn')
plot_dist(abc_rated, 'abc')

plt.hist()
