import { Mail, Zap } from "lucide-react";
import { useState } from "react";
import type { ProcessTemplate, Project } from "../types";
import { useWorkflowStore } from "../store/workflowStore";
import EmailInbox from "./EmailInbox";
import InfoPanel from "./InfoPanel";
import ProcessStepper from "./ProcessStepper";
import WorkflowWizard from "./WorkflowWizard";

interface Props {
  project: Project;
  template: ProcessTemplate;
}

export default function Layout({ project, template }: Props) {
  const selectedStageIndex = useWorkflowStore((s) => s.selectedStageIndex);
  const selectedStageTpl = template.stages[selectedStageIndex] ?? null;
  const [emailOpen, setEmailOpen] = useState(false);

  // Count unread emails (mock)
  const unreadEmails = 3;

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar */}
      <header className="flex items-center gap-3 border-b border-gray-200 bg-white px-6 py-3">
        <div className="flex items-center gap-2 text-blue-700">
          <Zap className="h-6 w-6" />
          <span className="text-lg font-bold tracking-tight">GridPermit Guide</span>
        </div>
        <span className="text-sm text-gray-300">|</span>
        <span className="text-sm font-medium text-gray-700">{project.name}</span>
        <div className="ml-auto flex items-center gap-2">
          <span className="rounded bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700">
            {project.pfad}
          </span>
          <span className="rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
            {project.kv_level} kV {project.technology}
          </span>
          <span className="rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
            {project.length_km} km
          </span>
          <span className="rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
            {project.states_crossed.join(", ")}
          </span>
          {/* Email inbox button */}
          <button
            onClick={() => setEmailOpen(true)}
            className="relative ml-2 rounded-lg border border-gray-200 p-2 text-gray-600 transition hover:bg-gray-50 hover:text-gray-800"
            title="E-Mail-Eingang"
          >
            <Mail className="h-4 w-4" />
            {unreadEmails > 0 && (
              <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[9px] font-bold text-white">
                {unreadEmails}
              </span>
            )}
          </button>
        </div>
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar */}
        <aside className="w-72 shrink-0 overflow-y-auto border-r border-gray-200 bg-white p-5">
          <ProcessStepper project={project} template={template} />
        </aside>

        {/* Center workspace */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6">
          <WorkflowWizard project={project} template={template} />
        </main>

        {/* Right info panel */}
        {selectedStageTpl && (
          <aside className="hidden w-80 shrink-0 overflow-y-auto border-l border-gray-200 bg-white p-5 xl:block">
            <InfoPanel project={project} stage={selectedStageTpl} />
          </aside>
        )}
      </div>

      {/* Email inbox overlay */}
      <EmailInbox
        project={project}
        template={template}
        isOpen={emailOpen}
        onClose={() => setEmailOpen(false)}
      />
    </div>
  );
}
