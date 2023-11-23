from .compose import *
from .llm import *

from pymongo import MongoClient

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_DIR = "DataFrame"

client = MongoClient('localhost', 27017)
reddit = client['reddit']
posts = reddit['posts']
selected_posts = reddit['selected_posts']
selected_posts1 = reddit['selected_posts1']

def convert_dataframe(collection):

    output_filename = 'all_selected_posts.pkl'  # You can change the file name as needed
    output_filepath = os.path.join(DATA_DIR, output_filename)

    if os.path.exists(output_filepath):
        df = pd.read_pickle(output_filepath)
    else:
        # Query the collection and aggregate the data
        data = list(collection.find({}))
        df = pd.DataFrame(pd.json_normalize(data))

        # Convert 'created_utc' to a DateTime format
        df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
        # Set time interval for analysis, e.g., 'M' for monthly
        df['Month'] = df['created_utc'].dt.to_period('M')

        df.to_pickle(output_filepath)

    # print(df.iloc[0])
    return df

def get_topics(dataframe):
    # Flatten the list of topics
    all_topics = sum(dataframe['Topics'].tolist(), [])
    unique_topics = set(all_topics)

    from collections import Counter
    # Count the frequency of each topic
    topic_counts = Counter(all_topics)

    # Identify the top 10 topics
    top_10_topics = topic_counts.most_common(20)

    # Display the count of these top 10 topics
    top_10_df = pd.DataFrame(top_10_topics, columns=['Topic', 'Count'])

    return all_topics, unique_topics

def categorize_topics(unique_topics): 
    # Assuming `unique_topics` is a list of your unique topics
    embeddings = embeddings_model.embed_documents(unique_topics)

    from sklearn.cluster import KMeans
    # Clustering
    n_clusters = 10  # You can choose a different number
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(embeddings)

    # Map topics to clusters
    topic_to_category = {topic: cluster for topic, cluster in zip(unique_topics, kmeans.labels_)}

    return topic_to_category

if __name__ == '__main__':
    df = convert_dataframe(selected_posts1)
    _, unique_topics = get_topics(df)
    topic_to_category = categorize_topics(unique_topics)

    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv("OPENAI_API_KEY"))

    # # Choose a category to focus on
    # category_id = 0

    # # Find topics in the chosen category
    # topics_in_category = [topic for topic, category in topic_to_category.items() if category == category_id]

    # # Print the topics in the chosen category
    # print(f"Topics in Category {category_id}:")
    # for topic in topics_in_category:
    #     print(topic)
