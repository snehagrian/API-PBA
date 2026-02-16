import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIAnalyzer:
    """OpenAI integration for bottleneck analysis"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
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
        
        # Build prompt for OpenAI
        prompt = self._build_analysis_prompt(issues, analysis_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
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
            
            ai_analysis = response.choices[0].message.content
            
            return {
                "status": "bottlenecks_detected",
                "ai_analysis": ai_analysis,
                "issues_analyzed": len(issues),
                "raw_issues": issues
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to get AI analysis"
            }
    
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
