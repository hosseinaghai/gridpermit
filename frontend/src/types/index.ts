export type TaskStatus = "pending" | "in_progress" | "done";
export type StageStatus = "pending" | "active" | "completed";
export type VerfahrensPfad = "NABEG" | "EnWG";

export interface FormField {
  name: string;
  label: string;
  type: "text" | "textarea" | "date";
}

export interface TaskTemplate {
  id: string;
  title: string;
  description: string;
  checklist: string[];
  form_fields: FormField[];
}

export interface StageTemplate {
  id: string;
  title: string;
  law_reference: string;
  description: string;
  tasks: TaskTemplate[];
  info_text: string;
}

export interface ProcessTemplate {
  pfad: VerfahrensPfad;
  label: string;
  description: string;
  stages: StageTemplate[];
}

export interface TaskInstance {
  id: string;
  template_id: string;
  status: TaskStatus;
  form_data: Record<string, string>;
  completed_checklist: number[];
  updated_at: string | null;
}

export interface StageInstance {
  id: string;
  template_id: string;
  status: StageStatus;
  tasks: TaskInstance[];
}

export interface Blocker {
  blocker_id: string;
  title: string;
  severity: string;
  owner_role: string;
}

export interface GeoLayer {
  layer_id: string;
  type: string;
  source: string;
  geometry_ref: string;
  last_update: string;
}

export interface HistoricalCase {
  case_id: string;
  title: string;
  similarity_features: Record<string, unknown>;
  outcome: string;
  key_reasons: string[];
  reusable_docs: string[];
}

export interface ProjectDocument {
  doc_id: string;
  doc_type: string;
  version: string;
  status: string;
  source: string;
  linked_stage: string;
}

export interface Risk {
  risk_id: string;
  category: string;
  probability: number;
  impact: number;
  mitigation: string;
  owner: string;
}

export interface ProjectTask {
  task_id: string;
  title: string;
  owner_role: string;
  due_date: string;
  dependencies: string[];
  done_definition: string;
}

export interface Section {
  id: string;
  name: string;
  km_start: number;
  km_end: number;
  region: string;
  stages: StageInstance[];
}

export interface PermitStatus {
  id: string;
  section_id: string;
  permit_type: string;
  label: string;
  status: string;
}

export interface EmailAction {
  action_type: string;
  label: string;
  description: string;
  confidence: number;
  document_id?: string;
  task_template_id?: string;
  stage_index?: number;
  section_id?: string;
}

export interface Project {
  id: string;
  name: string;
  pfad: VerfahrensPfad;
  kv_level: number;
  technology: string;
  routing_type: string;
  states_crossed: string[];
  length_km: number;
  is_multi_state: boolean;
  current_stage_index: number;
  stages: StageInstance[];
  blockers: Blocker[];
  geo_layers: GeoLayer[];
  historical_cases: HistoricalCase[];
  documents: ProjectDocument[];
  risks: Risk[];
  project_tasks: ProjectTask[];
  sections: Section[];
  permits: PermitStatus[];
  created_at: string;
}

export interface WorkflowResponse {
  project: Project;
  template: ProcessTemplate;
}

export interface AIFieldResponse {
  text: string;
}
