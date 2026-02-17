# AI-Powered API Performance Bottleneck Analyzer

Automated API log analysis with OpenAI-powered recommendations. Detects slow endpoints, high error rates, and database bottlenecks with actionable fixes.

## Features

- Identifies slow endpoints (>500ms), high error rates (>5%), and database-heavy operations
- **Multiple AI Providers**: Choose between OpenAI GPT-4 or Anthropic Claude for analysis
- GPT-4 or Claude-powered root cause analysis and optimization recommendations
- FastAPI backend with Docker containerization
- Interactive API documentation at `/docs`

## Tech Stack

- FastAPI + Uvicorn
- OpenAI GPT-4 or Anthropic Claude
- Python 3.11
- Docker & Docker Compose

## Quick Start

### Docker (Recommended)

```bash
# Create .env file with your AI provider and API key
# For OpenAI:
echo "AI_PROVIDER=openai" > .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# For Claude:
echo "AI_PROVIDER=claude" > .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# Build and run
docker-compose up --build
```

API available at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### Local Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env with your AI provider and API key
cp .env.example .env
# Edit .env and configure:
# - AI_PROVIDER=openai or claude
# - OPENAI_API_KEY=sk-... (if using OpenAI)
# - ANTHROPIC_API_KEY=sk-ant-... (if using Claude)

python main.py
```

## Usage

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze sample logs
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"logs":'"$(cat sample_logs.json)"',"use_ai":false}'

# Run test script
python test_analyzer.py
```

### API Endpoints

**POST /analyze**
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
  "use_ai": true,
  "ai_provider": "claude"  // Optional: "openai" or "claude" (overrides env)
}
```

Returns: Performance analysis with AI-powered recommendations for optimization.

**GET /health** - Health check endpoint (shows configured AI provider)

**GET /docs** - Interactive Swagger UI documentation

### AI Provider Configuration

Choose between OpenAI or Claude for AI analysis:

**Using OpenAI (default):**
```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
```

**Using Claude:**
```bash
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-claude-key
```

**Override per request:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"logs":[...], "use_ai":true, "ai_provider":"claude"}'
```

### Configuration

**Analysis thresholds** - Edit `main.py`:

```python
log_analyzer = LogAnalyzer(
    slow_threshold_ms=500,
    error_rate_threshold=0.05
)
```

**AI Models used:**
- OpenAI: `gpt-4-turbo-preview`
- Claude: `claude-3-5-sonnet-20241022`

## Project Structure

```
api-pba/
├── main.py              # FastAPI application
├── log_analyzer.py      # Analysis logic
├── ai_analyzer.py       # OpenAI integration
├── requirements.txt     # Dependencies
├── sample_logs.json     # Sample data
├── test_analyzer.py     # Test script
├── Dockerfile           # Container config
├── docker-compose.yml   # Docker orchestration
└── .env.example         # API key template
```

## Docker Commands

```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker logs api-pba-container -f

# Rebuild
docker-compose up --build
```

## Deployment

**AWS ECS/Fargate:**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag api-pba:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-pba:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/api-pba:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy api-pba --source . --platform managed --region us-central1
```

**Heroku:**
```bash
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

## License

MIT
