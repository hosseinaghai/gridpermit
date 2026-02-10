import {
  ArrowRight,
  Check,
  ChevronDown,
  ChevronUp,
  Inbox,
  Mail,
  MailOpen,
  Sparkles,
  X,
} from "lucide-react";
import { useState } from "react";
import type { ProcessTemplate, Project } from "../types";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";

export interface Email {
  id: string;
  from: string;
  subject: string;
  body: string;
  received_at: string;
  read: boolean;
  filed: boolean;
  ai_suggestion?: {
    stage_index: number;
    stage_title: string;
    task_template_id: string;
    task_title: string;
    confidence: number;
    reason: string;
  };
}

// Mock emails
const MOCK_EMAILS: Email[] = [
  {
    id: "email-001",
    from: "netzausbau@bnetza.de",
    subject: "Eingangsbestätigung Antrag Bundesfachplanung – P-DE-TSO-001",
    body: `Sehr geehrte Damen und Herren,

hiermit bestätigen wir den Eingang Ihres Antrags auf Bundesfachplanung gemäß § 6 NABEG für das Vorhaben "Nord-Süd-Link Abschnitt Demo A" (Az.: BFP-2026-001).

Die Vollständigkeitsprüfung wird innerhalb von 4 Wochen abgeschlossen. Wir werden Sie über das Ergebnis informieren.

Mit freundlichen Grüßen
Bundesnetzagentur
Referat für Netzausbau`,
    received_at: "2026-02-04T09:15:00",
    read: true,
    filed: false,
    ai_suggestion: {
      stage_index: 0,
      stage_title: "Scope & Rechtsrahmen",
      task_template_id: "s1_t1",
      task_title: "Rechtsrahmen & Zuständigkeit",
      confidence: 0.92,
      reason: "Bezug auf § 6 NABEG Antrag, Eingangsbestätigung der BNetzA",
    },
  },
  {
    id: "email-002",
    from: "forst@aelf-musterstadt.bayern.de",
    subject: "Rückfrage Waldumwandlung – Unterlagen unvollständig",
    body: `Sehr geehrte Damen und Herren,

bezugnehmend auf Ihre Anfrage zur Waldumwandlung vom 28.01.2026 teilen wir mit, dass die eingereichten Unterlagen unvollständig sind.

Es fehlen:
1. Detailkarte der Waldtypen im Maßstab 1:5.000 (nur 1:10.000 vorliegend)
2. Nachweis über die Prüfung von Trassenalternativen im Waldbereich
3. Aktualisiertes Konzept zum Waldausgleich (Referenz auf veraltete Daten)

Bitte reichen Sie die fehlenden Unterlagen bis zum 28.02.2026 nach.

Mit freundlichen Grüßen
Amt für Ernährung, Landwirtschaft und Forsten`,
    received_at: "2026-02-05T14:30:00",
    read: false,
    filed: false,
    ai_suggestion: {
      stage_index: 2,
      stage_title: "Untersuchungsrahmen",
      task_template_id: "s3_t3",
      task_title: "Forstbehörde-Anfrage",
      confidence: 0.95,
      reason: "Direkte Antwort auf Forstanfrage, Nachforderung fehlender Unterlagen",
    },
  },
  {
    id: "email-003",
    from: "dr.schmidt@oeko-gutachten.de",
    subject: "Zwischenbericht Artenschutzkartierung – Fledermausdaten",
    body: `Sehr geehrte Projektleitung,

anbei übersende ich den Zwischenbericht der Fledermaus-Detektorbegehungen (Stand 60%).

Ergebnisse bisher:
- 4 Arten nachgewiesen: Großes Mausohr, Zwergfledermaus, Breitflügelfledermaus, Abendsegler
- Quartiersverdacht bei km 34,5 bestätigt (Wochenstube Großes Mausohr)
- Flugrouten entlang der Waldkante bei km 12-18 dokumentiert

Die restlichen Begehungen sind für KW 7-8 geplant. Der Abschlussbericht wird fristgerecht bis 20.02.2026 vorliegen.

Beste Grüße
Dr. Anna Schmidt
Ökologische Fachgutachten`,
    received_at: "2026-02-05T16:45:00",
    read: false,
    filed: false,
    ai_suggestion: {
      stage_index: 2,
      stage_title: "Untersuchungsrahmen",
      task_template_id: "s3_t1",
      task_title: "Artenschutz-Vorprüfung",
      confidence: 0.97,
      reason: "Artenschutzkartierung Fledermäuse, direkt relevant für ASP",
    },
  },
  {
    id: "email-004",
    from: "mueller.k@demohausen.de",
    subject: "Anfrage Erdkabelverlegung – Auswirkungen auf Gemeindestraße",
    body: `Sehr geehrte Damen und Herren,

als Bürgermeisterin der Gemeinde Demohausen möchte ich folgende Fragen zur geplanten Erdkabelverlegung im Bereich unserer Gemeinde stellen:

1. Wie lang wird die Bauphase im Bereich der Gemeindestraße dauern?
2. Ist eine Vollsperrung geplant oder wird der Verkehr umgeleitet?
3. Wer trägt die Kosten für die Wiederherstellung der Straßenoberfläche?
4. Gibt es eine Informationsveranstaltung für die Bürgerinnen und Bürger?

Wir bitten um zeitnahe Rückmeldung.

Mit freundlichen Grüßen
Katrin Müller
Bürgermeisterin Gemeinde Demohausen`,
    received_at: "2026-02-06T08:20:00",
    read: false,
    filed: false,
    ai_suggestion: {
      stage_index: 1,
      stage_title: "Korridorfindung",
      task_template_id: "s2_t2",
      task_title: "GIS-Verschneidung",
      confidence: 0.78,
      reason: "Betrifft Flurstück HE-044-887-03, Erdkabelabschnitt bei Demohausen",
    },
  },
];

