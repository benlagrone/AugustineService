import tweepy
import requests
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_image(tweet_text):
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    
    # Combine the tweet theme with the Pre-Raphaelite style prompt
    prompt = f"""A Pre-Raphaelite style scene illustrating the wisdom: '{tweet_text}'. 
    Saint Augustine sits in his study at Hippo, a stone archway frames him as he writes this very message. 
    Golden divine light streams through the arch, creating a path of illumination that mirrors the tweet's meaning. 
    He wears rich burgundy and gold episcopal robes, his expression deeply contemplative of these words. 
    The scene opens to the North African coastline at sunset, with dramatic clouds in deep purples and golds. 
    Climbing roses and vines with intricate Pre-Raphaelite botanical details frame the scene. 
    The lighting and composition specifically emphasize the message about {tweet_text.lower()}"""

    payload = {
        "prompt": prompt,
        "negative_prompt": "text, logos, modern elements, cartoon, anime, photographic, cluttered, busy, grainy, blurry, deformed, abnormal limbs, black, African, blurry, or deformed faces, asymmetrical face, asymmetrical body, missing eyesx",
        "steps": 20,
        "sampler_name": "DPM++ 2M Karras",
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "model": "ral-medieval-manuscripts-flux"
    }

    try:
        print("\nGenerating image with Stable Diffusion...")
        response = requests.post(url=url, json=payload)
        r = response.json()
        
        # Decode and save the image
        image_data = base64.b64decode(r['images'][0])
        image_path = "augustine_tweet_image.png"
        with open(image_path, 'wb') as f:
            f.write(image_data)
        print("Image generated successfully!")
        return image_path
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def setup_twitter():
    # Create Client for v2 endpoints
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_SECRET')
    )
    
    # Also create API v1.1 instance for media upload
    auth = tweepy.OAuth1UserHandler(
        os.getenv('TWITTER_API_KEY'),
        os.getenv('TWITTER_API_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_SECRET')
    )
    api = tweepy.API(auth)
    
    return client, api

def get_wisdom():
    try:
        response = requests.get("http://localhost:8080/wise_tweet")
        if response.status_code == 200:
            wisdom = response.json()["tweet"]
            print(f"\nGenerated wisdom: {wisdom}")
            return wisdom
        else:
            print(f"Error getting wisdom: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def post_tweet_with_generated_image():
    try:
        print("\nInitializing Twitter client...")
        client, api = setup_twitter()
        
        print("\nGetting wisdom...")
        wisdom = get_wisdom()
        
        if wisdom:
            # Generate image based on the tweet
            image_path = generate_image(wisdom)
            
            if image_path:
                print("\nUploading image to Twitter...")
                # Upload image first (using v1.1 endpoint)
                media = api.media_upload(image_path)
                
                print("\nAttempting to post tweet with image...")
                # Create tweet with media (using v2 endpoint)
                tweet = client.create_tweet(
                    text=wisdom,
                    media_ids=[media.media_id]
                )
                
                print(f"Success! Posted tweet at {datetime.now()}")
                print(f"Tweet content: {wisdom}")
                
                # Clean up the image file
                os.remove(image_path)
                return True
            
        return False
    
    except Exception as e:
        print(f"\nError posting tweet: {type(e).__name__}")
        print(f"Full error details: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nStarting tweet poster...")
    post_tweet_with_generated_image()