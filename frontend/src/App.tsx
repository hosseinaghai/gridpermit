import { useQuery } from "@tanstack/react-query";
import { fetchWorkflow } from "./api/client";
import Layout from "./components/Layout";
import { useT } from "./i18n/translations";
import { useWorkflowStore } from "./store/workflowStore";

export default function App() {
  const projectId = useWorkflowStore((s) => s.projectId);
  const language = useWorkflowStore((s) => s.language);
  const t = useT();

  const { data, isLoading, error } = useQuery({
    queryKey: ["workflow", projectId, language],
    queryFn: () => fetchWorkflow(projectId!, language),
    enabled: !!projectId,
  });

  if (!projectId) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-gray-500">{t("app.noProject")}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          <span className="text-gray-600">{t("app.loading")}</span>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-red-600">
          {t("app.errorLoading")} {error?.message ?? t("app.unknownError")}
        </p>
      </div>
    );
  }

  return <Layout project={data.project} template={data.template} />;
}
