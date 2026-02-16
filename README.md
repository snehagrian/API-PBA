# 🚀 AI-Powered API Performance Bottleneck Analyzer

> Ever spent hours debugging why your API suddenly became slow? Yeah, me too. That's why I built this.

This is an intelligent backend service that analyzes your API logs, spots the performance bottlenecks you might miss, and uses OpenAI to tell you exactly what's wrong and how to fix it. Think of it as having a senior performance engineer review your logs 24/7.

## 💡 The Problem I'm Solving

We've all been there:
- Your API is slow but you don't know which endpoint is the culprit
- Error rates spike and you're drowning in logs trying to find patterns
- You suspect database issues but can't pinpoint the N+1 queries
- By the time you manually analyze everything, users are already frustrated

**This tool does in seconds what normally takes hours of manual log analysis.**

## ✨ What Makes This Different

Instead of just showing you charts and numbers, this analyzer:
- 🔍 **Actually understands your logs** - Detects slow endpoints (>500ms), high error rates (>5%), and database-heavy operations
- 🤖 **AI-powered insights** - Uses OpenAI GPT-4 to explain root causes in plain English
- 💊 **Gives you the fix** - Not just "this is slow" but "add this index, implement this cache, here's the code"
- ⚡ **Works in real-time** - Drop in your logs, get answers immediately

## 🎯 Perfect For Your Resume

I built this to showcase real-world skills that matter:
- API performance optimization (the stuff that actually moves the needle)
- AI/ML integration that solves real problems
- FastAPI microservices (production-ready, not tutorial code)
- The kind of observability work that prevents 3am incidents

## 🛠️ Tech Stack

- **FastAPI** - Because life's too short for slow frameworks
- **OpenAI GPT-4** - The brains of the operation
- **Python 3.8+** - Clean, readable, maintainable
- **Pydantic** - Because data validation shouldn't be an afterthought

## 📦 Getting Started

### Installation (2 minutes, I promise)

```bash
# Clone this repo
cd api-pba

# Set up your environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install everything
pip install -r requirements.txt
```

### Get Your OpenAI API Key

You'll need an OpenAI API key (don't worry, it's free to start):
1. Head to https://platform.openai.com/api-keys
2. Create a new key
3. Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
# Then edit .env and paste your key
OPENAI_API_KEY=sk-your-actual-key-here
```

### Fire It Up

```bash
# Start the server
python main.py
```

Visit **http://localhost:8000/docs** and you'll see the interactive API docs. Pretty cool, right?

### Try It Out

I've included realistic sample data (think e-commerce API logs). Run this in another terminal:

```bash
python test_analyzer.py
```

You'll see it analyze 50+ log entries and give you detailed AI recommendations. Takes about 5 seconds.

## 📡 How It Works

### Main Endpoint: `POST /analyze`

Send your logs, get insights back. Simple as that.

**What you send:**
```json
{
  "logs": [
    {
      "endpoint": "/api/users/search",
      "response_time_ms": 1250,
      "status_code": 200,
      "db_query_count": 15,
      "timestamp": "2026-02-16T10:15:23Z",
      "method": "GET"
    }
  ],
  "use_ai": true
}
```

**What you get back:**
```json
{
  "analysis": {
    "total_logs_analyzed": 51,
    "slow_endpoints": [/* The problematic ones */],
    "high_error_endpoints": [/* What's breaking */],
    "db_heavy_endpoints": [/* Database bottlenecks */]
  },
  "ai_recommendations": {
    "status": "bottlenecks_detected",
    "ai_analysis": "Here's what's actually wrong and how to fix it..."
  }
}
```

### Quick Analysis: `POST /quick-analyze`

Need just the essentials? This endpoint skips the AI analysis for faster responses. Great for dashboards or monitoring systems.

### Health Check: `GET /health`

Check if everything's running and your OpenAI connection is good.

## 📊 Real Output Example

Here's what you actually see when you run it:

```
📊 ANALYSIS RESULTS
============================================================

✅ Total logs analyzed: 51
✅ Unique endpoints: 12

🐌 SLOW ENDPOINTS:
  - /api/reports/export
    Avg: 3483.33ms | P95: 3800.0ms
    
  - /api/analytics/dashboard  
    Avg: 2255.0ms | P95: 2550.0ms

