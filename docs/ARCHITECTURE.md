# Architecture

FastAPI → LangGraph intake → synthetic FHIR patient lookup → fictional policy lookup → rule engine → packet assembly → mandatory clinician interrupt → simulated payer submission.

MCP server exports synthetic lookup tools independently; the graph currently calls fixture functions directly.

SQLite stores request statuses and metadata audit logs. MemorySaver checkpoints are not durable.

Security limitations: demo header key is not RBAC, identity verification, or tenant isolation. No real PHI, real insurer integration, BAA, HIPAA compliance certification, production encryption, or clinical validation. Use for learning only.
