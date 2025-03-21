from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.ollama import Ollama
import json
import random
import os

# Initialize FastAPI
app = FastAPI(title="Augustine API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the Query class
class Query(BaseModel):
    question: str

class TweetResponse(BaseModel):
    tweet: str
    prompt: str

def load_tweet_prompts():
    # Go up one directory from api/main.py to find tweet_prompts.json
    prompts_path = os.path.join(os.path.dirname(__file__), '..', 'tweet_prompts.json')
    print(f"Looking for prompts file at: {prompts_path}")  # Debug print
    
    if not os.path.exists(prompts_path):
        raise HTTPException(
            status_code=500,
            detail=f"Prompts file not found at {prompts_path}"
        )
    
    try:
        with open(prompts_path, 'r') as f:
            data = json.load(f)
            if not data.get('prompts'):
                raise HTTPException(
                    status_code=500,
                    detail="No prompts found in prompts file"
                )
            return data['prompts']
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON in prompts file: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading prompts: {str(e)}"
        )

# Initialize Ollama for tweets
tweet_llm = Ollama(
    model="augustine",
    temperature=0.7,
    max_tokens=100,
)

@app.get("/tweet")
async def generate_tweet():
    try:
        # Get prompts
        prompts = load_tweet_prompts()
        if not prompts:
            raise HTTPException(status_code=500, detail="No prompts available")
        
        # Select random prompt
        prompt = random.choice(prompts)
        
        # Add specific instruction for tweet length
        full_prompt = f"Provide a tweet-length response (maximum 280 characters, no hashtags, no icons, no emojis) to: {prompt}"
        
        # Get response from Ollama
        response = tweet_llm.complete(full_prompt)
        tweet = str(response).strip()
        tweet = " ".join(tweet.split())  # Replace all whitespace with single spaces
        
        # Ensure tweet length
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
            
        return TweetResponse(
            tweet=tweet,
            prompt=prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/tweet_response")
async def generate_tweet_response(query: Query):
    try:
        # Format the prompt to ensure a tweet-length response
        full_prompt = f"Provide a tweet-length response (maximum 280 characters, no hashtags, no icons, no emojis) to this message: {query.question}"
        
        # Get response from Ollama
        response = tweet_llm.complete(full_prompt)
        tweet = str(response).strip()
        tweet = " ".join(tweet.split())  # Replace all whitespace with single spaces
        
        # Ensure tweet length
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
            
        return {"tweet": str(tweet)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/wise_tweet")
async def generate_wise_tweet():
    try:
        # Direct request for a tweet-length wisdom
        full_prompt = "Share a brief, profound spiritual insight or reflection in a tweet (maximum 280 characters, no hashtags, no icons, no emojis)."
        
        # Get response from Ollama
        response = tweet_llm.complete(full_prompt)
        tweet = str(response).strip()
        
        # Ensure tweet length
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
            
        return {"tweet": str(tweet)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Initialize Ollama with custom parameters
llm = Ollama(
    model="augustine",
    temperature=0.7,
    context_window=4096,  # Increased context window
    max_tokens=1000,      # Increased max response length
    num_predict=1000,     # Alternative way to control response length
)

@app.post("/ask")
async def ask_augustine(query: Query):
    try:
        # Use Ollama with completion parameters
        response = llm.complete(
            query.question,
            temperature=0.7,
            max_tokens=1000,
            num_predict=1000
        )
        return {"response": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)