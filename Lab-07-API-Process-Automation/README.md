# Lab 07 — API-Driven Process Automation

**Pillar:** BPM (Business Process Management)  
**Difficulty:** Intermediate  
**Estimated Time:** 60–90 minutes

---

## Objective

Build a lightweight workflow automation system with:
- A **FastAPI server** that accepts task requests and routes them through a 3-step workflow (validate → enrich → notify)
- A **client script** that automatically submits tasks on a schedule
- Full **audit logging** of every workflow execution to JSONL
- A **stats endpoint** showing real-time task counts by status and type

This demonstrates **BPM** — orchestrating business processes through an API-driven workflow engine.

---

## Concepts Covered

| Concept | Description |
|---------|-------------|
| REST API design | FastAPI endpoints with Pydantic schemas |
| Workflow orchestration | Multi-step validation/enrichment pipeline |
| Task routing | Type-specific logic per task (invoice, leave, IT, PO) |
| Process logging | Timestamped JSONL audit trail per task |
| Automated client | Scheduled task submission with `httpx` |

---

## Project Structure

```
Lab-07-API-Process-Automation/
├── README.md
├── requirements.txt
├── src/
│   ├── models.py            # Pydantic schemas (TaskRequest, TaskResponse, etc.)
│   ├── workflow_engine.py   # 3-step pipeline: validate → enrich → notify
│   ├── server.py            # FastAPI REST API
│   └── client.py            # Automated task submission client
└── logs/
    └── workflow.jsonl       # Append-only audit log
```

---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Step 1: Start the server

```bash
cd src
uvicorn server:app --reload --port 8007
```

The API will be live at `http://localhost:8007`.  
Interactive docs: `http://localhost:8007/docs`

### Step 2: Run the automated client

In a second terminal:

```bash
cd src
python client.py                  # Submit batches every 10 seconds
python client.py --once           # Submit one batch and exit
python client.py --interval 5 --batch-size 5
```

### Step 3: Inspect the API manually

```bash
# Check health
curl http://localhost:8007/health

# Submit a task manually
curl -X POST http://localhost:8007/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "invoice_approval",
    "requester": "alice@company.com",
    "payload": {"vendor": "Acme Corp", "amount": 1500.00},
    "priority": 2
  }'

# View stats
curl http://localhost:8007/stats
```

---

## Workflow Steps

```
Client Request (TaskRequest)
        │
        ▼ [Step 1: Validate]
  Check required fields per task type
  → REJECTED if invalid
        │
        ▼ [Step 2: Enrich]
  Add derived fields (reference IDs, approval tier, ticket numbers...)
        │
        ▼ [Step 3: Notify]
  Simulate stakeholder notification
        │
        ▼ TaskResponse (COMPLETED / REJECTED)
  Append to logs/workflow.jsonl
```

## Task Types & Validation Rules

| Task Type | Required Fields | Enrichment |
|-----------|----------------|-----------|
| `invoice_approval` | `amount` (> 0) | `approval_tier`, `reference` |
| `leave_request` | `start_date`, `end_date`, `reason` | `hr_reference`, `manager_notified` |
| `it_support` | `issue_description` (≥ 10 chars) | `ticket_id`, `priority_label` |
| `purchase_order` | `item`, `quantity` (> 0) | `po_number`, `estimated_delivery` |

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health check |
| POST | `/tasks` | Submit a new task |
| GET | `/tasks` | List tasks (filter by `?status=`) |
| GET | `/tasks/{task_id}` | Get task by ID |
| GET | `/stats` | Aggregate counts |

---

## Extension Challenge

1. Add a **priority queue** so P1 tasks are processed before P3
2. Persist tasks to **SQLite** using SQLAlchemy instead of in-memory store
3. Add a **webhook** callback URL to `TaskRequest` and POST the result when complete
