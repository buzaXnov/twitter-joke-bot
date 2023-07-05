import tweepy
from config import (
    API_KEY,
    API_SECRET_KEY,
    BEARER_TOKEN,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

BOT_SCREEN_NAME = "JokWhySoSerious"

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
    # tweets = get_tweets(client, "python")
    user = client.get_user(username=BOT_SCREEN_NAME)
    mentions = client.get_users_mentions(user.data.id)  # NOTE: Projveri ima li since_id argument ovdje i kako ga iskoristiti!!!???
    # if type(mentions) == dict:
    if mentions.data is not None:
        print(mentions)
        for mention in mentions.data:
            try:
                print(mention.text)
                client.create_tweet(text=f"This is a joke reply to your mention.\nYou tweeted:\n{mention.text}", in_reply_to_tweet_id=mention.id)
            except Exception as e:
                print(e)

            # VIDEO: https://www.youtube.com/watch?v=6FLeguySZLc

    else:
        # If no mentions are found, the type is tweepy.Client.Response
        print(type(mentions))
        print("No mentions.")
    # for tweet in tweets:
    #     print(tweet)


# QUESTIONS:
# NOTE: Should my bot reply to tweets? 
# NOTE: Should I have a list or sht of the mentiones that I have answered to since the get_users_mentions() method returns the last 10 mentions by minimum up to 800 max???
# NOTE: Should my bot reply to direct messages? 
# NOTE: How do I counter the open rate limit of 300 requests per 15 minutes and the charging???? Check out the correct numbers.

# NOTE: This is the output of running this code.
"""
Response(data=[<Tweet id=1676705115653173248 text='@JokWhySoSerious And another one.'>, <Tweet id=1676704553121505280 text='@JokWhySoSerious This is a test joke tweet.'>], includes={}, errors=[], meta={'result_count': 2, 'newest_id': '1676705115653173248', 'oldest_id': '1676704553121505280'})
@JokWhySoSerious And another one.
@JokWhySoSerious This is a test joke tweet.
"""

# NOTE: When I ran it again on accident and DID NOT change the code in any way:
"""
Response(data=[<Tweet id=1676705199405056001 text='@FButic This is a joke reply to your mention.\nYou tweeted:\n@JokWhySoSerious This is a test joke tweet.'>, <Tweet id=1676705198339682304 text='@FButic This is a joke reply to your mention.\nYou tweeted:\n@JokWhySoSerious And another one.'>, <Tweet id=1676705115653173248 text='@JokWhySoSerious And another one.'>, <Tweet id=1676704553121505280 text='@JokWhySoSerious This is a test joke tweet.'>], includes={}, errors=[], meta={'result_count': 4, 'newest_id': '1676705199405056001', 'oldest_id': '1676704553121505280'})
@FButic This is a joke reply to your mention.
You tweeted:
@JokWhySoSerious This is a test joke tweet.
@FButic This is a joke reply to your mention.
You tweeted:
@JokWhySoSerious And another one.
@JokWhySoSerious And another one.
403 Forbidden
You are not allowed to create a Tweet with duplicate content.
@JokWhySoSerious This is a test joke tweet.
403 Forbidden
You are not allowed to create a Tweet with duplicate content.
"""
# NOTE: Use this if you can! Or just ask someone....