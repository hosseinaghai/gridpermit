import { useQuery } from "@tanstack/react-query";
import { fetchWorkflow } from "./api/client";
import Layout from "./components/Layout";
import { useWorkflowStore } from "./store/workflowStore";

export default function App() {
  const projectId = useWorkflowStore((s) => s.projectId);

  const { data, isLoading, error } = useQuery({
    queryKey: ["workflow", projectId],
    queryFn: () => fetchWorkflow(projectId!),
    enabled: !!projectId,
  });

  if (!projectId) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-gray-500">Kein Projekt ausgewählt.</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          <span className="text-gray-600">Workflow wird geladen...</span>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-red-600">
          Fehler beim Laden: {error?.message ?? "Unbekannter Fehler"}
        </p>
      </div>
    );
  }

  return <Layout project={data.project} template={data.template} />;
}
