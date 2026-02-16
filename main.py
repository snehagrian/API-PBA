from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from log_analyzer import LogAnalyzer
from ai_analyzer import AIAnalyzer

app = FastAPI(
    title="API Performance Bottleneck Analyzer",
    description="AI-powered API performance analysis and optimization recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
log_analyzer = LogAnalyzer(slow_threshold_ms=500, error_rate_threshold=0.05)


class LogEntry(BaseModel):
    """Schema for API log entry"""
    endpoint: str = Field(..., description="API endpoint path", json_schema_extra={"example": "/api/users"})
    response_time_ms: float = Field(..., description="Response time in milliseconds", json_schema_extra={"example": 234.5})
    status_code: int = Field(..., description="HTTP status code", json_schema_extra={"example": 200})
    db_query_count: Optional[int] = Field(0, description="Number of database queries", json_schema_extra={"example": 3})
    timestamp: Optional[str] = Field(None, description="Log timestamp", json_schema_extra={"example": "2026-02-16T10:30:00Z"})
    method: Optional[str] = Field("GET", description="HTTP method", json_schema_extra={"example": "GET"})


class AnalyzeRequest(BaseModel):
    """Request body for analysis"""
    logs: List[LogEntry] = Field(..., description="List of API log entries")
    use_ai: bool = Field(True, description="Enable AI-powered recommendations")


class AnalysisResponse(BaseModel):
    """Response schema for analysis"""
    analysis: Dict[str, Any]
    ai_recommendations: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "API Performance Bottleneck Analyzer",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    try:
        # Test OpenAI connection
        ai_analyzer = AIAnalyzer()
        ai_status = "connected"
    except Exception as e:
        ai_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "log_analyzer": "ready",
        "ai_analyzer": ai_status
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_logs(request: AnalyzeRequest):
    """
    Analyze API logs and detect performance bottlenecks
    
    This endpoint:
    1. Analyzes logs to detect slow endpoints, high error rates, and DB-heavy operations
    2. (Optional) Uses OpenAI to provide root cause analysis and recommendations
    
    Returns detailed analysis with actionable insights
    """
    try:
        # Convert Pydantic models to dicts
        logs_data = [log.model_dump() for log in request.logs]
        
        # Perform log analysis
        analysis = log_analyzer.analyze_logs(logs_data)
        
        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])
        
        result = {
            "analysis": analysis,
            "ai_recommendations": None
        }
        
        # Get AI recommendations if requested
        if request.use_ai:
            try:
                ai_analyzer = AIAnalyzer()
                issues = log_analyzer.get_critical_issues(analysis)
                ai_recommendations = ai_analyzer.analyze_bottlenecks(issues, analysis)
                result["ai_recommendations"] = ai_recommendations
            except ValueError as e:
                # OpenAI API key not configured
                result["ai_recommendations"] = {
                    "status": "disabled",
                    "message": str(e)
                }
            except Exception as e:
                result["ai_recommendations"] = {
                    "status": "error",
                    "message": f"AI analysis failed: {str(e)}"
                }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/quick-analyze")
async def quick_analyze(logs: List[LogEntry]):
    """
    Quick analysis without AI recommendations
    Faster endpoint for basic bottleneck detection
    """
    try:
        logs_data = [log.model_dump() for log in logs]
        analysis = log_analyzer.analyze_logs(logs_data)
        
        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])
        
        # Extract just the critical summary
        return {
            "summary": analysis.get("summary", {}),
            "top_slow_endpoint": analysis.get("slow_endpoints", [{}])[0] if analysis.get("slow_endpoints") else None,
            "top_error_endpoint": analysis.get("high_error_endpoints", [{}])[0] if analysis.get("high_error_endpoints") else None,
            "total_logs": analysis.get("total_logs_analyzed", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
