import { Check, ChevronRight, Circle } from "lucide-react";
import type { ProcessTemplate, Project, StageStatus } from "../types";
import { useWorkflowStore } from "../store/workflowStore";

interface Props {
  project: Project;
  template: ProcessTemplate;
}

const circleStyles: Record<StageStatus, string> = {
  completed: "bg-emerald-500 text-white",
  active: "bg-amber-500 text-white",
  pending: "bg-gray-200 text-gray-400",
};

const lineStyles: Record<StageStatus, string> = {
  completed: "bg-emerald-500",
  active: "bg-amber-300",
  pending: "bg-gray-200",
};

export default function ProcessStepper({ project, template }: Props) {
  const { selectedStageIndex, selectStage } = useWorkflowStore();

  return (
    <div>
      <h2 className="mb-5 text-xs font-semibold uppercase tracking-wider text-gray-400">
        Verfahrensschritte
      </h2>

      <div className="relative">
        {project.stages.map((stage, idx) => {
          const tpl = template.stages[idx]!;
          const isLast = idx === project.stages.length - 1;
          const isSelected = idx === selectedStageIndex;
          const completedTasks = stage.tasks.filter(
            (t) => t.status === "done"
          ).length;
          const totalTasks = stage.tasks.length;

          return (
            <button
              key={stage.id}
              onClick={() => selectStage(idx)}
              className={`relative flex w-full gap-3 rounded-lg pb-8 text-left transition last:pb-0 ${
                isSelected ? "bg-blue-50/80 -mx-2 px-2 py-2" : "hover:bg-gray-50 -mx-2 px-2 py-1"
              }`}
            >
              {/* Connector line */}
              {!isLast && (
                <div
                  className={`absolute left-[15px] top-9 h-[calc(100%-20px)] w-0.5 ${
                    isSelected ? "left-[17px]" : ""
                  } ${lineStyles[stage.status]}`}
                />
              )}

              {/* Circle */}
              <div
                className={`relative z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold transition ${
                  circleStyles[stage.status]
                } ${isSelected ? "ring-4 ring-blue-200" : ""}`}
              >
                {stage.status === "completed" ? (
                  <Check className="h-5 w-5" />
                ) : stage.status === "active" ? (
                  <ChevronRight className="h-5 w-5" />
                ) : (
                  <Circle className="h-4 w-4" />
                )}
              </div>

              {/* Text */}
              <div className="min-w-0 pt-1">
                <p
                  className={`text-sm font-semibold leading-tight ${
                    isSelected
                      ? "text-blue-900"
                      : stage.status === "pending"
                        ? "text-gray-400"
                        : "text-gray-900"
                  }`}
                >
                  {tpl.title}
                </p>
                <p className="mt-0.5 text-xs text-gray-400">
                  {tpl.law_reference}
                </p>
                <div className="mt-2">
                  <div className="flex items-center gap-2">
                    <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-gray-100">
                      <div
                        className={`h-full rounded-full transition-all ${
                          stage.status === "completed"
                            ? "bg-emerald-500"
                            : stage.status === "active"
                              ? "bg-amber-400"
                              : "bg-gray-300"
                        }`}
                        style={{
                          width: `${totalTasks ? (completedTasks / totalTasks) * 100 : 0}%`,
                        }}
                      />
                    </div>
                    <span className="text-xs tabular-nums text-gray-400">
                      {completedTasks}/{totalTasks}
                    </span>
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
