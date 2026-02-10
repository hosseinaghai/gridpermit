import { Globe, Info, Mail, Menu, X, Zap } from "lucide-react";
import { useState } from "react";
import type { ProcessTemplate, Project } from "../types";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";
import EmailInbox from "./EmailInbox";
import Impressum from "./Impressum";
import InfoPanel from "./InfoPanel";
import ProcessStepper from "./ProcessStepper";
import WorkflowWizard from "./WorkflowWizard";

interface Props {
  project: Project;
  template: ProcessTemplate;
}

export default function Layout({ project, template }: Props) {
  const {
    selectedStageIndex,
    sidebarOpen,
    infoPanelOpen,
    language,
    setSidebarOpen,
    setInfoPanelOpen,
    setLanguage,
  } = useWorkflowStore();
  const t = useT();
  const selectedStageTpl = template.stages[selectedStageIndex] ?? null;
  const [emailOpen, setEmailOpen] = useState(false);
  const [impressumOpen, setImpressumOpen] = useState(false);

  // Count unread emails (mock)
  const unreadEmails = 3;

  return (
    <div className="flex h-screen flex-col">
      {/* Top bar */}
      <header className="flex items-center gap-2 border-b border-gray-200 bg-white px-3 py-2 md:gap-3 md:px-6 md:py-3">
        {/* Hamburger menu - visible below lg */}
        <button
          onClick={() => setSidebarOpen(true)}
          className="rounded-lg p-2 text-gray-600 hover:bg-gray-100 lg:hidden"
          aria-label={t("layout.openSteps")}
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-2 text-blue-700">
          <Zap className="h-5 w-5 md:h-6 md:w-6" />
          <span className="text-base font-bold tracking-tight md:text-lg">GridPermit Guide</span>
        </div>
        <span className="hidden text-sm text-gray-300 sm:inline">|</span>
        <span className="hidden text-sm font-medium text-gray-700 sm:inline">{project.name}</span>
        <div className="ml-auto flex items-center gap-2">
          <span className="hidden rounded bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 md:inline">
            {project.pfad}
          </span>
          <span className="hidden rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600 md:inline">
            {project.kv_level} kV {project.technology}
          </span>
          <span className="hidden rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600 md:inline">
            {project.length_km} km
          </span>
          <span className="hidden rounded bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600 md:inline">
            {project.states_crossed.join(", ")}
          </span>
          {/* Language toggle */}
          <button
            onClick={() => setLanguage(language === "de" ? "en" : "de")}
            className="flex items-center gap-1 rounded-lg border border-gray-200 px-2 py-1.5 text-xs font-medium text-gray-600 transition hover:bg-gray-50"
            title={language === "de" ? "Switch to English" : "Auf Deutsch wechseln"}
          >
            <Globe className="h-3.5 w-3.5" />
            {language === "de" ? "EN" : "DE"}
          </button>
          {/* Info panel toggle - visible below xl */}
          {selectedStageTpl && (
            <button
              onClick={() => setInfoPanelOpen(true)}
              className="rounded-lg border border-gray-200 p-2 text-gray-600 transition hover:bg-gray-50 hover:text-gray-800 xl:hidden"
              aria-label={t("layout.openInfoPanel")}
            >
              <Info className="h-4 w-4" />
            </button>
          )}
          {/* Email inbox button */}
          <button
            onClick={() => setEmailOpen(true)}
            className="relative rounded-lg border border-gray-200 p-2 text-gray-600 transition hover:bg-gray-50 hover:text-gray-800"
            title={t("layout.emailInbox")}
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
        {/* Left sidebar backdrop - mobile only */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/30 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Left sidebar */}
        <aside
          className={`fixed inset-y-0 left-0 z-50 w-72 transform overflow-y-auto border-r border-gray-200 bg-white p-5 transition-transform duration-300 ease-in-out lg:static lg:z-auto lg:translate-x-0 lg:transition-none ${
            sidebarOpen ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          {/* Close button - mobile only */}
          <div className="mb-4 flex items-center justify-between lg:hidden">
            <span className="text-sm font-bold text-gray-700">{t("layout.navigation")}</span>
            <button
              onClick={() => setSidebarOpen(false)}
              className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <ProcessStepper project={project} template={template} />
        </aside>

        {/* Center workspace */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-3 sm:p-4 md:p-6">
          <WorkflowWizard project={project} template={template} />
        </main>

        {/* Right info panel */}
        {selectedStageTpl && (
          <>
            {/* Info panel backdrop - below xl only */}
            {infoPanelOpen && (
              <div
                className="fixed inset-0 z-40 bg-black/30 xl:hidden"
                onClick={() => setInfoPanelOpen(false)}
              />
            )}
            <aside
              className={`fixed inset-y-0 right-0 z-50 w-80 max-w-[calc(100vw-3rem)] transform overflow-y-auto border-l border-gray-200 bg-white p-5 transition-transform duration-300 ease-in-out xl:static xl:z-auto xl:max-w-none xl:translate-x-0 xl:transition-none ${
                infoPanelOpen ? "translate-x-0" : "translate-x-full"
              }`}
            >
              {/* Close button - below xl only */}
              <div className="mb-4 flex items-center justify-between xl:hidden">
                <span className="text-sm font-bold text-gray-700">{t("layout.information")}</span>
                <button
                  onClick={() => setInfoPanelOpen(false)}
                  className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <InfoPanel project={project} stage={selectedStageTpl} />
            </aside>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="flex items-center justify-between border-t border-gray-200 bg-white px-3 py-2 md:px-6">
        <span className="text-xs text-gray-400">
          &copy; {new Date().getFullYear()} Hossein Aghai. {t("layout.allRightsReserved")}
        </span>
        <button
          onClick={() => setImpressumOpen(true)}
          className="text-xs text-gray-400 underline hover:text-gray-600"
        >
          {t("layout.impressum")}
        </button>
      </footer>

      {/* Email inbox overlay */}
      <EmailInbox
        project={project}
        template={template}
        isOpen={emailOpen}
        onClose={() => setEmailOpen(false)}
      />

      {/* Impressum overlay */}
      <Impressum isOpen={impressumOpen} onClose={() => setImpressumOpen(false)} />
    </div>
  );
}
