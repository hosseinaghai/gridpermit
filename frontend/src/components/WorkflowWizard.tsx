import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Circle,
  Clock,
  FileEdit,
  PartyPopper,
  Trophy,
} from "lucide-react";
import { useState } from "react";
import type {
  ProcessTemplate,
  Project,
  StageInstance,
  StageTemplate,
  TaskStatus,
} from "../types";
import { useWorkflowStore } from "../store/workflowStore";
import { useT } from "../i18n/translations";
import TaskWorker from "./TaskWorker";

interface Props {
  project: Project;
  template: ProcessTemplate;
}

function daysUntil(dateStr: string): number {
  const target = new Date(dateStr);
  const now = new Date();
  return Math.ceil((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

export default function WorkflowWizard({ project, template }: Props) {
  const { selectedStageIndex, selectedSectionIndex, selectedTaskId, openTask, closeTask } =
    useWorkflowStore();
  const [prevContextOpen, setPrevContextOpen] = useState(true);
  const t = useT();

  const statusConfig: Record<
    TaskStatus,
    { icon: typeof Circle; color: string; label: string }
  > = {
    done: { icon: CheckCircle2, color: "text-emerald-500", label: t("wizard.statusDone") },
    in_progress: { icon: Clock, color: "text-amber-500", label: t("wizard.statusInProgress") },
    pending: { icon: Circle, color: "text-gray-300", label: t("wizard.statusOpen") },
  };

  const currentSection = project.sections[selectedSectionIndex];
  const sectionStages = currentSection?.stages ?? project.stages;
  const stage: StageInstance | undefined = sectionStages[selectedStageIndex];
  const stageTpl: StageTemplate | undefined = template.stages[selectedStageIndex];

  if (!stage || !stageTpl) {
    return (
      <div className="flex h-full items-center justify-center text-gray-400">
        {t("wizard.stageNotFound")}
      </div>
    );
  }

  // If a task is selected show TaskWorker
  if (selectedTaskId) {
    const taskInst = stage.tasks.find((t) => t.id === selectedTaskId);
    const taskTpl = stageTpl.tasks.find((t) => t.id === taskInst?.template_id);
    if (taskInst && taskTpl) {
      return (
        <TaskWorker
          project={project}
          template={template}
          stageIndex={selectedStageIndex}
          taskInstance={taskInst}
          taskTemplate={taskTpl}
          sectionId={currentSection?.id}
          onClose={closeTask}
        />
      );
    }
  }

  // Collect previous stage data
  const previousStages = sectionStages.slice(0, selectedStageIndex);
  const hasPreviousData = previousStages.some((s) =>
    s.tasks.some((t) => Object.keys(t.form_data).length > 0)
  );

  // Blockers for this stage
  const stageBlockers = project.blockers;

  // Overall progress
  const totalTasks = sectionStages.reduce((acc, s) => acc + s.tasks.length, 0);
  const doneTasks = sectionStages.reduce(
    (acc, s) => acc + s.tasks.filter((t) => t.status === "done").length,
    0
  );
  const overallPct = totalTasks > 0 ? Math.round((doneTasks / totalTasks) * 100) : 0;

  // Stage progress
  const stageCompleted = stage.tasks.filter((t) => t.status === "done").length;
  const stageTotal = stage.tasks.length;
  const stagePct = stageTotal > 0 ? Math.round((stageCompleted / stageTotal) * 100) : 0;
  const stageAllDone = stageCompleted === stageTotal && stageTotal > 0;

  // Deadlines
  const upcomingDeadlines = project.project_tasks
    ?.filter((t) => t.due_date)
    .map((t) => ({ ...t, daysLeft: daysUntil(t.due_date) }))
    .sort((a, b) => a.daysLeft - b.daysLeft)
    ?? [];

  return (
    <div>
      {/* Progress dashboard */}
      <div className="mb-4 grid gap-3 sm:mb-6 sm:gap-4 sm:grid-cols-3">
        {/* Overall progress */}
        <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
            {t("wizard.overallProgress")}
          </p>
          <div className="mt-2 flex items-end gap-2">
            <span className="text-2xl font-bold text-gray-900 sm:text-3xl">{overallPct}%</span>
            <span className="mb-1 text-xs text-gray-500">{doneTasks}/{totalTasks} {t("wizard.tasks")}</span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
            <div
              className="h-full rounded-full bg-gradient-to-r from-blue-500 to-emerald-500 transition-all duration-500"
              style={{ width: `${overallPct}%` }}
            />
          </div>
        </div>

        {/* Stage progress */}
        <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
            {t("wizard.currentPhase")}
          </p>
          <div className="mt-2 flex items-end gap-2">
            <span className="text-2xl font-bold text-gray-900 sm:text-3xl">{stagePct}%</span>
            <span className="mb-1 text-xs text-gray-500">
              {stageCompleted}/{stageTotal} {t("wizard.completed")}
            </span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                stageAllDone ? "bg-emerald-500" : "bg-amber-400"
              }`}
              style={{ width: `${stagePct}%` }}
            />
          </div>
        </div>

        {/* Deadlines */}
        <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
            {t("wizard.nextDeadlines")}
          </p>
          {upcomingDeadlines.length > 0 ? (
            <div className="mt-2 space-y-1.5">
              {upcomingDeadlines.map((d) => (
                <div key={d.task_id} className="flex items-center gap-2">
                  <Calendar
                    className={`h-3.5 w-3.5 shrink-0 ${
                      d.daysLeft <= 3
                        ? "text-red-500"
                        : d.daysLeft <= 7
                          ? "text-amber-500"
                          : "text-gray-400"
                    }`}
                  />
                  <span className="text-xs text-gray-700">{d.title}</span>
                  <span
                    className={`ml-auto shrink-0 rounded px-1.5 py-0.5 text-[10px] font-bold ${
                      d.daysLeft <= 3
                        ? "bg-red-100 text-red-700"
                        : d.daysLeft <= 7
                          ? "bg-amber-100 text-amber-700"
                          : "bg-gray-100 text-gray-600"
                    }`}
                  >
                    {d.daysLeft <= 0 ? t("wizard.overdue") : `${d.daysLeft}d`}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-xs text-gray-400">{t("wizard.noDeadlines")}</p>
          )}
        </div>
      </div>

      {/* Stage completion celebration */}
      {stageAllDone && (
        <div className="mb-5 flex items-center gap-3 rounded-xl border border-emerald-200 bg-gradient-to-r from-emerald-50 to-teal-50 p-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-100">
            {overallPct === 100 ? (
              <Trophy className="h-5 w-5 text-emerald-600" />
            ) : (
              <PartyPopper className="h-5 w-5 text-emerald-600" />
            )}
          </div>
          <div>
            <p className="text-sm font-bold text-emerald-800">
              {overallPct === 100
                ? t("wizard.allPhasesComplete")
                : t("wizard.phaseComplete", { title: stageTpl.title })}
            </p>
            <p className="text-xs text-emerald-600">
              {overallPct === 100
                ? t("wizard.allPhasesCongrats")
                : t("wizard.phaseCompleteNext")}
            </p>
          </div>
        </div>
      )}

      {/* Stage header */}
      <div className="mb-6">
        <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
          <span
            className={`rounded px-2 py-0.5 text-xs font-semibold ${
              stage.status === "completed"
                ? "bg-emerald-100 text-emerald-700"
                : stage.status === "active"
                  ? "bg-amber-100 text-amber-700"
                  : "bg-gray-100 text-gray-500"
            }`}
          >
            {stage.status === "completed"
              ? t("wizard.stageCompleted")
              : stage.status === "active"
                ? t("wizard.stageActive")
                : t("wizard.stagePending")}
          </span>
          <span className="rounded bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-700">
            {stageTpl.law_reference}
          </span>
          <span className="rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-500">
            {t("wizard.phase")} {selectedStageIndex + 1}/{template.stages.length}
          </span>
        </div>
        <h1 className="mt-2 text-xl font-bold text-gray-900 sm:text-2xl">
          {stageTpl.title}
        </h1>
        <p className="mt-1 text-sm text-gray-500">{stageTpl.description}</p>
      </div>

      {/* Blockers */}
      {stage.status === "active" && stageBlockers.length > 0 && (
        <div className="mb-5 space-y-2">
          {stageBlockers.map((b) => (
            <div
              key={b.blocker_id}
              className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4"
            >
              <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
              <div>
                <p className="text-sm font-semibold text-red-800">
                  {t("wizard.blocker")} {b.title}
                </p>
                <p className="text-xs text-red-600">
                  {t("wizard.severity")} {b.severity} &middot; {t("wizard.responsible")}{" "}
                  {b.owner_role}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Previous context */}
      {hasPreviousData && (
        <div className="mb-5 rounded-xl border border-gray-200 bg-white">
          <button
            onClick={() => setPrevContextOpen(!prevContextOpen)}
            className="flex w-full items-center justify-between p-4 text-left"
          >
            <span className="text-sm font-semibold text-gray-700">
              {t("wizard.previousResults")}
            </span>
            {prevContextOpen ? (
              <ChevronUp className="h-4 w-4 text-gray-400" />
            ) : (
              <ChevronDown className="h-4 w-4 text-gray-400" />
            )}
          </button>
          {prevContextOpen && (
            <div className="border-t border-gray-100 px-4 pb-4">
              {previousStages.map((prevStage, pIdx) => {
                const prevTpl = template.stages[pIdx];
                if (!prevTpl) return null;
                const filledTasks = prevStage.tasks.filter(
                  (t) => Object.keys(t.form_data).length > 0
                );
                if (filledTasks.length === 0) return null;

                return (
                  <div key={prevStage.id} className="mt-3 first:mt-0">
                    <p className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-400">
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                      {prevTpl.title}
                    </p>
                    <div className="grid gap-2 sm:grid-cols-2">
                      {filledTasks.map((task) => {
                        const tTpl = prevTpl.tasks.find(
                          (t) => t.id === task.template_id
                        );
                        if (!tTpl) return null;
                        const entries = Object.entries(task.form_data)
                          .filter(([, v]) => v);
                        return (
                          <div
                            key={task.id}
                            className="rounded-lg border border-gray-100 bg-gray-50 p-3"
                          >
                            <p className="text-xs font-semibold text-gray-700">
                              {tTpl.title}
                            </p>
                            {entries.map(([key, val]) => {
                              const fieldTpl = tTpl.form_fields.find(
                                (f) => f.name === key
                              );
                              return (
                                <p
                                  key={key}
                                  className="mt-1 text-xs text-gray-500"
                                >
                                  <span className="font-medium text-gray-600">
                                    {fieldTpl?.label ?? key}:
                                  </span>{" "}
                                  {val}
                                </p>
                              );
                            })}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Next step guidance */}
      {!stageAllDone && (
        <div className="mb-5 rounded-lg border border-blue-100 bg-blue-50/50 p-3">
          <p className="flex items-center gap-2 text-xs font-medium text-blue-700">
            <Circle className="h-3 w-3 fill-blue-400 text-blue-400" />
            {t("wizard.nextStepLabel")}{" "}
            {(() => {
              const nextTask = stage.tasks.find((t) => t.status !== "done");
              if (!nextTask) return t("wizard.allTasksDone");
              const tpl = stageTpl.tasks.find((t) => t.id === nextTask.template_id);
              return tpl?.title ?? t("wizard.editTask");
            })()}
          </p>
        </div>
      )}

      {/* Task cards */}
      <div className="grid gap-4">
        {stage.tasks.map((task, taskIdx) => {
          const tpl = stageTpl.tasks.find((t) => t.id === task.template_id);
          if (!tpl) return null;
          const cfg = statusConfig[task.status];
          const Icon = cfg.icon;
          const isNext =
            task.status !== "done" &&
            stage.tasks.slice(0, taskIdx).every((t) => t.status === "done");

          return (
            <div
              key={task.id}
              className={`rounded-xl border bg-white p-4 shadow-sm transition hover:shadow-md sm:p-5 ${
                isNext
                  ? "border-blue-200 ring-1 ring-blue-100"
                  : "border-gray-200"
              }`}
            >
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:gap-4">
                <div className="flex items-start gap-3 sm:gap-4 sm:flex-1 sm:min-w-0">
                  <Icon className={`mt-0.5 h-6 w-6 shrink-0 ${cfg.color}`} />
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-semibold text-gray-900">{tpl.title}</h3>
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        task.status === "done"
                          ? "bg-emerald-50 text-emerald-700"
                          : task.status === "in_progress"
                            ? "bg-amber-50 text-amber-700"
                            : "bg-gray-100 text-gray-500"
                      }`}
                    >
                      {cfg.label}
                    </span>
                    {isNext && (
                      <span className="rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-700">
                        {t("wizard.nextStepBadge")}
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-sm text-gray-500">{tpl.description}</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {tpl.form_fields.length > 0 && (
                      <span className="inline-flex items-center gap-1 rounded bg-gray-50 px-2 py-0.5 text-xs text-gray-500">
                        <FileEdit className="h-3 w-3" />
                        {tpl.form_fields.length} {t("wizard.fields")}
                      </span>
                    )}
                    {tpl.checklist.length > 0 && (
                      <span className="inline-flex items-center gap-1 rounded bg-gray-50 px-2 py-0.5 text-xs text-gray-500">
                        <CheckCircle2 className="h-3 w-3" />
                        {task.completed_checklist.length}/{tpl.checklist.length}{" "}
                        {t("wizard.items")}
                      </span>
                    )}
                    {tpl.form_fields.some((f) => f.type !== "date") && (
                      <span className="inline-flex items-center gap-1 rounded bg-violet-50 px-2 py-0.5 text-xs text-violet-600">
                        {t("wizard.aiSupport")}
                      </span>
                    )}
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => openTask(task.id)}
                  className={`w-full shrink-0 rounded-lg px-4 py-2.5 text-sm font-medium transition sm:w-auto sm:py-2 ${
                    task.status === "done"
                      ? "border border-gray-200 bg-white text-gray-600 hover:bg-gray-50"
                      : isNext
                        ? "bg-blue-600 text-white shadow-sm hover:bg-blue-700"
                        : "bg-blue-600 text-white hover:bg-blue-700"
                  }`}
                >
                  {task.status === "done" ? t("wizard.view") : t("wizard.edit")}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
