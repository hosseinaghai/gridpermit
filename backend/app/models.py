from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --- Enums ---

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class StageStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class VerfahrensPfad(str, Enum):
    NABEG = "NABEG"
    ENWG = "EnWG"


# --- Template models (static definitions) ---

class FormField(BaseModel):
    name: str
    label: str
    type: str = "text"  # text, textarea, date


class TaskTemplate(BaseModel):
    id: str
    title: str
    description: str
    checklist: list[str] = Field(default_factory=list)
    form_fields: list[FormField] = Field(default_factory=list)


class StageTemplate(BaseModel):
    id: str
    title: str
    law_reference: str
    description: str
    tasks: list[TaskTemplate]
    info_text: str = ""


class ProcessTemplate(BaseModel):
    pfad: VerfahrensPfad
    label: str
    description: str
    stages: list[StageTemplate]


# --- Runtime models (project instances) ---

class TaskInstance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: str
    status: TaskStatus = TaskStatus.PENDING
    form_data: dict = Field(default_factory=dict)
    completed_checklist: list[str] = Field(default_factory=list)
    updated_at: Optional[datetime] = None


class StageInstance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: str
    status: StageStatus = StageStatus.PENDING
    tasks: list[TaskInstance]


# --- Rich project context models ---

class Blocker(BaseModel):
    blocker_id: str
    title: str
    severity: str
    owner_role: str


class GeoLayer(BaseModel):
    layer_id: str
    type: str
    source: str
    geometry_ref: str
    last_update: str


class LandParcel(BaseModel):
    parcel_id: str
    owner_type: str
    rights_status: str
    contact_ref: str


class Stakeholder(BaseModel):
    stakeholder_id: str
    type: str
    name: str
    preferred_channel: str


class SimilarityFeatures(BaseModel):
    routing_type: str = ""
    forest_crossing: Optional[bool] = None
    ffh_overlap: Optional[bool] = None
    state: str = ""
    settlement_distance_m: Optional[int] = None
    wsg_overlap: Optional[bool] = None


class HistoricalCase(BaseModel):
    case_id: str
    title: str
    similarity_features: SimilarityFeatures
    outcome: str
    key_reasons: list[str]
    reusable_docs: list[str]


class ProjectDocument(BaseModel):
    doc_id: str
    doc_type: str
    version: str
    status: str
    source: str
    linked_stage: str


class ProjectTask(BaseModel):
    task_id: str
    title: str
    owner_role: str
    due_date: str
    dependencies: list[str]
    done_definition: str


class Risk(BaseModel):
    risk_id: str
    category: str
    probability: float
    impact: float
    mitigation: str
    owner: str


class RegulatoryRequirement(BaseModel):
    requirement_id: str
    legal_basis: str
    trigger_condition: str
    required_artifacts: list[str]
    authority: str


class DraftTemplate(BaseModel):
    template_id: str
    output_type: str
    applicable_stage: str
    placeholders: list[str]


# --- Project (with full context) ---

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    pfad: VerfahrensPfad
    kv_level: int
    technology: str = ""
    routing_type: str = ""
    states_crossed: list[str] = Field(default_factory=list)
    length_km: float = 0
    is_cross_border: bool = False
    is_multi_state: bool = False
    current_stage_index: int = 0
    stages: list[StageInstance] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    geo_layers: list[GeoLayer] = Field(default_factory=list)
    land_parcels: list[LandParcel] = Field(default_factory=list)
    stakeholders: list[Stakeholder] = Field(default_factory=list)
    historical_cases: list[HistoricalCase] = Field(default_factory=list)
    documents: list[ProjectDocument] = Field(default_factory=list)
    project_tasks: list[ProjectTask] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    regulatory_requirements: list[RegulatoryRequirement] = Field(default_factory=list)
    draft_templates: list[DraftTemplate] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


# --- API schemas ---

class ProjectCreateRequest(BaseModel):
    name: str
    kv_level: int


class TaskCompleteRequest(BaseModel):
    form_data: dict = Field(default_factory=dict)
    completed_checklist: list[str] = Field(default_factory=list)


class AIFieldRequest(BaseModel):
    project_id: str
    task_instance_id: str
    field_name: str
    field_label: str


class AIFieldResponse(BaseModel):
    text: str


class WorkflowResponse(BaseModel):
    project: Project
    template: ProcessTemplate
