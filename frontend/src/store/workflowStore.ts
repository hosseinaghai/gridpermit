import { create } from "zustand";
import type { Language } from "../i18n/translations";

interface WorkflowState {
  projectId: string | null;
  selectedSectionIndex: number;
  selectedStageIndex: number;
  selectedTaskId: string | null;
  sidebarOpen: boolean;
  infoPanelOpen: boolean;
  language: Language;
  setProjectId: (id: string) => void;
  selectSection: (index: number) => void;
  selectStage: (index: number) => void;
  navigateTo: (sectionIndex: number, stageIndex: number, taskId?: string) => void;
  openTask: (taskId: string) => void;
  closeTask: () => void;
  setSidebarOpen: (open: boolean) => void;
  setInfoPanelOpen: (open: boolean) => void;
  setLanguage: (lang: Language) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  projectId: "P-DE-TSO-001",
  selectedSectionIndex: 0,
  selectedStageIndex: 2, // Start at stage 3 (Untersuchungsrahmen) for section A
  selectedTaskId: null,
  sidebarOpen: false,
  infoPanelOpen: false,
  language: (localStorage.getItem("gridpermit-lang") as Language) || "de",
  setProjectId: (id) => set({ projectId: id, selectedTaskId: null }),
  selectSection: (index) => set({ selectedSectionIndex: index, selectedStageIndex: 0, selectedTaskId: null, sidebarOpen: false }),
  selectStage: (index) => set({ selectedStageIndex: index, selectedTaskId: null, sidebarOpen: false }),
  navigateTo: (sectionIndex, stageIndex, taskId) => set({ selectedSectionIndex: sectionIndex, selectedStageIndex: stageIndex, selectedTaskId: taskId ?? null, sidebarOpen: false }),
  openTask: (taskId) => set({ selectedTaskId: taskId }),
  closeTask: () => set({ selectedTaskId: null }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setInfoPanelOpen: (open) => set({ infoPanelOpen: open }),
  setLanguage: (lang) => {
    localStorage.setItem("gridpermit-lang", lang);
    set({ language: lang });
  },
}));
