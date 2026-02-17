# AI-Powered API Performance Bottleneck Analyzer

Automated API log analysis with OpenAI-powered recommendations. Detects slow endpoints, high error rates, and database bottlenecks with actionable fixes.

## Features

- Identifies slow endpoints (>500ms), high error rates (>5%), and database-heavy operations
- GPT-4 powered root cause analysis and optimization recommendations
- FastAPI backend with Docker containerization
- Interactive API documentation at `/docs`

## Tech Stack

- FastAPI + Uvicorn
- OpenAI GPT-4
- Python 3.11
- Docker & Docker Compose

## Quick Start

### Docker (Recommended)

```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

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

# Create .env with your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

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
  "use_ai": true
}
```

Returns: Performance analysis with AI-powered recommendations for optimization.

**GET /health** - Health check endpoint

**GET /docs** - Interactive Swagger UI documentation

### Configuration

Edit `main.py` to adjust thresholds:

```python
log_analyzer = LogAnalyzer(
    slow_threshold_ms=500,
    error_rate_threshold=0.05
)
```

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
