import requests
import json

# Sample logs with performance issues
with open("sample_logs.json", "r") as f:
    sample_logs = json.load(f)

# API endpoint
url = "http://localhost:8000/analyze"

# Make request
response = requests.post(
    url,
    json={
        "logs": sample_logs,
        "use_ai": True  # Set to False to skip AI analysis
    }
)

# Print results
if response.status_code == 200:
    result = response.json()
    
    print("=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)
    
    analysis = result["analysis"]
    print(f"\n✅ Total logs analyzed: {analysis['total_logs_analyzed']}")
    print(f"✅ Unique endpoints: {analysis['unique_endpoints']}")
    
    print("\n🐌 SLOW ENDPOINTS:")
    for endpoint in analysis.get("slow_endpoints", []):
        print(f"  - {endpoint['endpoint']}")
        print(f"    Avg: {endpoint['avg_response_time_ms']}ms | P95: {endpoint['p95_response_time_ms']}ms")
    
    print("\n❌ HIGH ERROR RATE ENDPOINTS:")
    for endpoint in analysis.get("high_error_endpoints", []):
        print(f"  - {endpoint['endpoint']}")
        print(f"    Error rate: {endpoint['error_rate']*100:.1f}% ({endpoint['total_errors']} errors)")
    
    print("\n💾 DB-HEAVY ENDPOINTS:")
    for endpoint in analysis.get("db_heavy_endpoints", []):
        print(f"  - {endpoint['endpoint']}")
        print(f"    Avg queries: {endpoint['avg_db_queries']}")
    
    # AI Recommendations
    if result.get("ai_recommendations"):
        ai = result["ai_recommendations"]
        if ai.get("status") == "bottlenecks_detected":
            print("\n" + "=" * 60)
            print("🤖 AI RECOMMENDATIONS")
            print("=" * 60)
            print(ai.get("ai_analysis", ""))
        else:
            print(f"\n⚠️  AI Analysis: {ai.get('message', 'Not available')}")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
