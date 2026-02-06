import { create } from "zustand";

interface WorkflowState {
  projectId: string | null;
  selectedStageIndex: number;
  selectedTaskId: string | null;
  sidebarOpen: boolean;
  infoPanelOpen: boolean;
  setProjectId: (id: string) => void;
  selectStage: (index: number) => void;
  openTask: (taskId: string) => void;
  closeTask: () => void;
  setSidebarOpen: (open: boolean) => void;
  setInfoPanelOpen: (open: boolean) => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  projectId: "P-DE-TSO-001",
  selectedStageIndex: 2, // Start at stage 3 (Untersuchungsrahmen)
  selectedTaskId: null,
  sidebarOpen: false,
  infoPanelOpen: false,
  setProjectId: (id) => set({ projectId: id, selectedTaskId: null }),
  selectStage: (index) => set({ selectedStageIndex: index, selectedTaskId: null, sidebarOpen: false }),
  openTask: (taskId) => set({ selectedTaskId: taskId }),
  closeTask: () => set({ selectedTaskId: null }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setInfoPanelOpen: (open) => set({ infoPanelOpen: open }),
}));
