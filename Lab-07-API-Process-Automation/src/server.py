"""
Lab 07 — API-Driven Process Automation
FastAPI server exposing the workflow engine as a REST API.

Endpoints:
  POST /tasks           — Submit a task
  GET  /tasks/{task_id} — Get task status
  GET  /tasks           — List all tasks (in-memory)
  GET  /health          — Health check

Usage:
    uvicorn server:app --reload --port 8007
"""

from collections import OrderedDict
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from models import TaskRequest, TaskResponse, TaskStatus
from workflow_engine import process_task

app = FastAPI(
    title="Intelligent Automation — Workflow API",
    description="Lab 07: BPM workflow automation via REST API",
    version="1.0.0",
)

# In-memory task store (keyed by task_id, capped at 500 entries)
_task_store: OrderedDict[str, TaskResponse] = OrderedDict()
MAX_TASKS = 500


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat(), "tasks_in_store": len(_task_store)}


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def submit_task(request: TaskRequest):
    """Submit a task and immediately run it through the workflow pipeline."""
    result = process_task(request)

    # Evict oldest entry if at capacity
    if len(_task_store) >= MAX_TASKS:
        _task_store.popitem(last=False)
    _task_store[result.task_id] = result

    return result


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(status: TaskStatus | None = None, limit: int = 50):
    """List tasks, optionally filtered by status."""
    tasks = list(_task_store.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    return tasks[-limit:]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    """Get a specific task by ID."""
    task = _task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id!r} not found")
    return task


@app.get("/stats")
def get_stats():
    """Aggregate workflow statistics."""
    from collections import Counter
    statuses = Counter(t.status for t in _task_store.values())
    types = Counter(t.task_type for t in _task_store.values())
    return {
        "total_tasks": len(_task_store),
        "by_status": dict(statuses),
        "by_type": dict(types),
    }
