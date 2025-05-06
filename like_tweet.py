import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET'),
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_SECRET')
)

# Create API object
api = tweepy.API(auth)

# Function to like a tweet by its ID
def like_tweet(tweet_id):
    try:
        api.create_favorite(tweet_id)
        print(f"Liked tweet with ID: {tweet_id}")
    except tweepy.TweepError as e:
        print(f"Error: {e.reason}")

# Example usage: replace 'tweet_id' with the actual tweet ID you want to like
tweet_id = '1234567890123456789'
like_tweet(tweet_id)