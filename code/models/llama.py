import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login

# Log in with your Hugging Face API key
login("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")

# Load LLaMA model and tokenizer
model_name = "meta-llama/Llama-3.2-1B"  # Change based on the model you're using
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Example news content
news_content = """
Stein tells “This Week” that Harris was hindered by a “tough national mood.”
After prevailing in a state that went for Republican Donald Trump, Democratic Gov.-elect Josh Stein said that his service as North Carolina's attorney general gave voters confidence and called the Tar Heel state a "bright spot" for Democrats on election night.
Stein told ABC's "This Week" co-anchor Jonathan Karl that Kamala Harris ran a "strong campaign," but was hindered by a condensed timeline and "tough national mood."
"""
input_text = f"""
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

# Tokenize the input
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(inputs['input_ids'], max_length=1000, num_beams=5, early_stopping=True)

# Decode the generated output
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Output the result
print(decoded_output)
