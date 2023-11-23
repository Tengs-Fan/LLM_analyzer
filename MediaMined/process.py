from .compose import *
from .llm import *
from multiprocessing import Pool
import json
from pymongo import MongoClient
from datetime import datetime, timedelta

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import os

DATA_DIR = "DataFrame"

client = MongoClient('localhost', 27017)
reddit = client['reddit']
posts = reddit['posts']
selected_post = reddit['selected_posts']
selected_post1 = reddit['selected_posts1']

time_2010_1_1 = datetime(2010, 1, 1)
time_2023_04_01 = datetime(2023, 4, 1)

def update_utc_to_int(collection):
    # Find records where 'created_utc' is stored as a string
    string_utc_records = collection.find({
        'created_utc': {'$type': 'string'}
    })

    # Update each record to store 'created_utc' as an integer
    for record in string_utc_records:
        updated_utc = int(record['created_utc'])
        collection.update_one({'_id': record['_id']}, {'$set': {'created_utc': updated_utc}})
        
def stratified_sample(number_of_month):

    # if number_of_month < 100:
    #     number_selected = number_of_month
    # elif number_of_month < 1000:
    #     number_selected = 100 + (number_of_month - 100) * 0.11
    # else:
    #     number_selected = 1000 + (number_of_month - 1000) * 0.05        
    if number_of_month < 100:
        number_selected = number_of_month * 0.1
    elif number_of_month < 1000:
        number_selected = 10 + (number_of_month - 100) * 0.01
    else:
        number_selected = 100 + (number_of_month - 1000) * 0.005        

    return int(number_selected)

def each_month(collection, start_date, sort_on):
    # Calculate the start and end dates for the current month
    start_of_month = start_date.replace(day=1)
    end_of_month = (start_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Query the database for records within the current month's timeframe
    records = collection.find({
        'created_utc': {
            '$gte': int(start_of_month.timestamp()),
            '$lte': int(end_of_month.timestamp())
        }
    })

    # Sort the records by 'score' in descending order
    sorted_records = sorted(records, key=lambda x: x[sort_on], reverse=True)

    # Calculate the number of records to select for this month
    num_records_to_select = stratified_sample(len(sorted_records))
    selected_records = sorted_records[:num_records_to_select]

    next_month = start_date.replace(day=1) + timedelta(days=32)

    return selected_records, next_month, num_records_to_select

def number_plot():

    # Dump to CSV
    output_filename = 'date_number_of_post.pkl'  # You can change the file name as needed
    output_filepath = os.path.join(DATA_DIR, output_filename)

    if os.path.exists(output_filepath):
        df = pd.read_pickle(output_filepath)
    else:
        dates = []
        values = []
        current = time_2010_1_1
        dates.append(current)
        while current < time_2023_04_01:
            record, current, num = each_month(posts, current , 'score')
            dates.append(current)
            values.append(num)
        dates.pop()
        # Create a DataFrame
        df = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        df.to_pickle(output_filepath)

    # Plotting
    plt.figure(figsize=(12, 10))
    plt.plot(df['Date'], df['Value'], marker='o', color='royalblue', linestyle='-', linewidth=2, markersize=6)

    # Improve date formatting on x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.gcf().autofmt_xdate()

    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.title('Change of Values Over Time', fontsize=16)

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def convert_dataframe(collection):

    output_filename = 'all_selected_post.pkl'  # You can change the file name as needed
    output_filepath = os.path.join(DATA_DIR, output_filename)

    if os.path.exists(output_filepath):
        df = pd.read_pickle(output_filepath)
    else:
        # Query the collection and aggregate the data
        data = list(collection.find({}))
        df = pd.DataFrame(pd.json_normalize(data))
        df.to_pickle(output_filepath)

    print(df.head())

def process_post(text):
    client = MongoClient('localhost', 27017)
    reddit = client['reddit']
    comments = reddit['comments']
    selected_posts = reddit['selected_posts1']
    if not mongo._test_exist_in_collection(selected_posts, '_id', text['id']):
        try:
            composed_text = compose_reddit_post(posts, comments, "id", text['id'])
            reply = analyze_reddit_post(composed_text)
            try: 
                parsed_data = json.loads(reply)
                attitudes_data = parsed_data.get('Attitudes', {})
                formatted_attitudes = {key: {'Relevance': value.get('Relevance', 0),
                                             'Sentiment': value.get('Sentiment', 0)}
                                       for key, value in attitudes_data.items()}
            except Exception as e:
                print(reply)
                raise Exception(f"the returned JSON is invalid: {e}")
            post = {
                '_id': text['id'],
                'subreddit': text['subreddit'],
                'created_utc': int(text['created_utc']),
                'published_at': utils.utc_to_short_format(int(text['created_utc'])),
                'score': int(text['score']),
                'Topics': parsed_data.get('Topics', []),
                'Attitudes': formatted_attitudes,
                'OtherWords': parsed_data.get('OtherWords', '')
            }
            # selected_posts.insert_one(post)
            print(f"Completed analysis of {text['id']}")
        except Exception as e:
            print(f"Error composing {text['id']}: {e}")
    else: 
        print(f"{text['id']} is already inside")

if __name__ == '__main__':
    import sys
    processes = int(sys.argv[1])
    
    current = datetime(2010, 1, 1)
    while current < datetime(2023, 4, 1):
        records, current, num = each_month(posts, current , 'score')
        print(f"processing {num} post in {current}")
        # Create a pool of workers to process posts in parallel
        with Pool(processes=processes) as pool:  # Adjust the number of processes as needed
            pool.map(process_post, records)
