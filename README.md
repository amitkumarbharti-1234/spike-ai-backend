# Spike AI Backend

A Tier-3 multi-agent analytics backend built for the Spike AI BuildX Hackathon.

## What it does
- Accepts natural language queries
- Routes queries using an Orchestrator
- GA4 Agent converts queries into Google Analytics insights
- SEO Agent (ready) supports crawl-based analysis
- Gracefully handles AI infrastructure failures

## Example Query
```json
{
  "query": "users last 7 days",
  "propertyId": "516920629"
}
