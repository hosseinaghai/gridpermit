import { MapPin } from "lucide-react";
import type { Project, ProcessTemplate } from "../types";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";

interface Props {
  project: Project;
  template: ProcessTemplate;
}

export default function SectionTabs({ project }: Props) {
  const { selectedSectionIndex, selectSection } = useWorkflowStore();
  const t = useT();

  if (project.sections.length === 0) return null;

  return (
    <div className="border-b border-gray-200 bg-white px-3 md:px-6">
      <div className="flex items-center gap-2 overflow-x-auto py-1">
        <span className="hidden text-xs font-semibold uppercase tracking-wider text-gray-400 md:inline">
          {t("sections.title")}
        </span>
        <div className="flex gap-1">
          {project.sections.map((section, idx) => {
            const isSelected = idx === selectedSectionIndex;
            const totalTasks = section.stages.reduce((a, s) => a + s.tasks.length, 0);
            const doneTasks = section.stages.reduce(
              (a, s) => a + s.tasks.filter((tk) => tk.status === "done").length,
              0
            );
            const pct = totalTasks > 0 ? Math.round((doneTasks / totalTasks) * 100) : 0;

            return (
              <button
                key={section.id}
                onClick={() => selectSection(idx)}
                className={`flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-left transition ${
                  isSelected
                    ? "bg-blue-50 ring-1 ring-blue-200"
                    : "hover:bg-gray-50"
                }`}
              >
                <MapPin
                  className={`h-3.5 w-3.5 shrink-0 ${
                    isSelected ? "text-blue-600" : "text-gray-400"
                  }`}
                />
                <div className="min-w-0">
                  <p
                    className={`text-sm font-semibold leading-tight ${
                      isSelected ? "text-blue-900" : "text-gray-700"
                    }`}
                  >
                    {section.name}
                  </p>
                  <p className="text-[10px] text-gray-400">
                    {t("sections.km", {
                      start: section.km_start,
                      end: section.km_end,
                    })}{" "}
                    &middot;{" "}
                    {t("sections.progress", { pct })}
                  </p>
                </div>
                {/* Mini progress bar */}
                <div className="hidden h-1.5 w-12 overflow-hidden rounded-full bg-gray-100 sm:block">
                  <div
                    className={`h-full rounded-full transition-all ${
                      pct === 100
                        ? "bg-emerald-500"
                        : pct > 0
                          ? "bg-amber-400"
                          : "bg-gray-200"
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
