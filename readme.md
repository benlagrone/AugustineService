Building Augustine Twitter Bot: Step-by-Step Guide
1. Text Collection & Processing
Step 1: Gather Augustine's Texts
Download from New Advent (www.newadvent.org/fathers/)
Confessions
City of God
On Christian Doctrine
Letters
Save raw HTML files in augustine_texts/ directory
Step 2: Clean & Process Texts
Remove HTML formatting
Remove footnotes and references
Split into logical chunks (paragraphs/sections)
Maintain theological context within chunks
Save as clean text files
Step 3: Create Vector Database
Use Chroma DB for similarity search
Store in augustine_index/ directory
Embeddings capture theological concepts
Enables semantic search of Augustine's writings
2. LLM Setup
Step 1: Install Ollama
Local installation for custom model
Enables fine-tuning and context injection
Maintains low latency for responses
Step 2: Configure Model
Base: Mistral (good balance of size/quality)
Temperature: 0.8 (creative but controlled)
System prompt: Augustine's persona and style
Include historical context (354-430 AD)
Step 3: Query Process
Receive input query
Search vector DB for relevant texts
Inject found context into Ollama prompt
Generate response in Augustine's voice
Format for Twitter length
3. Image Generation
Step 1: Setup Stable Diffusion
Install WebUI with API enabled
Port 7861 for API access
Install medieval manuscript model
Step 2: Image Generation Process
Take generated wisdom text
Combine with Pre-Raphaelite style prompt
Generate image with Augustine theme
Save to timestamped directory in output/
Save prompt for reproducibility
4. Twitter Integration
Step 1: Developer Setup
Create Twitter Developer account
Setup Project and App
Get necessary API keys/tokens
Store in .env file
Step 2: Posting Process
Generate wisdom using LLM
Create matching image
Post tweet with image
Handle rate limits
Save outputs
5. Rate Limits & Monitoring
Twitter Limits
50 tweets per 24 hours
180 mention checks per 15 minutes
Schedule posts accordingly
Local Resources
Monitor Stable Diffusion memory
Track Ollama response times
Manage disk space for outputs
6. Directory Structure
logic
7. Operational Flow
Start Stable Diffusion WebUI
Start Ollama service
Run bot script
Monitor output directory
Check Twitter for posts
