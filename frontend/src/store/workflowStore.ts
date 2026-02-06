import { create } from "zustand";

interface WorkflowState {
  projectId: string | null;
  selectedStageIndex: number;
  selectedTaskId: string | null;
  setProjectId: (id: string) => void;
  selectStage: (index: number) => void;
  openTask: (taskId: string) => void;
  closeTask: () => void;
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  projectId: "P-DE-TSO-001",
  selectedStageIndex: 2, // Start at stage 3 (Untersuchungsrahmen)
  selectedTaskId: null,
  setProjectId: (id) => set({ projectId: id, selectedTaskId: null }),
  selectStage: (index) => set({ selectedStageIndex: index, selectedTaskId: null }),
  openTask: (taskId) => set({ selectedTaskId: taskId }),
  closeTask: () => set({ selectedTaskId: null }),
}));
