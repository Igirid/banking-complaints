Build a separate frontend microservice for a banking complaints intelligence platform.

Project goal:
Create a React + Next.js + TypeScript dashboard that consumes the backend complaint intelligence API and lets bank analysts monitor complaint trends, issue clusters, and ranked priorities in real time.

Requirements:

- Use Next.js or Vite React app with TypeScript
- Use Tailwind CSS or a similar utility-first UI framework
- Create a secure, multi-tenant dashboard UI for banking clients
- Show summary KPIs such as:
  - total complaints
  - complaint velocity
  - top issue cluster
  - high-priority items
  - sentiment trend
  - regional distribution
- Provide views for:
  - overview dashboard
  - issue list
  - complaint detail drilldown
  - metric configuration panel
  - alert list
  - product or channel filter
- Add a ranking table where issues can be sorted by:
  - severity
  - sentiment risk
  - volume
  - trend
  - regulatory risk
  - custom user metric
- Include a chart panel using Recharts or ECharts
- Support dark mode and responsive layout
- Provide login screen and auth guard placeholders
- Communicate with backend via an API client layer
- Use environment variables for backend URL and auth config
- Document how to run the frontend microservice and how it connects to the backend

API contract assumptions:

- Base URL is provided via environment variable
- Endpoints include:
  - GET /health
  - POST /insights/rank
  - GET /insights/trends
  - GET /insights/issues
  - GET /insights/alerts
- Use JSON responses and typed frontend models

Deliverables:

- app structure with pages or routes
- components for cards, charts, tables, filters, and detail views
- reusable API client
- README for local installation and run instructions
- basic tests for key UI components and API contract handling

Acceptance criteria:

- The app starts locally without errors
- The dashboard renders mock or live complaint data
- Users can change the metric weighting and see ranking changes
- The UI is separate from backend and can be deployed independently
- The design is production-ready and cleanly separated from the API service

Important:
This is a separate microservice from the backend. Keep the frontend decoupled from the backend logic and use explicit API contracts only.
