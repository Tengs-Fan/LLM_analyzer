from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate
from .utils import utils

import os
from dotenv import load_dotenv
load_dotenv()

chatGPT3_16k = ChatOpenAI(
    temperature=0.4, 
    model_name="gpt-3.5-turbo-1106",
    openai_api_key=os.getenv("OPENAI_API_KEY")
    )

chatGPT4_100k = ChatOpenAI(
    temperature=0.3, 
    model_name="gpt-4-1106-preview",
    openai_api_key=os.getenv("OPENAI_API_KEY")
    )


expert = "Assume you are an expert of Human Right and Hong Kong, You will analyze online discussions related to state surveillance in Hong Kong. You should answer in JSON format"

system_template = ("{system}")
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

task_template = (
"""{task}
{start}
{end}
""")
task_prompt = HumanMessagePromptTemplate.from_template(task_template)

related_post = """
2019 Jan 01 17:38
Upvotes: 1034
Title: Impact of National Security Law on Hong Kong's Freedom

I'm increasingly concerned about the state surveillance in Hong Kong under the new National Security Law. It feels like our freedoms are being stripped away. What are your thoughts?

2019 Jan 01 20:12
By Marcus123
Upvotes: 534 

It's alarming to see how quickly our rights are being eroded.
---
2019 Jan 02 10:56
By 香港榮光
Upvotes: 345 

This is just the beginning. More oppressive measures might be on the way.
---
2019 Jan 01 17:38
By Nichchk
Upvotes: 275 

I think the law is necessary for national security, but I'm worried about privacy.
"""

reply_related = (
""" {
  "Topic": ["National Security Law", "Privacy", "Human Rights", "Protest"],
  "Attitudes": [
    {
      "Topic": "Surveillance",
      "Relevance": 10,
      "Sentiment": -7,
    },
    {
      "Topic": "Security Law",
      "Relevance": 10,
      "Sentiment": -8,
    },
    {
      "Topic": "Police",
      "Relevance": 9,
      "Sentiment": -9,
    },
    {
      "Topic": "Resistance",
      "Relevance": 8,
      "Sentiment": 5,
    },
    {
      "Topic": "Immigration",
      "Relevance": 6,
      "Sentiment": -3,
    }
  ],
  "OtherWords": "The general tone in discussions indicates a growing unease about personal freedoms and the future of democracy in Hong Kong."
}""")
# example_prompt = AIMessagePromptTemplate.from_template(example_template)


unrelated_post = """2019 Oct 09 07:38
Upvotes: 1034
Title: Best Hiking Trails in Hong Kong
    
Comments
---
2019 Oct 09 10:12
By frauenarzZzt
Upvotes: 123 

Dragon's Back is a must-try, offers amazing views!
---
2019 Oct 09 07:40
By Nichchk
Upvotes: 75 

Lion Rock has a challenging path but it's totally worth it.
---
2019 Oct 09 11:08
By Dr_Rockso89
Upvotes: 1534 

Don't forget to check out the MacLehose Trail, it's fantastic."""
reply_unrelated = """{
  "Topic": [Hiking", "Outdoor Activities"],
  "Ralted": false
  "OtherWords": "This one is totally unrelated"
}"""

# analyze_reddit_post(unrelated_post)
input_prompts = ChatPromptTemplate.from_messages(
    [system_prompt, task_prompt]
)

# Summarize a video dictation
def summarize_video_dictation(dictation, aimed_words):
    task = f"Here is a video dictation, too long, hard to analyze, please summarize it using {aimed_words} words"
    end = "---\nPlease now summarize it !"

    return send_request(True, input_prompts, expert, task, dictation, end)

# Get a analysis of reddit post 
def analyze_reddit_post(post):
    task = "Analyze the sentiment and themes in the provided Reddit post and comments related to state surveillance in Hong Kong."
    end = "Provide your analysis in JSON format."

    return send_request(False, input_prompts, expert, task, post, end)

def send_request(use_100k, prompt, system, task, start, end):
    send_prompt = prompt.format_prompt(
            system = system,
            task = task,
            start = start,
            end = end
            )

    token_num = utils.count_tokens(prompt.format(system = system, task = task, start = start, end = end))
    if (token_num < 16385):
        responce = chatGPT3_16k(send_prompt.to_messages())
    elif (token_num < 128000) and use_100k:
        print("We are using 128K ChatGPT-4 model")
        responce = chatGPT4_100k(send_prompt.to_messages())
    else: 
        raise Exception("There is more than 16K tokens: ", token_num)

    print(responce.content)
