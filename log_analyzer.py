from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict, Counter


class LogAnalyzer:
    """Analyzes API logs to detect performance bottlenecks"""
    
    def __init__(self, slow_threshold_ms: int = 500, error_rate_threshold: float = 0.05):
        self.slow_threshold_ms = slow_threshold_ms
        self.error_rate_threshold = error_rate_threshold
    
    def analyze_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze API logs and detect bottlenecks
        
        Args:
            logs: List of log entries with fields like endpoint, response_time, status_code, etc.
        
        Returns:
            Dictionary containing analysis results
        """
        if not logs:
            return {"error": "No logs provided"}
        
        # Group logs by endpoint
        endpoint_stats = defaultdict(lambda: {
            "count": 0,
            "total_response_time": 0,
            "errors": 0,
            "db_queries": 0,
            "response_times": []
        })
        
        for log in logs:
            endpoint = log.get("endpoint", "unknown")
            response_time = log.get("response_time_ms", 0)
            status_code = log.get("status_code", 200)
            db_query_count = log.get("db_query_count", 0)
            
            stats = endpoint_stats[endpoint]
            stats["count"] += 1
            stats["total_response_time"] += response_time
            stats["response_times"].append(response_time)
            stats["db_queries"] += db_query_count
            
            if status_code >= 400:
                stats["errors"] += 1
        
        # Analyze each endpoint
        slow_endpoints = []
        high_error_endpoints = []
        db_heavy_endpoints = []
        
        for endpoint, stats in endpoint_stats.items():
            avg_response_time = stats["total_response_time"] / stats["count"]
            error_rate = stats["errors"] / stats["count"]
            avg_db_queries = stats["db_queries"] / stats["count"]
            
            # P95 calculation
            sorted_times = sorted(stats["response_times"])
            p95_index = int(len(sorted_times) * 0.95)
            p95_response_time = sorted_times[p95_index] if sorted_times else 0
            
            endpoint_analysis = {
                "endpoint": endpoint,
                "total_requests": stats["count"],
                "avg_response_time_ms": round(avg_response_time, 2),
                "p95_response_time_ms": round(p95_response_time, 2),
                "error_rate": round(error_rate, 3),
                "avg_db_queries": round(avg_db_queries, 2),
                "total_errors": stats["errors"]
            }
            
            # Detect bottlenecks
            if avg_response_time > self.slow_threshold_ms:
                slow_endpoints.append(endpoint_analysis)
            
            if error_rate > self.error_rate_threshold:
                high_error_endpoints.append(endpoint_analysis)
            
            if avg_db_queries > 5:  # More than 5 queries on average
                db_heavy_endpoints.append(endpoint_analysis)
        
        # Sort by severity
        slow_endpoints.sort(key=lambda x: x["avg_response_time_ms"], reverse=True)
        high_error_endpoints.sort(key=lambda x: x["error_rate"], reverse=True)
        db_heavy_endpoints.sort(key=lambda x: x["avg_db_queries"], reverse=True)
        
        return {
            "total_logs_analyzed": len(logs),
            "unique_endpoints": len(endpoint_stats),
            "slow_endpoints": slow_endpoints[:5],  # Top 5
            "high_error_endpoints": high_error_endpoints[:5],
            "db_heavy_endpoints": db_heavy_endpoints[:5],
            "summary": {
                "slow_endpoints_count": len(slow_endpoints),
                "high_error_endpoints_count": len(high_error_endpoints),
                "db_heavy_endpoints_count": len(db_heavy_endpoints)
            }
        }
    
    def get_critical_issues(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract critical issues for AI analysis"""
        issues = []
        
        for endpoint in analysis.get("slow_endpoints", [])[:3]:
            issues.append(
                f"Slow endpoint: {endpoint['endpoint']} - "
                f"Avg: {endpoint['avg_response_time_ms']}ms, "
                f"P95: {endpoint['p95_response_time_ms']}ms, "
                f"DB Queries: {endpoint['avg_db_queries']}"
            )
        
        for endpoint in analysis.get("high_error_endpoints", [])[:3]:
            issues.append(
                f"High error rate: {endpoint['endpoint']} - "
                f"Error rate: {endpoint['error_rate']*100:.1f}%, "
                f"Total errors: {endpoint['total_errors']}"
            )
        
        for endpoint in analysis.get("db_heavy_endpoints", [])[:3]:
            issues.append(
                f"DB-heavy endpoint: {endpoint['endpoint']} - "
                f"Avg {endpoint['avg_db_queries']} queries per request"
            )
        
        return issues
