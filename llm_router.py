import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
# Add other API keys as needed
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
together_api_key = os.getenv("TOGETHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
# Add other API keys as needed

def get_prompt(persona):
    prompts = {
        "Augustine": """You are Augustine of Hippo, responding to questions in a conversational manner.
When discussing theological or philosophical topics, always follow this format:
1. Begin by mentioning which of your works you're drawing from (e.g., "As I wrote in De Genesi ad litteram...")
2. Provide the relevant quote using markdown blockquotes (e.g., > "quote here")
3. Then explain your meaning and how it relates to the question
4. If multiple works are relevant, repeat this pattern for each one

For example:
"As I wrote in De Genesi ad litteram:
> 'When we deal with the mysteries of Nature (which, we believe, is God Almighty's workmanship), our methodology should be to ask questions rather than to make claims.'
Let me explain what I meant by this..."

When asked about previous messages, focus ONLY on the conversation history provided.
Maintain your role as Augustine while directly addressing the current conversation."""
    }
    return prompts.get(persona, "You are a wise sage...")

def openai_call(messages):
    try:
        # Print the messages being sent to ChatGPT
        print("\n=== Messages being sent to ChatGPT ===")
        for msg in messages:
            print(f"\nRole: {msg['role']}")
            print(f"Content: {msg['content']}\n")
        print("=====================================\n")

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            timeout=30
        )
        return response.choices[0].message.content.strip()
    except openai.APITimeoutError as e:
        return "Request timed out. Please try again later."
    except openai.APIError as e:
        return f"Error with OpenAI API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def query_llm(query, context, persona, provider='openai'):
    # Print the raw inputs
    print("\n=== Raw Inputs ===")
    print(f"Query: {query}")
    print(f"Context: {context}")
    print(f"Persona: {persona}")
    print("=================\n")

    messages = [
        {"role": "system", "content": get_prompt(persona)},
        {"role": "user", "content": f"{context}\n\n{query}"}
    ]
    
    if provider == 'openai':
        return openai_call(messages)
    elif provider == 'deepseek':
        return deepseek_call(messages)
    elif provider == 'together':
        return together_call(messages)
    elif provider == 'groq':
        return groq_call(messages)
    elif provider == 'anthropic':
        return claude_call(messages)
    else:
        return "Unsupported provider"

# Placeholder functions for other providers
def deepseek_call(messages):
    # Implement DeepSeek API call
    return "DeepSeek response"

def together_call(messages):
    # Implement Together API call
    return "Together response"

def groq_call(messages):
    # Implement Groq API call
    return "Groq response"

def claude_call(messages):
    # Implement Anthropic Claude API call
    return "Claude response"

def query_llm(query, context, persona, provider='openai'):
    messages = [
        {"role": "system", "content": get_prompt(persona)},
        {"role": "user", "content": f"{context}\n\n{query}"}
    ]
    if provider == 'openai':
        return openai_call(messages)
    elif provider == 'deepseek':
        return deepseek_call(messages)
    elif provider == 'together':
        return together_call(messages)
    elif provider == 'groq':
        return groq_call(messages)
    elif provider == 'anthropic':
        return claude_call(messages)
    else:
        return "Unsupported provider"

def get_llm_response(question, context, mode, persona):
    """
    Route the query to the appropriate LLM API based on the mode and persona.
    
    :param question: The question to be answered.
    :param context: The context to be used for generating the response.
    :param mode: The mode of interaction ('reference' or 'conversation').
    :param persona: The persona to be used (e.g., 'Augustine').
    :return: The generated response from the LLM.
    """
    # Use the query_llm function to get the response
    return query_llm(question, context, persona, provider='openai')  # Default to OpenAI