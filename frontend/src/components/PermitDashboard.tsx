import { Shield } from "lucide-react";
import type { ProcessTemplate, Project } from "../types";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";

interface Props {
  project: Project;
  template: ProcessTemplate;
  onNavigate?: () => void;
}

const PERMIT_TYPES = [
  "naturschutz",
  "waldumwandlung",
  "wasserrecht",
  "denkmalschutz",
  "kreuzung",
  "immission",
] as const;

/** Maps permit_type to the task template id that handles it */
const PERMIT_TASK_MAP: Record<string, string> = {
  naturschutz: "s3_t1",
  waldumwandlung: "s3_t3",
  wasserrecht: "s3_t4",
  denkmalschutz: "s3_t5",
  kreuzung: "s2_t4",
  immission: "s3_t6",
};

const CELL_BG: Record<string, string> = {
  open: "bg-red-400 hover:bg-red-500",
  in_progress: "bg-amber-400 hover:bg-amber-500",
  approved: "bg-emerald-400 hover:bg-emerald-500",
};

function worstStatus(statuses: string[]): string {
  if (statuses.length === 0) return "none";
  if (statuses.includes("open")) return "open";
  if (statuses.includes("in_progress")) return "in_progress";
  return "approved";
}

export default function PermitDashboard({ project, template, onNavigate }: Props) {
  const t = useT();
  const navigateTo = useWorkflowStore((s) => s.navigateTo);
  const sections = project.sections;
  const permits = project.permits;

  if (sections.length === 0) return null;

  const getPermits = (sectionId: string, permitType: string) =>
    permits.filter(
      (p) => p.section_id === sectionId && p.permit_type === permitType
    );

  /** Navigate to the section, stage, and task that corresponds to a permit type */
  const handleCellClick = (sectionIndex: number, permitType: string) => {
    const taskTemplateId = PERMIT_TASK_MAP[permitType];
    if (!taskTemplateId) {
      navigateTo(sectionIndex, 0);
      onNavigate?.();
      return;
    }

    // Find which stage index contains this task template
    let stageIndex = 0;
    for (let si = 0; si < template.stages.length; si++) {
      const stage = template.stages[si];
      if (stage && stage.tasks.some((tt) => tt.id === taskTemplateId)) {
        stageIndex = si;
        break;
      }
    }

    // Find the task instance id in the section's stages
    const section = sections[sectionIndex];
    let taskInstanceId: string | undefined;
    if (section) {
      const stageInstance = section.stages[stageIndex];
      if (stageInstance) {
        const taskInstance = stageInstance.tasks.find(
          (ti) => ti.template_id === taskTemplateId
        );
        if (taskInstance) {
          taskInstanceId = taskInstance.id;
        }
      }
    }

    navigateTo(sectionIndex, stageIndex, taskInstanceId);
    onNavigate?.();
  };

  return (
    <div className="flex flex-col rounded-xl border border-gray-200 bg-white shadow-sm">
      <div className="flex items-center gap-2 border-b border-gray-100 px-4 py-2.5">
        <Shield className="h-4 w-4 text-blue-600" />
        <h3 className="text-sm font-bold text-gray-900">{t("permits.title")}</h3>
      </div>
      <div className="p-3">
        <table className="w-full border-separate border-spacing-[3px]">
          <thead>
            <tr>
              <th />
              {sections.map((s) => (
                <th
                  key={s.id}
                  className="pb-0.5 text-center text-[10px] font-semibold text-gray-600"
                >
                  {s.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PERMIT_TYPES.map((pt) => (
              <tr key={pt}>
                <td className="whitespace-nowrap pr-2 text-right text-[10px] font-medium text-gray-500">
                  {t(`permits.type.${pt}`)}
                </td>
                {sections.map((s, sIdx) => {
                  const sectionPermits = getPermits(s.id, pt);
                  const status = worstStatus(
                    sectionPermits.map((p) => p.status)
                  );
                  return (
                    <td key={s.id} className="text-center">
                      <button
                        onClick={() => handleCellClick(sIdx, pt)}
                        title={
                          sectionPermits.length > 0
                            ? sectionPermits.map((p) => p.label).join("\n")
                            : t(`permits.type.${pt}`)
                        }
                        className={`mx-auto block h-5 w-full max-w-[2rem] rounded cursor-pointer transition ${CELL_BG[status] ?? "bg-emerald-400 hover:bg-emerald-500"}`}
                      />
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
        {/* Legend */}
        <div className="mt-2 flex items-center justify-end gap-3 text-[9px] text-gray-400">
          <span className="flex items-center gap-1">
            <span className="inline-block h-2.5 w-2.5 rounded bg-emerald-400" />
            {t("permits.approved")}
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-2.5 w-2.5 rounded bg-amber-400" />
            {t("permits.inProgress")}
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-2.5 w-2.5 rounded bg-red-400" />
            {t("permits.open")}
          </span>
        </div>
      </div>
    </div>
  );
}
