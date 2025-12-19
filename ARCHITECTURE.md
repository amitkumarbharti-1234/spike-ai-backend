
Paste this:

```markdown
# System Architecture

## Tier Level
Tier 3 (Production-Oriented)

## Components

### FastAPI
- Exposes /query endpoint
- Handles validation

### Orchestrator
- Detects intent
- Routes queries to agents

### GA4 Agent
- Uses LLM for query planning
- Enforces GA4 API rules
- Gracefully disables if LLM unavailable

### SEO Agent
- Uses crawl data (Screaming Frog)
- Rule-based SEO insights

### LLM Layer
- Abstracted via LiteLLM
- Optional dependency

## Design Philosophy
- Stability over blind AI
- Clear failure handling
- No crashes, no fake data
