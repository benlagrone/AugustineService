import tweepy
import requests
import os
import base64
import json
import time
import random
from datetime import datetime
from dotenv import load_dotenv
AUGUST_URL = os.getenv('AUGUST_URL')
FREUD_URL = os.getenv('FREUD_URL')

character = "augustine"


# Load environment variables from .env file
load_dotenv()

number_of_posts = 7 

def generate_image(tweet_text,character):
    url = "http://127.0.0.1:7861/sdapi/v1/txt2img"

    if character == "freud":
        prompt = f"""A scene in the style of early 20th-century Viennese realism illustrating the wisdom: '{tweet_text}'. 
            Sigmund Freud, represented in middle age, with his short beard and glasses, sits in his study, surrounded by books and notes. 
            A warm, introspective light illuminates his thoughtful expression as he contemplates the mysteries of the mind. 
            The scene is rich with details of a Viennese study, with a window showing a serene garden outside. 
            The lighting and composition specifically emphasize the depth of thought and introspection associated with psychoanalysis
            and the message about {tweet_text.lower()}"""  
        
        neg = "Freud as a woman, overweight Freud, old Freud, deformed face, deformed hands, text, logos, modern elements, cartoon, anime, photographic, cluttered, busy, grainy, blurry, deformed, abnormal limbs, black, African, blurry, or deformed faces, asymmetrical face, asymmetrical body, missing eyes"
    else:
        prompt = f"""A Pre-Raphaelite style scene illustrating the wisdom: '{tweet_text}'. 
            Saint Augustine sits in his study at Hippo, a stone archway frames him as he writes this very message. 
            Golden divine light streams through the arch, creating a path of illumination that mirrors the tweet's meaning. 
            He wears rich burgundy and gold episcopal robes, his expression deeply contemplative of these words. 
            The scene opens to the North African coastline at sunset, with dramatic clouds in deep purples and golds. 
            Climbing roses and vines with intricate Pre-Raphaelite botanical details frame the scene. 
            The lighting and composition specifically emphasize the message about {tweet_text.lower()}"""    

        neg = "Augustine as a woman, text, logos, modern elements, cartoon, anime, photographic, cluttered, busy, grainy, blurry, deformed, abnormal limbs, black, African, blurry, or deformed faces, asymmetrical face, asymmetrical body, missing eyes"               
    # Combine the tweet theme with the Pre-Raphaelite style prompt
    

    payload = {
        "prompt": prompt,
        "negative_prompt": neg,
        "steps": 20,
        "sampler_name": "DPM++ 2M Karras",
        "cfg_scale": 7,
        "width": 512,
        "height": 512,
        "override_settings": {
    "sd_model_checkpoint": "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
        }
    }

    try:
        print("\nGenerating image with Stable Diffusion...")
        response = requests.post(url=url, json=payload)
        
        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            return None
        
        r = response.json()
        
        # Debug: Print the entire response
        print("Response JSON:", json.dumps(r, indent=4))
        
        # Check if 'images' key is in the response
        if 'images' not in r or not r['images']:
            print("Error: No images found in the response")
            return None
        
        # Decode and save the image
        try:
            image_data = base64.b64decode(r['images'][0])
        except Exception as e:
            print(f"Error decoding image data: {e}")
            return None
        
        # Define the base output directory
        base_output_dir = "output"
        
        # Create a directory with the current datetime stamp inside the output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(base_output_dir, timestamp)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the image
        image_path = os.path.join(output_dir, "augustine_tweet_image.png")
        try:
            with open(image_path, 'wb') as f:
                f.write(image_data)
            print(f"Image saved successfully at {image_path}")
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
        
        # Save the request payload
        payload_path = os.path.join(output_dir, "request_payload.json")
        with open(payload_path, 'w') as f:
            json.dump(payload, f, indent=4)
        
        print("Image and payload saved successfully!")
        return image_path
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def setup_twitter(character):
    # Create Client for v2 endpoints
    if character == "augustine":
        client = tweepy.Client(
            consumer_key=os.getenv('AUGUST_TWITTER_API_KEY'),
            consumer_secret=os.getenv('AUGUST_TWITTER_API_SECRET'),
            access_token=os.getenv('AUGUST_TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('AUGUST_TWITTER_ACCESS_SECRET')
        )
        
        # Also create API v1.1 instance for media upload
        auth = tweepy.OAuth1UserHandler(
            os.getenv('AUGUST_TWITTER_API_KEY'),
            os.getenv('AUGUST_TWITTER_API_SECRET'),
            os.getenv('AUGUST_TWITTER_ACCESS_TOKEN'),
            os.getenv('AUGUST_TWITTER_ACCESS_SECRET')
        )
    else:
        client = tweepy.Client(
            consumer_key=os.getenv('FREUD_TWITTER_API_KEY'),
            consumer_secret=os.getenv('FREUD_TWITTER_API_SECRET'),
            access_token=os.getenv('FREUD_TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('FREUD_TWITTER_ACCESS_SECRET')
        )
        
        # Also create API v1.1 instance for media upload
        auth = tweepy.OAuth1UserHandler(
            os.getenv('FREUD_TWITTER_API_KEY'),
            os.getenv('FREUD_TWITTER_API_SECRET'),
            os.getenv('FREUD_TWITTER_ACCESS_TOKEN'),
            os.getenv('FREUD_TWITTER_ACCESS_SECRET')
        )
    api = tweepy.API(auth)
    
    return client, api

def get_wisdom(character):
    if character == "augustine":
        wisdom_url = AUGUST_URL
        try:
            response = requests.get(wisdom_url)
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
    else:
        wisdom_url = FREUD_URL
        try:
            response = requests.get(wisdom_url)
            if response.status_code == 200:
                tweet = response.json()["response"]
                print(f"\nGenerated Freud-like tweet: {tweet}")
                return tweet
            else:
                print(f"Error getting tweet: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def post_tweet_with_generated_image(character):
    try:
        print("\nInitializing Twitter client...")
        client, api = setup_twitter(character)
        
        print("\nGetting wisdom...")
        wisdom = get_wisdom(character)
        
        if wisdom:
            # Generate image based on the tweet
            image_path = generate_image(wisdom,character)
            
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


def random_delay():
    """Generate a random delay between 5 and 30 minutes"""
    delay_minutes = random.randint(5, 30)
    print(f"Waiting for {delay_minutes} minutes before next tweet...")
    time.sleep(delay_minutes * 60)  # Convert minutes to seconds


if __name__ == "__main__":
    print("\nStarting tweet poster...",character)
    # post_tweet_with_generated_image()

    for i in range(number_of_posts):
        post_tweet_with_generated_image(character)  
        random_delay()
        i+1
        # post_tweet(f"{tweet_content} #{i+1}")                       