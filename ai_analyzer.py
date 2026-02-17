import os
from typing import List, Dict, Any, Literal
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AIAnalyzer:
    """Multi-provider AI integration for bottleneck analysis (OpenAI/Claude)"""
    
    def __init__(self, provider: Literal["openai", "claude"] = "openai"):
        """
        Initialize AI analyzer with specified provider
        
        Args:
            provider: AI provider to use ("openai" or "claude")
        """
        self.provider = provider
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4-turbo-preview"
        
        elif provider == "claude":
            if not ANTHROPIC_AVAILABLE:
                raise ValueError("Anthropic library not installed. Run: pip install anthropic")
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-3-opus-20240229"  # Alternatively: claude-3-sonnet-20240229 or claude-3-haiku-20240307
        
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'claude'")
    
    def analyze_bottlenecks(
        self, 
        issues: List[str], 
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send bottleneck data to OpenAI for root cause analysis
        
        Args:
            issues: List of critical issues detected
            analysis_data: Full analysis data from log analyzer
        
        Returns:
            AI-generated recommendations and insights
        """
        if not issues:
            return {
                "status": "healthy",
                "message": "No significant bottlenecks detected",
                "recommendations": []
            }
        
        # Build prompt for AI
        prompt = self._build_analysis_prompt(issues, analysis_data)
        
        try:
            if self.provider == "openai":
                ai_analysis = self._get_openai_analysis(prompt)
            elif self.provider == "claude":
                ai_analysis = self._get_claude_analysis(prompt)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            return {
                "status": "bottlenecks_detected",
                "ai_analysis": ai_analysis,
                "provider": self.provider,
                "model": self.model,
                "issues_analyzed": len(issues),
                "raw_issues": issues
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": f"Failed to get AI analysis from {self.provider}"
            }
    
    def _get_openai_analysis(self, prompt: str) -> str:
        """Get analysis from OpenAI"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert backend performance engineer specializing in API optimization, 
                    database query optimization, and microservices architecture. Analyze API performance bottlenecks 
                    and provide actionable, code-level recommendations."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def _get_claude_analysis(self, prompt: str) -> str:
        """Get analysis from Claude"""
        system_message = """You are an expert backend performance engineer specializing in API optimization, 
        database query optimization, and microservices architecture. Analyze API performance bottlenecks 
        and provide actionable, code-level recommendations."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            temperature=0.7,
            system=system_message,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.content[0].text
    
    def _build_analysis_prompt(self, issues: List[str], analysis_data: Dict[str, Any]) -> str:
        """Build detailed prompt for OpenAI"""
        
        issues_text = "\n".join([f"{i+1}. {issue}" for i, issue in enumerate(issues)])
        
        summary = analysis_data.get("summary", {})
        
        prompt = f"""Analyze these API performance bottlenecks and provide detailed recommendations:

📊 DETECTED ISSUES:
{issues_text}

📈 OVERALL STATISTICS:
- Total logs analyzed: {analysis_data.get('total_logs_analyzed', 0)}
- Unique endpoints: {analysis_data.get('unique_endpoints', 0)}
- Slow endpoints: {summary.get('slow_endpoints_count', 0)}
- High error rate endpoints: {summary.get('high_error_endpoints_count', 0)}
- DB-heavy endpoints: {summary.get('db_heavy_endpoints_count', 0)}

Please provide:

1. **ROOT CAUSE ANALYSIS**: What's likely causing each bottleneck?

2. **IMMEDIATE FIXES** (Quick wins):
   - Caching strategies
   - Index recommendations
   - Query optimization tips

3. **CODE-LEVEL SUGGESTIONS**:
   - Example code snippets for optimization
   - Specific database index recommendations
   - API design improvements

4. **ARCHITECTURE RECOMMENDATIONS**:
   - Should any endpoints be async?
   - Microservice decomposition suggestions
   - Load balancing considerations

5. **MONITORING IMPROVEMENTS**:
   - What additional metrics to track
   - Alert thresholds to set

Format your response in clear sections with actionable items."""
        
        return prompt
