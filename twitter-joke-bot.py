import time
import tweepy

from config import (
    API_KEY,
    API_SECRET_KEY,
    BEARER_TOKEN,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

# Bot screen name
BOT_SCREEN_NAME = 'JokWhySoSerious'

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


# Function to respond to mentions with a joke
def respond_to_mentions(client: tweepy.Client):
    user = client.get_user(username=BOT_SCREEN_NAME)

    mentions = client.get_users_mentions(user.data.id)   # .mentions_timeline(tweet_fields=['entities'], expansions=['author_id'], user_fields=['username'])

    if mentions.data is None:
        return
    
    for mention in reversed(mentions):
        # if mention.in_reply_to_user_id is not None:
        #     continue

        if BOT_SCREEN_NAME in mention.text:
            mention_id = mention.id
            mention_message = mention.text
            tweet_author = mention.author.username
            # keywords = extract_keywords(mention.text)  # Implement your own logic to extract keywords

            joke = "No Joke for you!"
            reply = f"@{tweet_author} Here's a joke for you: {joke}.\n Based on the tweet:\n{mention_message}."
            client.create_tweet(text=reply, in_reply_to_tweet_id=mention_id)
            # if keywords:
            #     joke = generate_joke(keywords)
            #     reply_text = f"@{tweet_author} Here's a joke for you: {joke}"
            #     api.create_tweet(reply_text, in_reply_to_tweet_id=mention_id)
            #     print(f"Replied to mention by @{tweet_author} with a joke.")
            # else:
            #     reply_text = f"@{tweet_author} I couldn't find any keywords in your mention. Please provide some keywords."
            #     api.create_tweet(reply_text, in_reply_to_tweet_id=mention_id)
            #     print(f"Replied to mention by @{tweet_author} requesting keywords.")


# Main loop to continuously listen for mentions
def main():
    """
    An error occurred: 429 Too Many Requests
Too Many Requests
    """
    client = get_client()
    while True:
        try:
            respond_to_mentions(client=client)
        except tweepy.TweepyException as e:
            print(f"An error occurred: {str(e)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Delay between checks (adjust as needed)
        time.sleep(10)

if __name__ == '__main__':
    main()
