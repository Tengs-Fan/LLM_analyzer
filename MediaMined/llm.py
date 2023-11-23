from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from .utils import utils

import os
from dotenv import load_dotenv
load_dotenv()

chatGPT3_16k = ChatOpenAI(
    temperature=0.2, 
    model_name="gpt-3.5-turbo-1106",
    openai_api_key=os.getenv("OPENAI_API_KEY")
    )

chatGPT4_100k = ChatOpenAI(
    temperature=0.2, 
    model_name="gpt-4-1106-preview",
    openai_api_key=os.getenv("OPENAI_API_KEY")
    )


embeddings_model = OpenAIEmbeddings(
    # model_name="text-embedding-ada-002",
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

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
related_post = """2019 Jan 01 17:38
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

reply_related = """{
  "Topics": ["National Security Law", "Privacy", "Freedom"],
  "Attitudes": {
    "Surveillance": {"Relevance": 10, "Sentiment": -6},
    "Privacy": {"Relevance": 10, "Sentiment": -8},
    "Human Rights": {"Relevance": 7, "Sentiment": -6},
    "Democracy": {"Relevance": 4, "Sentiment": -6},
    "Freedom": {"Relevance": 10, "Sentiment": -8},
    "Police": {"Relevance": 1, "Sentiment": -2},
    "Resistance": {"Relevance": 3, "Sentiment": 5},
    "China": {"Relevance": 4, "Sentiment": -6}
  },
  "OtherWords": "Growing unease about personal freedoms and the future of democracy in Hong Kong."
}"""


unrelated_post = """2020 Mar 15 15:05
Upvotes: 926
Title: Exploring Hong Kong's Street Food Scene

Comments
---
2020 Mar 15 16:20
By FoodieHK88
Upvotes: 340 

You have to try the egg waffles in Mong Kok, they're crispy and delicious!
---
2020 Mar 15 15:30
By TravellerJoe
Upvotes: 215 

The fish balls and curry skewers at Temple Street Night Market are a must. So flavorful!
---
2020 Mar 15 17:45
By LocalGourmet
Upvotes: 287 

Don't miss out on the dim sum in Central. The shrimp dumplings are amazing.
---
2020 Mar 15 18:10
By VeggieDelight
Upvotes: 132 

For vegetarians, the tofu stalls in Causeway Bay offer a great variety. The spicy tofu is my favorite.
"""
reply_unrelated = """{
  "Topics": ["Street Food", "Local Cuisine", "Culinary Exploration"],
  "Attitudes": {
    "Surveillance": {"Relevance": 0, "Sentiment": 0},
    "Privacy": {"Relevance": 0, "Sentiment": 0},
    "Human Rights": {"Relevance": 0, "Sentiment": 0},
    "Democracy": {"Relevance": 0, "Sentiment": 0},
    "Freedom": {"Relevance": 0, "Sentiment": 0},
    "Police": {"Relevance": 0, "Sentiment": 0},
    "Resistance": {"Relevance": 0, "Sentiment": 0},
    "China": {"Relevance": 0, "Sentiment": 0}
  },
  "OtherWords": "This post is totally unrelated to surveillance, but centered around Hong Kong's vibrant street food culture and culinary diversity."
}"""

examples = [
    {"input": related_post, "output": reply_related },
    {"input": unrelated_post, "output": reply_unrelated },
]

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# analyze_reddit_post(unrelated_post)
input_prompts = ChatPromptTemplate.from_messages(
    [system_prompt, few_shot_prompt, task_prompt]
)

# Summarize a video dictation
def summarize_video_dictation(dictation, aimed_words):
    task = f"Here is a video dictation, too long, hard to analyze, please summarize it using {aimed_words} words"
    end = "---\nPlease now summarize it !"

    return send_request(True, input_prompts, expert, task, dictation, end)

# Get a analysis of reddit post 
def analyze_reddit_post(post):
    task = "Analyze the topics and sentiments in the Reddit post and comments, the Topic field is about the general theme, the Attitudes is only for the attitudes towards Surveillance, Privacy, Human Rights, Democracy, Freedom, Police, Resistance, China. Relevance is [0, 10], Sentiment is [-10, 10]"
    end = "Provide your analysis in a directly parsible JSON string start with { and end with }, NO triple backticks !"

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

    return responce.content
