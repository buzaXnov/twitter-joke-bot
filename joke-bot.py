import tweepy
from config import (
    API_KEY,
    API_SECRET_KEY,
    BEARER_TOKEN,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)


def get_client():
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

    return client
        
def get_tweets(client: tweepy.Client, query: str):
    tweets = client.search_recent_tweets(query=query, max_results=10)
    return tweets


if __name__ == "__main__":
    client = get_client()
    tweets = get_tweets(client, "python")
    for tweet in tweets:
        print(tweet)
