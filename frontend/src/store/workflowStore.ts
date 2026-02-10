import { create } from "zustand";
import type { Language } from "../i18n/translations";

interface WorkflowState {
  projectId: string | null;
  selectedStageIndex: number;
  selectedTaskId: string | null;
  sidebarOpen: boolean;
  infoPanelOpen: boolean;
  language: Language;
  setProjectId: (id: string) => void;
  selectStage: (index: number) => void;
  openTask: (taskId: string) => void;
  closeTask: () => void;
  setSidebarOpen: (open: boolean) => void;
  setInfoPanelOpen: (open: boolean) => void;
  setLanguage: (lang: Language) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  projectId: "P-DE-TSO-001",
  selectedStageIndex: 2, // Start at stage 3 (Untersuchungsrahmen)
  selectedTaskId: null,
  sidebarOpen: false,
  infoPanelOpen: false,
  language: (localStorage.getItem("gridpermit-lang") as Language) || "de",
  setProjectId: (id) => set({ projectId: id, selectedTaskId: null }),
  selectStage: (index) => set({ selectedStageIndex: index, selectedTaskId: null, sidebarOpen: false }),
  openTask: (taskId) => set({ selectedTaskId: taskId }),
  closeTask: () => set({ selectedTaskId: null }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setInfoPanelOpen: (open) => set({ infoPanelOpen: open }),
  setLanguage: (lang) => {
    localStorage.setItem("gridpermit-lang", lang);
    set({ language: lang });
  },
}));
