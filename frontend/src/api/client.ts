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

export function fetchWorkflow(projectId: string) {
  return request<WorkflowResponse>(`/project/${projectId}/workflow`);
}

export function fetchProjects() {
  return request<Project[]>("/projects");
}

export function completeTask(
  taskId: string,
  projectId: string,
  formData: Record<string, string>,
  completedChecklist: string[]
) {
  return request<{ status: string; project: Project }>(
    `/task/${taskId}/complete?project_id=${projectId}`,
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
  completedChecklist: string[]
) {
  return request<{ status: string }>(
    `/task/${taskId}/save?project_id=${projectId}`,
    {
      method: "POST",
      body: JSON.stringify({
        form_data: formData,
        completed_checklist: completedChecklist,
      }),
    }
  );
}

export function reopenTask(taskId: string, projectId: string) {
  return request<{ status: string }>(`/task/${taskId}/reopen?project_id=${projectId}`, {
    method: "PATCH",
  });
}

export function generateFieldText(
  taskInstanceId: string,
  projectId: string,
  fieldName: string,
  fieldLabel: string
) {
  return request<AIFieldResponse>("/ai/generate-field", {
    method: "POST",
    body: JSON.stringify({
      task_instance_id: taskInstanceId,
      project_id: projectId,
      field_name: fieldName,
      field_label: fieldLabel,
    }),
  });
}
