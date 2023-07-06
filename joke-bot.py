import time
import tweepy
import json
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


def main(client: tweepy.Client, bot_id: int):

    try:
        # Load the last id of the last mention that the bot replied to
        with open("last_id.json", "r") as file:
            last_id = json.load(file)["last_id"]

        while True:

            # NOTE: Projveri ima li since_id argument ovdje i kako ga iskoristiti!!!???
            mentions = client.get_users_mentions(id=bot_id, since_id=last_id)

            if mentions.data is not None:
                mention_ids = [mention.id for mention in mentions.data]
                last_id = mention_ids[0]

                # Save the last id to a file so that we can use it later if the bot crashes
                with open("last_id.json", "w") as file:
                    json.dump({'last_id': last_id}, file)

                # NOTE: The mentions are reversed so that the bot replies to the oldest mention first
                for mention in reversed(mentions.data):

                    try:
                        # print(mention.text)
                        # print(f"Meniton ID: {mention.id}\n\n")
                        client.create_tweet(
                            text=f"This is a joke reply to your mention.", in_reply_to_tweet_id=mention.id)
                    except Exception as e:
                        print(e)

                    # VIDEO: https://www.youtube.com/watch?v=6FLeguySZLc

            else:
                # If no mentions are found, the type is tweepy.Client.Response
                print(type(mentions))
                print("No mentions.")

            # NOTE: Wait for 60 seconds before checking for new mentions becasue of the Twitter API rate limit (Basic access level)
            time.sleep(60)
            break   # TODO: Remove this in production

    except Exception as e:
        print(f"Bot chrashed at {time.ctime()}.\nError: {e}")
        with open("last_id.json", "w") as file:
            json.dump({'last_id': last_id}, file)


if __name__ == "__main__":
    client = get_client()
    user = client.get_user(username=BOT_SCREEN_NAME)
    bot_id = user.data.id

    main(client, bot_id)


# prompt = f"Generate jokes based on tweets and keywords. Respond with a joke based on the words used in the tweet: {}"
# QUESTIONS:
# NOTE: Should my bot reply to tweets or tweet and tag the person?
# NOTE: Should I have a list or sht of the mentiones that I have answered to since the get_users_mentions() method returns the last 10 mentions by minimum up to 800 max???
# NOTE: Should my bot reply to direct messages?
# NOTE: How do I counter the open rate limit of 300 requests per 15 minutes and the charging???? Check out the correct numbers.
# NOTE: How fast should the bot asnwer? What is the allowed limit?
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
# NOTE: With Basic you get 15 requests per 15 minutes

# NOTE:
"""
Environment Variables: Since your bot requires API keys and other sensitive information, it's important to securely manage your credentials. 
Heroku provides a way to set environment variables that can be accessed by your application. This allows you to store sensitive information 
separately and ensure it's not exposed in your codebase.
"""