interface Props {
  project: Project;
  template: ProcessTemplate;
  isOpen: boolean;
  onClose: () => void;
}

export default function EmailInbox({ project, template, isOpen, onClose }: Props) {
  const [emails, setEmails] = useState<Email[]>(MOCK_EMAILS);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const t = useT();
  const language = useWorkflowStore((s) => s.language);

  if (!isOpen) return null;

  const unreadCount = emails.filter((e) => !e.read).length;

  const markRead = (id: string) => {
    setEmails((prev) =>
      prev.map((e) => (e.id === id ? { ...e, read: true } : e))
    );
  };

  const fileEmail = (id: string) => {
    setEmails((prev) =>
      prev.map((e) => (e.id === id ? { ...e, filed: true, read: true } : e))
    );
  };

  const toggleExpand = (id: string) => {
    const email = emails.find((e) => e.id === id);
    if (email && !email.read) markRead(id);
    setExpandedId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/30 sm:items-start sm:pt-16">
      <div className="w-full max-h-[85vh] rounded-t-xl border border-gray-200 bg-white shadow-2xl sm:mx-4 sm:max-w-2xl sm:rounded-xl sm:max-h-none">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-gray-100 px-4 py-3 sm:px-5 sm:py-4">
          <div className="flex items-center gap-3">
            <Inbox className="h-5 w-5 text-blue-600" />
            <h2 className="text-lg font-bold text-gray-900">{t("email.inbox")}</h2>
            {unreadCount > 0 && (
              <span className="rounded-full bg-red-500 px-2 py-0.5 text-xs font-bold text-white">
                {unreadCount}
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Email list */}
        <div className="max-h-[65vh] overflow-y-auto sm:max-h-[70vh]">
          {emails.map((email) => {
            const isExpanded = expandedId === email.id;
            return (
              <div
                key={email.id}
                className={`border-b border-gray-50 ${
                  email.filed ? "bg-emerald-50/30" : !email.read ? "bg-blue-50/30" : ""
                }`}
              >
                {/* Email row */}
                <button
                  onClick={() => toggleExpand(email.id)}
                  className="flex w-full items-start gap-3 px-5 py-3 text-left transition hover:bg-gray-50"
                >
                  {email.filed ? (
                    <Check className="mt-1 h-4 w-4 shrink-0 text-emerald-500" />
                  ) : email.read ? (
                    <MailOpen className="mt-1 h-4 w-4 shrink-0 text-gray-400" />
                  ) : (
                    <Mail className="mt-1 h-4 w-4 shrink-0 text-blue-500" />
                  )}
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-sm ${
                          !email.read ? "font-bold text-gray-900" : "font-medium text-gray-700"
                        }`}
                      >
                        {email.from}
                      </span>
                      <span className="text-[10px] text-gray-400">
                        {new Date(email.received_at).toLocaleDateString(
                          language === "de" ? "de-DE" : "en-US",
                          {
                            day: "2-digit",
                            month: "2-digit",
                            hour: "2-digit",
                            minute: "2-digit",
                          }
                        )}
                      </span>
                    </div>
                    <p
                      className={`mt-0.5 text-sm ${
                        !email.read ? "font-semibold text-gray-800" : "text-gray-600"
                      }`}
                    >
                      {email.subject}
                    </p>
                  </div>
                  {isExpanded ? (
                    <ChevronUp className="mt-1 h-4 w-4 shrink-0 text-gray-400" />
                  ) : (
                    <ChevronDown className="mt-1 h-4 w-4 shrink-0 text-gray-400" />
                  )}
                </button>

                {/* Expanded body */}
                {isExpanded && (
                  <div className="border-t border-gray-100 px-5 pb-4 pt-3">
                    <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans leading-relaxed">
                      {email.body}
                    </pre>

                    {/* AI suggestion */}
                    {email.ai_suggestion && !email.filed && (
                      <div className="mt-4 rounded-lg border border-violet-200 bg-violet-50 p-3">
                        <div className="flex items-center gap-2">
                          <Sparkles className="h-4 w-4 text-violet-600" />
                          <span className="text-xs font-semibold text-violet-800">
                            {t("email.aiAssignment")}
                          </span>
                          <span className="ml-auto rounded-full bg-violet-200 px-2 py-0.5 text-[10px] font-bold text-violet-700">
                            {Math.round(email.ai_suggestion.confidence * 100)}%
                          </span>
                        </div>
                        <p className="mt-1 text-xs text-violet-700">
                          <span className="font-medium">{t("email.phase")}</span>{" "}
                          {email.ai_suggestion.stage_title} &rarr;{" "}
                          <span className="font-medium">{email.ai_suggestion.task_title}</span>
                        </p>
                        <p className="mt-0.5 text-[10px] text-violet-600">
                          {email.ai_suggestion.reason}
                        </p>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            fileEmail(email.id);
                          }}
                          className="mt-2 flex items-center gap-1.5 rounded-md bg-violet-600 px-3 py-1.5 text-xs font-medium text-white transition hover:bg-violet-700"
                        >
                          <ArrowRight className="h-3.5 w-3.5" />
                          {t("email.fileAndAssign")}
                        </button>
                      </div>
                    )}

                    {email.filed && (
                      <div className="mt-3 flex items-center gap-2 text-xs text-emerald-700">
                        <Check className="h-4 w-4" />
                        {t("email.filedIn")} {email.ai_suggestion?.stage_title} &rarr;{" "}
                        {email.ai_suggestion?.task_title}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
