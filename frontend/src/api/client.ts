import type { Language } from "../i18n/translations";
import type { AIFieldResponse, Project, WorkflowResponse } from "../types";

const BASE = "/api";

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed: ${res.status}`);
  }
  return res.json();
}

export function fetchWorkflow(projectId: string, lang: Language = "de") {
  return request<WorkflowResponse>(`/project/${projectId}/workflow?lang=${lang}`);
}

export function fetchProjects() {
  return request<Project[]>("/projects");
}

export function completeTask(
  taskId: string,
  projectId: string,
  formData: Record<string, string>,
  completedChecklist: number[],
  lang: Language = "de"
) {
  return request<{ status: string; project: Project }>(
    `/task/${taskId}/complete?project_id=${projectId}&lang=${lang}`,
    {
      method: "POST",
      body: JSON.stringify({
        form_data: formData,
        completed_checklist: completedChecklist,
      }),
    }
  );
}

export function saveTask(
  taskId: string,
  projectId: string,
  formData: Record<string, string>,
  completedChecklist: number[],
  lang: Language = "de"
) {
  return request<{ status: string }>(
    `/task/${taskId}/save?project_id=${projectId}&lang=${lang}`,
    {
      method: "POST",
      body: JSON.stringify({
        form_data: formData,
        completed_checklist: completedChecklist,
      }),
    }
  );
}

export function reopenTask(taskId: string, projectId: string, lang: Language = "de") {
  return request<{ status: string }>(`/task/${taskId}/reopen?project_id=${projectId}&lang=${lang}`, {
    method: "PATCH",
  });
}

export function generateFieldText(
  taskInstanceId: string,
  projectId: string,
  fieldName: string,
  fieldLabel: string,
  lang: Language = "de"
) {
  return request<AIFieldResponse>("/ai/generate-field", {
    method: "POST",
    body: JSON.stringify({
      task_instance_id: taskInstanceId,
      project_id: projectId,
      field_name: fieldName,
      field_label: fieldLabel,
      lang,
    }),
  });
}
