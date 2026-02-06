import {
  AlertTriangle,
  BookOpen,
  Calendar,
  Clock,
  FileText,
  Layers,
  MapPin,
  Scale,
} from "lucide-react";
import type { Project, StageTemplate } from "../types";
import MapPanel from "./MapPanel";

interface Props {
  project: Project;
  stage: StageTemplate;
}

const outcomeLabels: Record<string, { label: string; color: string }> = {
  granted_with_conditions: {
    label: "Genehmigt (m. Auflagen)",
    color: "text-emerald-700 bg-emerald-50",
  },
  delayed: { label: "Verzögert", color: "text-amber-700 bg-amber-50" },
  granted: { label: "Genehmigt", color: "text-emerald-700 bg-emerald-50" },
  rejected: { label: "Abgelehnt", color: "text-red-700 bg-red-50" },
};

const riskColors: Record<string, string> = {
  biodiversity: "bg-green-500",
  land_rights: "bg-orange-500",
  schedule: "bg-blue-500",
  technical: "bg-purple-500",
};

const riskLabels: Record<string, string> = {
  biodiversity: "Artenschutz",
  land_rights: "Wegerechte",
  schedule: "Zeitplan",
  technical: "Technik",
};

const docStatusStyles: Record<string, { label: string; color: string }> = {
  approved_internal: { label: "Freigegeben", color: "bg-emerald-100 text-emerald-700" },
  needs_revision: { label: "Überarbeitung", color: "bg-amber-100 text-amber-700" },
  draft: { label: "Entwurf", color: "bg-gray-100 text-gray-600" },
};