💾 DB-HEAVY ENDPOINTS:
  - /api/reports/export
    Avg queries: 48.33 (!! This is your N+1 problem)

🤖 AI RECOMMENDATIONS
============================================================

ROOT CAUSE ANALYSIS:
The /api/reports/export endpoint is doing way too much work. You're 
making 48+ database queries per request - classic N+1 problem. Plus,
you're generating these reports synchronously which is killing your 
response times.

IMMEDIATE FIXES (do these first):
1. Move report generation to a background job (Celery/Redis)
2. Add SELECT query eager loading: .select_related('user', 'product')
3. Implement Redis caching with 5-minute TTL for dashboard queries
4. Create this composite index:
   CREATE INDEX idx_user_search ON users(name, email, created_at);

CODE EXAMPLE:
[Actual code snippets you can copy-paste]

ARCHITECTURE IMPROVEMENTS:
- Consider async endpoints for long-running operations
- Implement connection pooling (you're likely exhausting connections)
...
```

No jargon, no guessing - just actionable advice.

## 🔧 Customize It

### Adjust Detection Thresholds

Want different definitions of "slow"? Edit [main.py](main.py):

```python
log_analyzer = LogAnalyzer(
    slow_threshold_ms=300,      # I consider 300ms slow
    error_rate_threshold=0.10   # 10% error rate triggers alerts
)
```

### Use a Different AI Model

Want to save money or try different models? Edit [ai_analyzer.py](ai_analyzer.py):

```python
model="gpt-3.5-turbo",  # Cheaper, still pretty good
temperature=0.7,
max_tokens=1000
```

## 🧪 Use Your Own Logs

Got real logs to analyze? Here's how:

```python
import requests
import json

# Load your logs (from file, database, wherever)
with open('my_api_logs.json') as f:
    my_logs = json.load(f)

# Analyze them
response = requests.post(
    "http://localhost:8000/analyze",
    json={"logs": my_logs, "use_ai": True}
)

print(response.json())
```

Each log entry just needs: `endpoint`, `response_time_ms`, `status_code`, and optionally `db_query_count`.

## 📁 Project Structure

```
api-pba/
├── main.py              # FastAPI app - all the endpoints live here
├── log_analyzer.py      # The actual analysis logic (statistics, pattern detection)
├── ai_analyzer.py       # OpenAI integration - where the magic happens
├── requirements.txt     # Dependencies
├── sample_logs.json     # 51 realistic log entries to play with
├── test_analyzer.py     # Quick test script
├── .env.example         # Template for your API key
└── README.md            # You are here
```

## 🎓 What I Learned Building This

This project taught me a ton about:
- Building production-ready APIs that don't fall over
- Actually using AI for something useful (not just chatbots)
- Performance analysis that matters in real systems
- Writing code that other developers can actually understand
- The difference between "it works" and "it works well"

## 🚀 Ideas for Extensions

Want to take this further? Here are some ideas:

1. **Add a database** - Store analysis history, track trends over time
2. **Real-time streaming** - WebSocket support for live log analysis
3. **Build a UI** - React dashboard with beautiful charts
4. **Email alerts** - "Your API is on fire" notifications
5. **Prometheus metrics** - Export metrics for Grafana
6. **Multi-project support** - Analyze logs from different services

## 📝 The Interactive Docs

Once you have the server running, check out:
- **Swagger UI**: http://localhost:8000/docs (try the API right in your browser)
- **ReDoc**: http://localhost:8000/redoc (pretty documentation)

## 🤝 Want to Contribute?

Found a bug? Have an idea? Feel free to:
- Open an issue
- Submit a PR
- Fork it and make it your own
- Use it in your own projects

## 💬 Why I Built This

I've seen too many teams struggle with API performance issues. They have tons of logs but no easy way to make sense of them. Manual analysis is slow and error-prone. 

I wanted something that could:
- Analyze logs faster than any human
- Catch patterns we might miss
- Give recommendations that are actually useful
- Be simple enough to use in 5 minutes

This is that tool. Hope it helps you as much as it helped me learn.

## 📄 License

MIT - Do whatever you want with it. Build something cool.

---

**Questions? Found this useful? Let me know!**

*Built by someone who's spent too many late nights debugging slow APIs* 😅
