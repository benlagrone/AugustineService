from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.ollama import Ollama
from models import Query, TweetResponse, Query
# from RAG import get_context 
import json
import random
import sys
import os
from RAG import get_context
from llm_router import get_llm_response
from mysql_memory import store_chat_message, retrieve_chat_history
import uuid  # Add this import for generating session IDs

# Initialize FastAPI
app = FastAPI(title="Augustine API")


api_v1_router = APIRouter(prefix="/api/v1")
api_v2_router = APIRouter(prefix="/api/v2")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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

@api_v1_router.get("/health")
async def health_check():
    return {"status": "ok"}

@api_v1_router.post("/chat")
async def chat_with_augustine(query: Query):
    try:
        # Use existing session ID if provided, otherwise create new one
        session_id = query.session_id if query.session_id else str(uuid.uuid4())
        user_id = "default_user"
        
        # Retrieve existing chat history for this session
        chat_history = retrieve_chat_history(session_id)
        
        # Format previous conversations for context
        conversation_context = ""
        # In the chat endpoint, modify the context building:
        if chat_history:
            conversation_context = "Here's our conversation history:\n\n" + "\n".join([
                f"{'Human' if msg['role'] == 'user' else 'Augustine'}: {msg['message']}"
                for msg in chat_history[-4:]  # Get last 4 messages for context
            ])
            
            if query.question.lower().strip() in [
                "what did we discuss?",
                "what did we talk about?",
                "what did we discuss in our previous messages?",
                "what was our previous conversation about?"
            ]:
                context = conversation_context
            # In the chat endpoint:
            else:
                # Modified to explicitly request source citations and quotes
                rag_context = get_context(query.question, author=query.persona)
                context = (
                    f"{conversation_context}\n\n"
                    f"Relevant passages from my works:\n{rag_context}\n\n"
                    "Please cite the specific work each quote comes from and explain its relevance to the question."
                )
        else:
            # If no chat history, just use RAG context with quote request
            context = (
                f"Relevant background with original text:\n{get_context(query.question, author=query.persona)}\n\n"
                "Please include relevant quotes from the provided text in your response."
            )
        
        # Generate response
        response = get_llm_response(
            question=query.question,
            context=context,
            mode=query.mode,
            persona=query.persona
        )
        
        # Store both the new question and response
        store_chat_message(user_id, session_id, "user", query.question)
        store_chat_message(user_id, session_id, "assistant", response)
        
        return {
            "response": response,
            "session_id": session_id,
            "chat_history": retrieve_chat_history(session_id)
        }
    except Exception as e:
        print(f"\nError in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

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

app.include_router(api_v1_router)
app.include_router(api_v2_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)