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


expert = "Assume you are an expert of Human Right and Hong Kong, You will analyze online discussions related to state surveillance in Hong Kong."

system_template = ("{system}")
system_prompt = SystemMessagePromptTemplate.from_template(system_template)

task_template = (
"""{task}
{start}
{end}
""")
task_prompt = HumanMessagePromptTemplate.from_template(task_template)

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
    task = "example task"
    end = "please give your analysis"

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
