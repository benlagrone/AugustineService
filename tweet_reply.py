import os
import time
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# ✅ Twitter API v2 endpoint (Search for bot mentions)
BASE_URL = "https://api.twitter.com/2/tweets/search/recent"

# ✅ Track last seen tweet ID (to avoid duplicates)
LAST_SEEN_FILE = "last_seen_id.txt"

def get_last_seen_id():
    """Retrieve the last seen tweet ID."""
    try:
        with open(LAST_SEEN_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_last_seen_id(last_seen_id):
    """Save the last processed mention tweet ID."""
    with open(LAST_SEEN_FILE, "w") as file:
        file.write(str(last_seen_id))

def check_mentions():
    """Fetch new mentions using Twitter API v2."""
    last_seen_id = get_last_seen_id()
    query = "@YourBotUsername -is:retweet"  # Exclude retweets

    # API Request Parameters
    params = {
        "query": query,
        "tweet.fields": "author_id,created_at",
        "max_results": 10  # Limit to 10 latest mentions
    }

    if last_seen_id:
        params["since_id"] = last_seen_id  # Fetch only new mentions

    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    
    print("[🔍] Checking for new mentions...")
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"[❌] API Error {response.status_code}: {response.text}")
        return

    mentions = response.json().get("data", [])
    
    if not mentions:
        print("[✅] No new mentions found.")
        return

    for mention in reversed(mentions):
        tweet_id = mention["id"]
        user_id = mention["author_id"]
        text = mention["text"]

        print(f"[📩] New Mention from User ID {user_id}: {text}")

        # Save last seen tweet ID
        save_last_seen_id(tweet_id)

        # OPTIONAL: Auto-reply (uncomment to enable)
        # reply_to_mention(tweet_id, user_id)

    print("[✅] Done checking mentions.")

# OPTIONAL: Function to auto-reply (API v2 does NOT allow replies on Free tier)
def reply_to_mention(tweet_id, user_id):
    """Reply to a mention (Not allowed in free plan, but ready if upgraded)."""
    reply_text = f"@{user_id} Thanks for mentioning me! 🤖"
    print(f"[✍️] Would reply: {reply_text}")
    # API v2 does not support replies on Free plan (only in paid plans)

# ✅ Run every 30 seconds
while True:
    check_mentions()
    time.sleep(30)  # Adjust as needed