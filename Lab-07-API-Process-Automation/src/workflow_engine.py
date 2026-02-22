"""
Lab 07 — API-Driven Process Automation
Core workflow engine: validate → enrich → notify for each task type.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path

from models import TaskRequest, TaskResponse, TaskStatus, TaskType, WorkflowStep

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "workflow.jsonl"

# Validation rules per task type
VALIDATION_RULES = {
    TaskType.INVOICE_APPROVAL: lambda p: (
        "amount" in p and float(p["amount"]) > 0,
        "amount field is required and must be positive"
    ),
    TaskType.LEAVE_REQUEST: lambda p: (
        "start_date" in p and "end_date" in p and "reason" in p,
        "start_date, end_date, and reason are required"
    ),
    TaskType.IT_SUPPORT: lambda p: (
        "issue_description" in p and len(p.get("issue_description", "")) >= 10,
        "issue_description must be at least 10 characters"
    ),
    TaskType.PURCHASE_ORDER: lambda p: (
        "item" in p and "quantity" in p and int(p.get("quantity", 0)) > 0,
        "item and quantity (> 0) are required"
    ),
}

# Enrichment logic — adds derived fields to result
ENRICHMENT = {
    TaskType.INVOICE_APPROVAL: lambda p: {
        **p,
        "approval_tier": "auto" if float(p.get("amount", 0)) < 1000 else "manager",
        "reference": f"INV-{uuid.uuid4().hex[:8].upper()}",
    },
    TaskType.LEAVE_REQUEST: lambda p: {
        **p,
        "hr_reference": f"LV-{uuid.uuid4().hex[:6].upper()}",
        "manager_notified": True,
    },
    TaskType.IT_SUPPORT: lambda p: {
        **p,
        "ticket_id": f"IT-{uuid.uuid4().hex[:6].upper()}",
        "priority_label": "P1" if "urgent" in p.get("issue_description", "").lower() else "P3",
    },
    TaskType.PURCHASE_ORDER: lambda p: {
        **p,
        "po_number": f"PO-{uuid.uuid4().hex[:8].upper()}",
        "estimated_delivery": "3-5 business days",
    },
}


def _add_step(steps: list, step_name: str, status: str, details: str = "") -> None:
    steps.append(WorkflowStep(
        step=step_name,
        status=status,
        timestamp=datetime.utcnow(),
        details=details,
    ))


def _log_task(task: TaskResponse) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(task.model_dump_json() + "\n")


def process_task(request: TaskRequest) -> TaskResponse:
    """
    Execute the full workflow pipeline for a task:
      1. Validate request fields
      2. Enrich with derived data
      3. Notify (simulated)
    """
    task_id = f"TASK-{uuid.uuid4().hex[:10].upper()}"
    steps: list[WorkflowStep] = []
    now = datetime.utcnow()

    response = TaskResponse(
        task_id=task_id,
        task_type=request.task_type,
        status=TaskStatus.PENDING,
        requester=request.requester,
        priority=request.priority,
        submitted_at=now,
        workflow_steps=steps,
    )

    # Step 1: Validate
    response.status = TaskStatus.VALIDATING
    validator = VALIDATION_RULES.get(request.task_type)
    if validator:
        valid, msg = validator(request.payload)
        if not valid:
            _add_step(steps, "validation", "failed", msg)
            response.status = TaskStatus.REJECTED
            response.error = f"Validation failed: {msg}"
            response.completed_at = datetime.utcnow()
            _log_task(response)
            return response
    _add_step(steps, "validation", "passed")

    # Step 2: Enrich
    response.status = TaskStatus.ENRICHING
    enricher = ENRICHMENT.get(request.task_type, lambda p: p)
    enriched_payload = enricher(request.payload)
    _add_step(steps, "enrichment", "completed", f"Added {len(enriched_payload) - len(request.payload)} field(s)")

    # Step 3: Notify (simulated)
    response.status = TaskStatus.NOTIFYING
    time.sleep(0.05)  # Simulate async notification
    _add_step(steps, "notification", "sent",
              f"Stakeholders notified for {request.task_type.value}")

    # Complete
    response.status = TaskStatus.COMPLETED
    response.result = enriched_payload
    response.completed_at = datetime.utcnow()
    _log_task(response)
    return response
