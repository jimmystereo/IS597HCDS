from openai import OpenAI
import os
import json
from keys import OPENAIKEY
os.environ["OPENAI_API_KEY"] = OPENAIKEY
client = OpenAI()
def rate(news_content):
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


with open('../news/cnn.json', 'r') as f:
    cnn = json.load(f)


rated_cnn = []
for news in cnn:
    if news['content'] == '':
        continue
    print(news['title'])
    news['result'] = rate(news['content'])
    rated_cnn.append(news)

# https://www.cnn.com/politics/election-2024-key-dates-dg/index.html
print(rated_cnn[2]['title'])
print(rated_cnn[-1]['result'])
print(rated_cnn[2]['content'])


with open('../news/foxnews.json', 'r') as f:
    fox = json.load(f)
rated_fox = []
for news in fox:
    if news['content'] == '':
        continue
    print(news['title'])
    news['result'] = rate(news['content'])
    rated_fox.append(news)
print(rated_fox[0]['title'])
print(rated_fox[0]['result'])
print(rated_fox[0]['content'])


with open('../news/abcnews.json', 'r') as f:
    abc = json.load(f)
rated_abc = []
for news in abc:
    if news['content'] == '':
        continue
    print(news['title'])
    news['result'] = rate(news['content'])
    rated_abc.append(news)
print(rated_abc[0]['title'])
print(rated_abc[0]['result'])
print(rated_abc[0]['content'])

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

plot_dist(rated_fox, 'fox')
plot_dist(rated_cnn, 'cnn')
plot_dist(rated_abc, 'abc')

len(rated_cnn)


