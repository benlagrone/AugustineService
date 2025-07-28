# AugustineService: Local Chatbot Dev Plan (Handoff Document)

## 🧱 Purpose

Turn this existing repository into a complete local-first chatbot that:

* Uses RAG from `RAG.py` for contextual answers
* Supports both reference and conversational styles
* Stores UI chat history and session metadata in MySQL
* Supports switching LLMs (ChatGPT, DeepSeek, etc.) via `llm_router.py`
* Retains existing structure without moving files

---

## ✅ Phase 1: FastAPI Entry + Endpoint

Use `api/main.py` as your central FastAPI entrypoint.
Add a new endpoint:

```python
POST /ask
{
  "query": "What is grace?",
  "mode": "reference",       # or "conversation"
  "persona": "Augustine",
  "provider": "openai",
  "user_id": "abc123",
  "session_id": "sess456"
}
```

Return:

```json
{
  "response": "Grace is the unmerited favor..."
}
```

Use `RAG.py` for reference context via a helper in the same file:

```python
from RAG import get_context
```

---

## ✅ Phase 2: Add Support Modules (Non-invasive)

### Add to `/api` (new files)

* `llm_router.py`: Abstracts LLM API calls
* `prompts.py`: Contains Augustine persona/system prompts
* `memory.py`: In-memory chat history (development only)
* `mysql_memory.py`: MySQL-backed session + history storage

No need to move `RAG.py`, `query_augustine.py`, or tweet files.

---

## ✅ Phase 3: MySQL Persistence for UI Chat + Sessions

### SQL Tables (add to `sql/schema.sql`)

```sql
CREATE TABLE chat_ui_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id VARCHAR(64),
  session_id VARCHAR(64),
  role ENUM('user', 'assistant'),
  message TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_sessions (
  session_id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64),
  persona VARCHAR(32),
  mode VARCHAR(32),
  start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
  active BOOLEAN DEFAULT TRUE
);
```

---

## ✅ Phase 4: Add React Chat Frontend (`/frontend`)

Build a basic chat UI that:

* Sends query via POST `/ask`
* Loads last messages from `/chat/load-session`
* Has toggles for persona and mode
* Stores messages in browser or backend

You can use Vite or Create React App.

---

## ✅ Phase 5: `.env` File Additions

```
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=...
MODEL_PROVIDER=openai
MYSQL_HOST=localhost
MYSQL_USER=youruser
MYSQL_PASS=yourpass
MYSQL_DB=augustine_chat
```

---

## ✅ Phase 6: Add Freud Later (Optional Extension)

<!-- * Add `get_context(query, author="Freud")` in `RAG.py`
* Add Freud prompts to `prompts.py`
* Extend frontend to allow persona selection -->

---

## ✅ Phase 7: Tweet Integration (Keep Separate)

Your `tweet_poster.py` and `tweet_reply.py` are independent — no change needed. You can optionally:

* Call `/ask` from those scripts to generate tweet text
* Log posted tweets to MySQL if needed

---

## ✅ Working with ChatGPT in Cursor

Use Cursor’s ChatGPT for:

* Writing `llm_router.py` with support for multiple APIs
* Implementing MySQL functions in `mysql_memory.py`
* Refactoring long blocks into modular helpers

---

## ✅ Summary

| Feature             | Where It Goes             |
| ------------------- | ------------------------- |
| API Entry           | `api/main.py`             |
| RAG                 | `RAG.py` (already exists) |
| LLM Switching       | `api/llm_router.py`       |
| Prompts             | `api/prompts.py`          |
| Chat History (Dev)  | `api/memory.py`           |
| Chat History (Prod) | `api/mysql_memory.py`     |
| React Frontend      | `frontend/`               |
| Tweets              | `tweet_*.py` (no changes) |

---

**Author:** ChatGPT for Master Benjamin | Updated Handoff: Based on current repo layout, no restructuring required.
