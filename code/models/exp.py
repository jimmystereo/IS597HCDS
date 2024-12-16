import anthropic
import pandas as pd
from openai import OpenAI
import google.generativeai as genai
import os
import json
from keys import OPENAIKEY, ANTHROPIC_API_KEY
import re
import pandas as pd
news_content = """
Former Illinois Gov. Rod Blagojevich joins 'America's Newsroom' to discuss Chicago residents' frustration at local Democratic officials for prioritizing spending on migrants and President Biden's pardon for his son Hunter.
Former Illinois Gov. Rod Blagojevich, a Democrat whose 14-year corruption sentence was commuted by former President Trump, called out President Biden for lying to the American people about his intentions of pardoning his son, Hunter.
Blagojevich, who was released in 2020 after serving eight years behind bars in Colorado, wasconvicted in his second trialin 2011 on 18 counts, including trying to sell former President Obama’s old Senate seat. His first trial ended with the jury unable to reach a verdict, except for a single conviction, for lying to the FBI.
TRUMP ASKS ABOUT ‘J-6’ HOSTAGES IN RESPONSE TO BIDEN'S PARDON OF HUNTER: ‘SUCH AN ABUSE’
"My case is different from Hunter Biden," Blagojevich told Bill Hemmerduring "America's Newsroom"on Tuesday. "He really committed crimes. I didn't. I was in prison for politics. I wouldn't give in to weaponized prosecutors."
"Joe Biden's a father. I'm a father. I have to think that under the same circumstances, I probably would have done the same thing for my child," he continued. "Having said that, I wouldn't have lied to the American people. Joe Biden knew all along that he was going to do this for his son. How could he not?"
President Biden walks with Hunter Biden toward Marine One on the South Lawn of the White House, July 26, 2024.(AP Photo/Susan Walsh, File)
President Bidenissued a sweeping pardonfor Hunter on Sunday after he had repeatedly said he would not do so.
The first son had been convicted in two separate federal cases earlier this year. He pleaded guilty to federal tax charges in September, and was convicted of three felony gun charges in June after lying on a mandatory gun purchase form by saying he was not illegally using or addicted to drugs.
The presidentargued in a statementthat Hunter was "singled out only because he is my son" and that there was an effort "trying to break Hunter" in order to "break me."
Critics have been quick to call out the White House for reversing course on previous vows against pardoning the first son.
HUNTER BIDEN SAYS HIS MISTAKES WERE ‘EXPLOITED’ FOR POLITICAL SPORT, SAYS HE WON'T TAKE PARDON FOR GRANTED
"Right from the beginning, he lied to the American people, making chumps of the American people," Blagojevich said. "And here [is] just another lie coming from Democratic political leaders who have cynical purposes for political reasons instead of being straight with the American people. So I think it was wrong the way he handled it. It's hard for me to condemn a guy who is looking after his son."
Despite critics' claims the White House lied about Biden's intentions, White House press secretary Karine Jean-Pierre argued the American people werenever fed lieswhile speaking with reporters on the way to Angola.
"One thing the president believes is to always be truthful with the American people," Jeane-Pierre said Monday, repeatedly saying that Biden "wrestled with [the decision]."
She was peppered with questions about the pardon and why Biden decided to go forward with it last weekend, mostly repeating many points in the president's statement from Sunday night, such as Hunter was "singled out politically." She also teased that there could be more pardons on the horizon before Biden leaves office.
"There's a process in place, obviously," she told reporters. "And so, I'm not going to get ahead of the president on this, but you could expect more announcements, more pardons, clemency at the end of this term."
Fox News' Alexander Hall, Stephen Sorace and Brie Stimson contributed to this report.
CLICK TO GET THE FOX NEWS APP
Bailee Hill is an associate editor with Fox News Digital. Story ideas can be sent to bailee.hill@fox.com
"""


## Initilize Models
# GPT
os.environ["OPENAI_API_KEY"] = OPENAIKEY
gpt = OpenAI()

# Claude
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
claude = anthropic.Anthropic()

# Gemini
genai.configure(api_key="AIzaSyA6bk5BRHQJHnjruJC2CpULPJr9tE3wQg0")
gemini = genai.GenerativeModel("gemini-1.5-flash")



def rate(news_content, model, temperature):
    prompt = f"""
    You are an AI trained to evaluate political bias in news articles. 
    
    Please analyze the news content below and give a political bias score based on the content. Do not consider the source or any other context, only the content itself.
    
    1. Explanation: explain the reasoning in bullet points. Be objective, and logical in your explanation.
    
    2. Bias Score: Based on the explanation, provide a score between -2 and 2:
       - -2 = Far-left bias
       - 2 = Far-right bias
       - 0 = Neutral (no bias)
       Please wrap the score between !$*_& sign like this !$*_&score!$*_&
       
    
    Here is the news content:
    \"\"\"{news_content}\"\"\"
    
    **Please evaluate the content and output only the score following the reasons.**
    
    """
    if model == 'claude':
        message = claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=temperature,
            # system="You are an assistant to determine political bias of websites.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return prompt,message.content[0].text
    elif model == 'gpt':

        completion = gpt.chat.completions.create(
            model="gpt-4o",
            messages=[
                # {"role": "system", "content": "You are an assistant to determine political bias of websites."},
                {
                    "role": "user",
                    "content": prompt

                }
            ],
            temperature=temperature,  # Set to 0 for deterministic output
            top_p=1,        # Default value
            n=1
        )
        # compute entropy
        return prompt, completion.choices[0].message.dict()['content']

    elif model == 'gemini':

        response = gemini.generate_content(prompt,
                                          generation_config=genai.types.GenerationConfig(
                                              # Only one candidate for now.
                                              # candidate_count=1,
                                              # stop_sequences=["x"],
                                              # max_output_tokens=20,
                                              temperature=temperature,
                                          ),
                                          )
        return prompt, response.text




def parse_score(result):
    try:
        bias_score = float(result.split('!$*_&')[-2])
        return bias_score
    except:
        return -999

result_df = pd.DataFrame()
# model = 'gemini'
temperature = 0
df = pd.read_csv('exp_dataset.csv', sep = '\t')
df = pd.read_csv('cnn_addon.csv', sep = '\t')
c = 0
for j in range(5):
    for i in range(df.shape[0]):
            for model in ['claude', 'gpt', 'gemini']:
                c+=1
                # if c<= 1372+426+167:
                #     continue
                news_content = df.loc[i,'content']
                prompt, result = rate(news_content, model, temperature)
                print(i, df.shape[0], model)
                bias_score = parse_score(result)
                output_dict = df.loc[i,:].to_dict()
                output_dict['model'] = model
                output_dict['temperature'] = temperature
                output_dict['prompt'] = prompt
                output_dict['result'] = result
                output_dict['score'] = bias_score
                output_df = pd.DataFrame(output_dict, index = [0])
                result_df = pd.concat([result_df, output_df], ignore_index=True)
result_df.to_csv('h1_result_5.csv', encoding = 'utf-8-sig', sep = '\t', index = False)
# result_df.shape
# 1372+426+167+285