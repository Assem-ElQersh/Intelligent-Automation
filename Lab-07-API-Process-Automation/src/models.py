"""
Lab 07 — API-Driven Process Automation
Pydantic models for request/response schemas.
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    INVOICE_APPROVAL = "invoice_approval"
    LEAVE_REQUEST = "leave_request"
    IT_SUPPORT = "it_support"
    PURCHASE_ORDER = "purchase_order"


class TaskStatus(str, Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    ENRICHING = "enriching"
    NOTIFYING = "notifying"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


class TaskRequest(BaseModel):
    task_type: TaskType
    requester: str = Field(..., min_length=2, max_length=100)
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=3, ge=1, le=5, description="1=critical, 5=low")


class WorkflowStep(BaseModel):
    step: str
    status: str
    timestamp: datetime
    details: str = ""


class TaskResponse(BaseModel):
    task_id: str
    task_type: TaskType
    status: TaskStatus
    requester: str
    priority: int
    submitted_at: datetime
    completed_at: datetime | None = None
    workflow_steps: list[WorkflowStep] = []
    result: dict[str, Any] | None = None
    error: str | None = None