function daysUntil(dateStr: string): number {
  const target = new Date(dateStr);
  const now = new Date();
  return Math.ceil((target.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

export default function InfoPanel({ project, stage }: Props) {
  return (
    <div className="space-y-6">
      {/* Mini map */}
      <div>
        <div className="flex items-center gap-2 text-gray-400">
          <MapPin className="h-4 w-4" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">
            Trassenübersicht
          </h3>
        </div>
        <div className="mt-3 h-48">
          <MapPanel
            project={project}
            showLayers={{
              corridor: true,
              ffh: true,
              wald: true,
              wsg: true,
              parcels: false,
              railway: true,
              settlements: false,
            }}
          />
        </div>
      </div>

      {/* Legal context */}
      <div>
        <div className="flex items-center gap-2 text-gray-400">
          <BookOpen className="h-4 w-4" />
          <h3 className="text-xs font-semibold uppercase tracking-wider">
            Rechtlicher Kontext
          </h3>
        </div>
        <div className="mt-3 rounded-lg border border-amber-100 bg-amber-50/50 p-4">
          <div className="flex items-center gap-2">
            <Scale className="h-4 w-4 text-amber-600" />
            <span className="text-sm font-semibold text-amber-800">
              {stage.law_reference}
            </span>
          </div>
          <p className="mt-2 text-xs leading-relaxed text-amber-900/80">
            {stage.info_text}
          </p>
        </div>
      </div>

      {/* Deadlines */}
      {project.project_tasks && project.project_tasks.length > 0 && (
        <div>
          <div className="flex items-center gap-2 text-gray-400">
            <Calendar className="h-4 w-4" />
            <h3 className="text-xs font-semibold uppercase tracking-wider">
              Fristen
            </h3>
          </div>
          <div className="mt-3 space-y-2">
            {project.project_tasks.map((t) => {
              const days = daysUntil(t.due_date);
              return (
                <div
                  key={t.task_id}
                  className={`rounded-lg border p-3 ${
                    days <= 3
                      ? "border-red-200 bg-red-50"
                      : days <= 7
                        ? "border-amber-200 bg-amber-50"
                        : "border-gray-100 bg-gray-50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-gray-800">
                      {t.title}
                    </span>
                    <span
                      className={`rounded px-1.5 py-0.5 text-[10px] font-bold ${
                        days <= 3
                          ? "bg-red-200 text-red-800"
                          : days <= 7
                            ? "bg-amber-200 text-amber-800"
                            : "bg-gray-200 text-gray-700"
                      }`}
                    >
                      {days <= 0 ? "Überfällig!" : `${days} Tage`}
                    </span>
                  </div>
                  <p className="mt-1 text-[10px] text-gray-500">
                    Frist: {t.due_date} &middot; {t.owner_role}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Historical cases */}
      {project.historical_cases.length > 0 && (
        <div>
          <div className="flex items-center gap-2 text-gray-400">
            <Clock className="h-4 w-4" />
            <h3 className="text-xs font-semibold uppercase tracking-wider">
              Vergleichbare Fälle
            </h3>
          </div>
          <div className="mt-3 space-y-3">
            {project.historical_cases.map((c) => {
              const outcome = outcomeLabels[c.outcome] ?? {
                label: c.outcome,
                color: "text-gray-600 bg-gray-50",
              };
              return (
                <div
                  key={c.case_id}
                  className="rounded-lg border border-gray-100 bg-gray-50 p-3"
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-xs font-semibold text-gray-800">
                      {c.title}
                    </p>
                    <span
                      className={`shrink-0 rounded px-1.5 py-0.5 text-[10px] font-semibold ${outcome.color}`}
                    >
                      {outcome.label}
                    </span>
                  </div>
                  <p className="mt-1 text-[10px] text-gray-400">{c.case_id}</p>
                  <ul className="mt-2 space-y-1">
                    {c.key_reasons.map((r, i) => (
                      <li
                        key={i}
                        className="text-xs text-gray-600"
                      >
                        <span className="mr-1 text-gray-300">&bull;</span>
                        {r}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Risks */}
      {project.risks.length > 0 && (
        <div>
          <div className="flex items-center gap-2 text-gray-400">
            <AlertTriangle className="h-4 w-4" />
            <h3 className="text-xs font-semibold uppercase tracking-wider">
              Risiken
            </h3>
          </div>
          <div className="mt-3 space-y-2">
            {project.risks.map((r) => {
              const score = r.probability * r.impact;
              return (
                <div
                  key={r.risk_id}
                  className="rounded-lg border border-gray-100 bg-gray-50 p-3"
                >
                  <div className="flex items-center gap-2">
                    <div
                      className={`h-2.5 w-2.5 rounded-full ${
                        riskColors[r.category] ?? "bg-gray-400"
                      }`}
                    />
                    <span className="text-xs font-semibold text-gray-800">
                      {riskLabels[r.category] ?? r.category}
                    </span>
                    <span className="ml-auto text-[10px] font-bold text-gray-400">
                      Score: {(score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">{r.mitigation}</p>
                  <p className="mt-0.5 text-[10px] text-gray-400">
                    Verantw.: {r.owner}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Geo layers */}
      {project.geo_layers.length > 0 && (
        <div>
          <div className="flex items-center gap-2 text-gray-400">
            <Layers className="h-4 w-4" />
            <h3 className="text-xs font-semibold uppercase tracking-wider">
              Geo-Layer
            </h3>
          </div>
          <div className="mt-3 space-y-1.5">
            {project.geo_layers.map((gl) => (
              <div
                key={gl.layer_id}
                className="flex items-center justify-between rounded border border-gray-100 bg-gray-50 px-3 py-2"
              >
                <span className="text-xs font-medium text-gray-700">
                  {gl.type}
                </span>
                <span className="text-[10px] text-gray-400">
                  {gl.last_update}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Documents */}
      {project.documents.length > 0 && (
        <div>
          <div className="flex items-center gap-2 text-gray-400">
            <FileText className="h-4 w-4" />
            <h3 className="text-xs font-semibold uppercase tracking-wider">
              Dokumente
            </h3>
          </div>
          <div className="mt-3 space-y-1.5">
            {project.documents.map((doc) => {
              const ds = docStatusStyles[doc.status] ?? {
                label: doc.status,
                color: "bg-gray-100 text-gray-600",
              };
              return (
                <div
                  key={doc.doc_id}
                  className="flex items-center justify-between rounded border border-gray-100 bg-gray-50 px-3 py-2"
                >
                  <div>
                    <p className="text-xs font-medium text-gray-700">
                      {doc.doc_type}
                    </p>
                    <p className="text-[10px] text-gray-400">
                      {doc.doc_id} &middot; {doc.version}
                    </p>
                  </div>
                  <span
                    className={`rounded px-1.5 py-0.5 text-[10px] font-semibold ${ds.color}`}
                  >
                    {ds.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
