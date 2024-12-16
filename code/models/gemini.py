import google.generativeai as genai


genai.configure(api_key="AIzaSyA6bk5BRHQJHnjruJC2CpULPJr9tE3wQg0")
model = genai.GenerativeModel("gemini-1.5-flash")

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
prompt = f"""
You are an AI trained to evaluate political bias in news articles. 

Please analyze the news content below and give a political bias score based on the content. Do **NOT** consider the source or any other context, only the content itself.

1. **Explanation**: explain the reasoning in bullet points. Be **brief**, **objective**, and **logical** in your explanation.

1. **Bias Score**: Based on the explanation, provide a score between -2 and 2:
   - -2 = Far-left bias
   - 2 = Far-right bias
   - 0 = Neutral (no bias)
   

Here is the news content:
\"\"\"{news_content}\"\"\"

**Please evaluate the content and output only the reasons and score. Do not repeat the input text.**

"""

response = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
    # Only one candidate for now.
    # candidate_count=1,
    # stop_sequences=["x"],
    # max_output_tokens=20,
    temperature=0,
),
)
print(response.text)