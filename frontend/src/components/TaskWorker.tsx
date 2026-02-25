import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  ArrowLeft,
  Check,
  CheckCircle2,
  CheckSquare,
  Loader2,
  Map,
  RotateCcw,
  Save,
  Sparkles,
  Square,
  Trash2,
  Upload,
} from "lucide-react";
import { useState } from "react";
import { completeTask, generateFieldText, reopenTask, saveTask } from "../api/client";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";
import type {
  FormField,
  ProcessTemplate,
  Project,
  TaskInstance,
  TaskTemplate,
} from "../types";
import DocumentUpload from "./DocumentUpload";
import MapPanel from "./MapPanel";

interface Props {
  project: Project;
  template: ProcessTemplate;
  stageIndex: number;
  taskInstance: TaskInstance;
  taskTemplate: TaskTemplate;
  sectionId?: string;
  onClose: () => void;
}

// Tasks that benefit from the map view
const MAP_TASKS = new Set(["s2_t1", "s2_t2", "s2_t3", "s3_t1", "s1_t3"]);

export default function TaskWorker({
  project,
  template,
  stageIndex,
  taskInstance,
  taskTemplate,
  sectionId,
  onClose,
}: Props) {
  const queryClient = useQueryClient();
  const t = useT();
  const language = useWorkflowStore((s) => s.language);
  const [formData, setFormData] = useState<Record<string, string>>(
    taskInstance.form_data
  );
  const [checklist, setChecklist] = useState<number[]>(
    taskInstance.completed_checklist
  );
  const [loadingField, setLoadingField] = useState<string | null>(null);
  const [showMap, setShowMap] = useState(false);
  const [showUploads, setShowUploads] = useState<Record<string, boolean>>({});
  const [isDone, setIsDone] = useState(taskInstance.status === "done");

  const updateField = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const clearField = (name: string) => {
    setFormData((prev) => ({ ...prev, [name]: "" }));
  };

  const toggleChecklistItem = (idx: number) => {
    setChecklist((prev) =>
      prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]
    );
  };

  const handleAIGenerate = async (field: FormField) => {
    setLoadingField(field.name);
    try {
      const res = await generateFieldText(
        taskInstance.id,
        project.id,
        field.name,
        field.label,
        language
      );
      updateField(field.name, res.text);
    } catch {
      // silently fail for MVP
    } finally {
      setLoadingField(null);
    }
  };

  const saveMutation = useMutation({
    mutationFn: () =>
      saveTask(taskInstance.id, project.id, formData, checklist, language, sectionId),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["workflow", project.id] }),
  });

  const completeMutation = useMutation({
    mutationFn: () =>
      completeTask(taskInstance.id, project.id, formData, checklist, language, sectionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflow", project.id] });
      setIsDone(true);
    },
  });

  const reopenMutation = useMutation({
    mutationFn: () => reopenTask(taskInstance.id, project.id, language),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflow", project.id] });
      setIsDone(false);
    },
  });

  const checklistComplete =
    taskTemplate.checklist.length === 0 ||
    checklist.length === taskTemplate.checklist.length;

  const formFieldsFilled =
    taskTemplate.form_fields.length === 0 ||
    taskTemplate.form_fields.every(
      (f) => (formData[f.name] ?? "").trim() !== ""
    );

  const canComplete = checklistComplete && formFieldsFilled;

  // Collect previous stage context
  const currentSection = sectionId
    ? project.sections.find((s) => s.id === sectionId)
    : undefined;
  const sectionStages = currentSection?.stages ?? project.stages;
  const prevStages = sectionStages.slice(0, stageIndex);
  const prevEntries: { stageTitle: string; taskTitle: string; label: string; value: string }[] = [];
  prevStages.forEach((ps, psIdx) => {
    const psTpl = template.stages[psIdx];
    if (!psTpl) return;
    ps.tasks.forEach((pt) => {
      const ptTpl = psTpl.tasks.find((t) => t.id === pt.template_id);
      if (!ptTpl) return;
      Object.entries(pt.form_data).forEach(([key, val]) => {
        if (!val) return;
        const fieldTpl = ptTpl.form_fields.find((f) => f.name === key);
        prevEntries.push({
          stageTitle: psTpl.title,
          taskTitle: ptTpl.title,
          label: fieldTpl?.label ?? key,
          value: val,
        });
      });
    });
  });

  const showMapForTask = MAP_TASKS.has(taskTemplate.id);

  return (
    <div className="mx-auto max-w-3xl">
      <button
        onClick={onClose}
        className="-ml-2 mb-4 flex items-center gap-1.5 rounded-lg px-2 py-2 text-sm text-gray-500 hover:bg-gray-100 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" />
        {t("task.backToOverview")}
      </button>

      <div className="rounded-xl border border-gray-200 bg-white shadow-sm">
        <div className="border-b border-gray-100 p-4 sm:p-6">
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-gray-900 sm:text-xl">
              {taskTemplate.title}
            </h2>
            {isDone && (
              <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-medium text-emerald-700">
                {t("task.done")}
              </span>
            )}
          </div>
          <p className="mt-1 text-sm text-gray-500">
            {taskTemplate.description}
          </p>
          {/* Action buttons in header */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            {isDone && (
              <button
                onClick={() => reopenMutation.mutate()}
                disabled={reopenMutation.isPending}
                className="flex items-center gap-1.5 rounded-lg border border-amber-300 bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-700 transition hover:bg-amber-100"
              >
                {reopenMutation.isPending ? (
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <RotateCcw className="h-3.5 w-3.5" />
                )}
                {t("task.reopen")}
              </button>
            )}
            {showMapForTask && (
              <button
                onClick={() => setShowMap(!showMap)}
                className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-medium transition ${
                  showMap
                    ? "border-blue-300 bg-blue-50 text-blue-700"
                    : "border-gray-300 bg-white text-gray-600 hover:bg-gray-50"
                }`}
              >
                <Map className="h-3.5 w-3.5" />
                {t("task.map")} {showMap ? t("task.hide") : t("task.show")}
              </button>
            )}
          </div>
        </div>

        <div className="p-4 sm:p-6">
          {/* Map panel */}
          {showMap && showMapForTask && (
            <div className="mb-6 h-[250px] sm:h-[350px]">
              <MapPanel
                project={project}
                showLayers={{
                  corridor: true,
                  ffh: taskTemplate.id !== "s1_t3",
                  wald: ["s2_t2", "s3_t1", "s2_t3"].includes(taskTemplate.id),
                  wsg: ["s2_t2", "s2_t3"].includes(taskTemplate.id),
                  parcels: ["s2_t2", "s1_t3", "s2_t1"].includes(taskTemplate.id),
                  railway: ["s2_t1", "s2_t2"].includes(taskTemplate.id),
                  settlements: ["s2_t1", "s2_t2"].includes(taskTemplate.id),
                }}
              />
              {/* Map legend */}
              <div className="mt-2 flex flex-wrap gap-3 text-[10px] text-gray-500">
                <span className="flex items-center gap-1">
                  <span className="inline-block h-0.5 w-4 bg-blue-600" style={{ borderTop: "2px dashed #2563eb" }} />
                  {t("task.corridorB")}
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-0.5 w-4 bg-gray-400" style={{ borderTop: "1px dashed #9ca3af" }} />
                  {t("task.corridorA")}
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-2.5 w-2.5 rounded-sm bg-green-500/30 border border-green-600" />
                  {t("task.ffh")}
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-2.5 w-2.5 rounded-sm bg-green-800/20 border border-green-800" />
                  {t("task.forest")}
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-2.5 w-2.5 rounded-sm bg-blue-500/20 border border-blue-600" />
                  {t("task.wpa")}
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-0.5 w-4 bg-stone-500" style={{ borderTop: "2px dotted #78716c" }} />
                  {t("task.railway")}
                </span>
              </div>
            </div>
          )}

          {/* Previous context for this task */}
          {prevEntries.length > 0 && (
            <div className="mb-6 rounded-lg border border-blue-100 bg-blue-50/50 p-4">
              <p className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-600">
                <CheckCircle2 className="h-3.5 w-3.5" />
                {t("task.previousContext")}
              </p>
              <div className="max-h-60 overflow-y-auto space-y-1 sm:max-h-80">
                {prevEntries.map((e, i) => (
                  <p key={i} className="text-xs text-blue-800">
                    <span className="font-medium">{e.label}:</span>{" "}
                    {e.value}
                  </p>
                ))}
              </div>
            </div>
          )}

          {/* Form fields */}
          {taskTemplate.form_fields.length > 0 && (
            <div className="space-y-4">
              {taskTemplate.form_fields.map((field) => {
                const isFieldLoading = loadingField === field.name;
                const showAI = field.type !== "date";
                const fieldValue = formData[field.name] ?? "";

                return (
                  <div key={field.name}>
                    <div className="mb-1 flex items-center justify-between">
                      <label className="text-sm font-medium text-gray-700">
                        {field.label}
                      </label>
                      <div className="flex items-center gap-1">
                        {/* Clear field button */}
                        {fieldValue && !isDone && (
                          <button
                            onClick={() => clearField(field.name)}
                            className="flex items-center gap-1 rounded-md px-2 py-1 text-xs text-gray-400 transition hover:bg-red-50 hover:text-red-500"
                            title={t("task.clearField")}
                          >
                            <Trash2 className="h-3 w-3" />
                          </button>
                        )}
                        {showAI && (
                          <button
                            onClick={() => handleAIGenerate(field)}
                            disabled={isFieldLoading || isDone}
                            className="flex items-center gap-1 rounded-md bg-violet-50 px-2.5 py-1 text-xs font-medium text-violet-700 transition hover:bg-violet-100 disabled:opacity-40"
                          >
                            {isFieldLoading ? (
                              <Loader2 className="h-3.5 w-3.5 animate-spin" />
                            ) : (
                              <Sparkles className="h-3.5 w-3.5" />
                            )}
                            {t("task.ai")}
                          </button>
                        )}
                      </div>
                    </div>
                    {field.type === "textarea" ? (
                      <textarea
                        rows={4}
                        value={fieldValue}
                        onChange={(e) => updateField(field.name, e.target.value)}
                        disabled={isDone}
                        className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm transition focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
                      />
                    ) : (
                      <input
                        type={field.type}
                        value={fieldValue}
                        onChange={(e) => updateField(field.name, e.target.value)}
                        disabled={isDone}
                        className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm transition focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500"
                      />
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* Checklist */}
          {taskTemplate.checklist.length > 0 && (
            <div className="mt-6">
              <h3 className="mb-3 text-sm font-semibold text-gray-700">
                {t("task.checklist")}
              </h3>
              <div className="space-y-2">
                {taskTemplate.checklist.map((item, idx) => {
                  const checked = checklist.includes(idx);
                  const uploadKey = `checklist-${item}`;
                  const isUploadOpen = showUploads[uploadKey] ?? false;
                  return (
                    <div key={item}>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => !isDone && toggleChecklistItem(idx)}
                          disabled={isDone}
                          className="flex flex-1 items-center gap-3 rounded-lg border border-gray-100 px-3 py-2.5 text-left transition hover:bg-gray-50 disabled:cursor-default"
                        >
                          {checked ? (
                            <CheckSquare className="h-5 w-5 shrink-0 text-emerald-500" />
                          ) : (
                            <Square className="h-5 w-5 shrink-0 text-gray-300" />
                          )}
                          <span
                            className={`text-sm ${
                              checked
                                ? "text-gray-400 line-through"
                                : "text-gray-700"
                            }`}
                          >
                            {item}
                          </span>
                        </button>
                        <button
                          onClick={() =>
                            setShowUploads((prev) => ({
                              ...prev,
                              [uploadKey]: !prev[uploadKey],
                            }))
                          }
                          className={`shrink-0 rounded-lg border p-2 text-xs transition ${
                            isUploadOpen
                              ? "border-blue-300 bg-blue-50 text-blue-600"
                              : "border-gray-200 text-gray-400 hover:bg-gray-50 hover:text-gray-600"
                          }`}
                          title={t("task.attachDocument")}
                        >
                          <Upload className="h-4 w-4" />
                        </button>
                      </div>
                      {isUploadOpen && (
                        <div className="ml-8 mt-2">
                          <DocumentUpload
                            taskId={taskInstance.id}
                            linkedItem={item}
                            disabled={isDone}
                          />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* General document upload */}
          <div className="mt-6">
            <h3 className="mb-3 text-sm font-semibold text-gray-700">
              {t("task.documents")}
            </h3>
            <DocumentUpload taskId={taskInstance.id} disabled={isDone} />
          </div>
        </div>

        {/* Footer */}
        {!isDone && (
          <div className="flex flex-col-reverse gap-3 border-t border-gray-100 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-6">
            <button
              onClick={() => saveMutation.mutate()}
              disabled={saveMutation.isPending}
              className="flex w-full items-center justify-center gap-2 rounded-lg border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 transition hover:bg-gray-50 disabled:opacity-50 sm:w-auto sm:justify-start sm:py-2"
            >
              {saveMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Save className="h-4 w-4" />
              )}
              {t("task.save")}
            </button>
            <button
              onClick={() => completeMutation.mutate()}
              disabled={!canComplete || completeMutation.isPending}
              title={
                !canComplete
                  ? t("task.fillAllFields")
                  : undefined
              }
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:justify-start sm:py-2"
            >
              {completeMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Check className="h-4 w-4" />
              )}
              {t("task.markComplete")}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
