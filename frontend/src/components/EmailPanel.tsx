import {
  ArrowRight,
  Check,
  ChevronDown,
  ChevronUp,
  FileText,
  Inbox,
  Mail,
  MailOpen,
  Paperclip,
  Sparkles,
} from "lucide-react";
import { useState } from "react";
import type { ProcessTemplate, Project } from "../types";
import { useT } from "../i18n/translations";
import { useWorkflowStore } from "../store/workflowStore";

interface Attachment {
  name: string;
  type: string;
  size: string;
}

interface Email {
  id: string;
  from: string;
  subject: string;
  body: string;
  received_at: string;
  read: boolean;
  filed: boolean;
  attachments: Attachment[];
  ai_suggestion?: {
    stage_title: string;
    task_title: string;
  };
}

const SYNTHESIS_DE =
  "4 E-Mails: BNetzA-Eingangsbest\u00e4tigung (Pr\u00fcfung 4 Wo.), AELF-Nachforderung Waldunterlagen (Frist 28.02. \u2013 DRINGEND), Artenschutz-Zwischenbericht (4 Fledermausarten, Quartier km 34,5), Gemeinde Demohausen (5 Fragen Erdkabel, Antwort bis 15.03.)";
const SYNTHESIS_EN =
  "4 emails: BNetzA confirmation (review 4 wks), forestry doc request (deadline Feb 28 \u2013 URGENT), species interim report (4 bat species, roost km 34.5), municipality Demohausen (5 questions underground cable, response by Mar 15)";

const MOCK_EMAILS: Email[] = [
  {
    id: "email-001",
    from: "netzausbau@bnetza.de",
    subject: "Eingangsbest\u00e4tigung Antrag Bundesfachplanung \u2013 P-DE-TSO-001",
    body: "Sehr geehrte Damen und Herren,\n\nhiermit best\u00e4tigen wir den Eingang Ihres Antrags auf Bundesfachplanung gem\u00e4\u00df \u00a7 6 NABEG f\u00fcr das Vorhaben \"Nord-S\u00fcd-Link Abschnitt Demo A\" (Az.: BFP-2026-001).\n\nFolgende Verfahrensschritte teilen wir Ihnen mit:\n\n1. Vollst\u00e4ndigkeitspr\u00fcfung\nDie eingereichten Unterlagen werden innerhalb von 4 Wochen gepr\u00fcft. Eingereicht wurden:\n- Antrag auf Bundesfachplanung (Formblatt BFP-A, 47 Seiten)\n- Erl\u00e4uterungsbericht mit Vorschlag Untersuchungsrahmen (128 Seiten)\n- \u00dcbersichtskarte Trassenkorridore 1:100.000\n- UVP-Bericht (Vorentwurf)\n- Natura 2000-Vorpr\u00fcfung\n\n2. Antragskonferenz\nNach positiver Pr\u00fcfung wird die Antragskonferenz gem\u00e4\u00df \u00a7 7 NABEG einberufen. Voraussichtlicher Termin: KW 14-16/2026.\n\n3. Festlegung Untersuchungsrahmen\nAuf Grundlage der Antragskonferenz wird der Untersuchungsrahmen gem\u00e4\u00df \u00a7 7 Abs. 4 NABEG festgelegt (Frist: 2 Monate).\n\nAnsprechpartner: Dr. Thomas Weber, Referat N3\nTel.: +49 (0)228 14-6789\n\nMit freundlichen Gr\u00fc\u00dfen\nBundesnetzagentur\nAbteilung Netzausbau",
    received_at: "2026-02-04T09:15:00",
    read: true,
    filed: false,
    attachments: [
      { name: "Eingangsbest\u00e4tigung_BFP-2026-001.pdf", type: "pdf", size: "0.3 MB" },
    ],
    ai_suggestion: {
      stage_title: "Scope & Rechtsrahmen",
      task_title: "Rechtsrahmen & Zust\u00e4ndigkeit",
    },
  },
  {
    id: "email-002",
    from: "forst@aelf-musterstadt.bayern.de",
    subject: "R\u00fcckfrage Waldumwandlung \u2013 Unterlagen unvollst\u00e4ndig",
    body: "Sehr geehrte Damen und Herren,\n\nbezugnehmend auf Ihre Anfrage zur Waldumwandlungsgenehmigung gem\u00e4\u00df Art. 9 BayWaldG vom 28.01.2026 (Az.: AELF-MS-2026-0342) teilen wir mit, dass die Unterlagen nach Fachpr\u00fcfung unvollst\u00e4ndig sind.\n\nFehlende Unterlagen:\n\n1. Detailkarte der Waldtypen\nErforderlich im Ma\u00dfstab 1:5.000 (eingereicht: nur 1:10.000) mit:\n- Baumartenzusammensetzung je Bestand\n- Altersklassen und Bestockungsgrad\n- Schutzstatus (Bannwald, Schutzwald, Erholungswald)\n- Biotopb\u00e4ume und Totholzanteile\n\n2. Trassenalternativen im Waldbereich\nGem\u00e4\u00df Art. 9 Abs. 4 BayWaldG ist nachzuweisen, dass keine zumutbare Alternative besteht. Detaillierte Variantenuntersuchung erforderlich f\u00fcr km 8,2\u201312,7 und km 18,1\u201321,3.\n\n3. Aktualisiertes Waldausgleichskonzept\nStand September 2024 veraltet. Bitte \u00fcberarbeiten mit:\n- Aktuelle Fl\u00e4chenverf\u00fcgbarkeit (Kataster Stand 01.01.2026)\n- Erstaufforstungsfaktor 1:2 f\u00fcr Bannwaldbereiche\n- Zeitplanung Aufforstungsma\u00dfnahmen\n\nFrist: 28.02.2026. Bei Nichteinhaltung ruht die Bearbeitung.\n\nR\u00fcckfragen: Frau Dipl.-Ing. Sabine Forster, Tel.: 08421/70-234\n\nMit freundlichen Gr\u00fc\u00dfen\nAELF Musterstadt, Bereich Forsten",
    received_at: "2026-02-05T14:30:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Pr\u00fcfvermerk_Waldumwandlung_2026-0342.pdf", type: "pdf", size: "1.2 MB" },
      { name: "Checkliste_fehlende_Unterlagen.xlsx", type: "xlsx", size: "0.1 MB" },
    ],
    ai_suggestion: {
      stage_title: "Untersuchungsrahmen",
      task_title: "Forstbeh\u00f6rde-Anfrage",
    },
  },
  {
    id: "email-003",
    from: "dr.schmidt@oeko-gutachten.de",
    subject: "Zwischenbericht Artenschutzkartierung \u2013 Fledermausdaten",
    body: "Sehr geehrte Projektleitung,\n\nanbei der Zwischenbericht Nr. 3 der Fledermaus-Detektorbegehungen (Zeitraum: Okt. 2025 \u2013 Jan. 2026, Stand: 60%).\n\nA) Artenspektrum (4 von gesch\u00e4tzt 6-8 Arten)\n- Gro\u00dfes Mausohr (Myotis myotis) \u2013 FFH Anh. II/IV, 12 von 18 Transekten\n- Zwergfledermaus (Pipistrellus pipistrellus) \u2013 FFH Anh. IV, alle Transekte\n- Breitfl\u00fcgelfledermaus (Eptesicus serotinus) \u2013 vereinzelt, siedlungsnah\n- Gro\u00dfer Abendsegler (Nyctalus noctula) \u2013 \u00dcberfl\u00fcge, Herbstzug relevant\n\nB) Quartiere\n- km 34,5: Wochenstube Gro\u00dfes Mausohr BEST\u00c4TIGT (alte Eiche, ~40-60 Ind.)\n  \u2192 H\u00f6chster Schutzstatus (\u00a7 44 Abs. 1 Nr. 3 BNatSchG), erhebliche Planungsrelevanz\n- km 28,3: Quartierverdacht Zwergfledermaus (Best\u00e4tigung KW 8)\n\nC) Flugrouten\n- Hauptflugroute: Waldkante km 12-18 (Transferfl\u00fcge Gro\u00dfes Mausohr)\n- Jagdhabitate: Feuchtwiesen km 15,5, Streuobstwiese km 17,2\n- Kollisionsrisiko Freileitung: HOCH im Bereich km 14-16\n\nD) Vorl\u00e4ufige Empfehlungen\n- Erdkabel-Vorzug km 12-18 (Kollisionsvermeidung)\n- Bauzeitenbeschr\u00e4nkung 200m um Quartiere (April-August)\n- CEF-Ma\u00dfnahme: 20 Fledermausk\u00e4sten\n\nAbschlussbericht bis 20.02.2026.\n\nBeste Gr\u00fc\u00dfe\nDr. Anna Schmidt\n\u00d6kologische Fachgutachten Schmidt & Partner",
    received_at: "2026-02-05T16:45:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Zwischenbericht_Fledermaus_Nr3_2026.pdf", type: "pdf", size: "4.7 MB" },
      { name: "Karte_Fledermaus_Nachweise.pdf", type: "pdf", size: "2.1 MB" },
      { name: "Transektdaten_Rohdaten.xlsx", type: "xlsx", size: "0.8 MB" },
    ],
    ai_suggestion: {
      stage_title: "Untersuchungsrahmen",
      task_title: "Artenschutz-Vorpr\u00fcfung",
    },
  },
  {
    id: "email-004",
    from: "mueller.k@demohausen.de",
    subject: "Anfrage Erdkabelverlegung \u2013 Auswirkungen auf Gemeindestra\u00dfe",
    body: "Sehr geehrte Damen und Herren,\n\nals B\u00fcrgermeisterin der Gemeinde Demohausen wende ich mich bezgl. der Erdkabelverlegung \"Nord-S\u00fcd-Link\" (Gemarkung Demohausen, Fl. 887/3, 887/5, 888/1, 889/2).\n\nDer Gemeinderat hat am 15.01.2026 folgende Fragen formuliert:\n\n1. Bauphase\n- Wie lang dauert die Bauphase an der Gemeindestra\u00dfe \"Am Wiesengrund\" (DH-14)?\n- In welchem Zeitraum sind Hauptbauarbeiten geplant?\n- Kann au\u00dferhalb der Erntesaison (Juni-Sept.) gebaut werden?\n\n2. Verkehrsf\u00fchrung\n- Vollsperrung oder Behelfsumfahrung?\n- Erreichbarkeit der Betriebe Huber (Fl. 887/5) und Meier (Fl. 889/2)?\n- Rettungsfahrzeug-Zufahrt gesichert?\n\n3. Wiederherstellung & Kosten\n- Kostentr\u00e4ger f\u00fcr Stra\u00dfenwiederherstellung?\n- Wiederherstellung auf Vor-Bau-Standard oder Ausbau?\n- Haftung f\u00fcr Folgesch\u00e4den (Setzungssch\u00e4den)?\n\n4. B\u00fcrgerbeteiligung\n- Informationsveranstaltung geplant? Wann?\n- Feste Ansprechperson w\u00e4hrend Bauphase?\n\n5. Entsch\u00e4digung Landwirtschaft\n- Entsch\u00e4digungsregelungen f\u00fcr nicht bewirtschaftbare Fl\u00e4chen?\n- Vorab-Vereinbarung Flurschadensregulierung?\n\nAntwort bitte bis 15.03.2026 (Gemeinderatssitzung 20.03.2026).\n\nMit freundlichen Gr\u00fc\u00dfen\nKatrin M\u00fcller, B\u00fcrgermeisterin\nGemeinde Demohausen",
    received_at: "2026-02-06T08:20:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Gemeinderatsbeschluss_15012026.pdf", type: "pdf", size: "0.4 MB" },
      { name: "Lageplan_betroffene_Flurst\u00fccke.pdf", type: "pdf", size: "1.8 MB" },
    ],
    ai_suggestion: {
      stage_title: "Korridorfindung",
      task_title: "GIS-Verschneidung",
    },
  },
];

interface PanelProps {
  project: Project;
  template: ProcessTemplate;
  onOpenFullView?: () => void;
}

export default function EmailPanel({
  project,
  template,
  onOpenFullView,
}: PanelProps) {
  const [emails, setEmails] = useState<Email[]>(MOCK_EMAILS);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const t = useT();
  const language = useWorkflowStore((s) => s.language);

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
    <div className="flex flex-col rounded-xl border border-gray-200 bg-white shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-100 px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Inbox className="h-4 w-4 text-blue-600" />
          <h3 className="text-sm font-bold text-gray-900">
            {t("email.panel.title")}
          </h3>
          {unreadCount > 0 && (
            <span className="rounded-full bg-red-500 px-1.5 py-0.5 text-[9px] font-bold text-white">
              {unreadCount}
            </span>
          )}
        </div>
        {onOpenFullView && (
          <button
            onClick={onOpenFullView}
            className="text-[10px] text-blue-600 hover:underline"
          >
            {t("email.fullView")}
          </button>
        )}
      </div>

      {/* AI Synthesis */}
      <div className="flex items-start gap-2 border-b border-gray-100 bg-violet-50/50 px-4 py-2">
        <Sparkles className="mt-0.5 h-3 w-3 shrink-0 text-violet-500" />
        <p className="text-[10px] leading-relaxed text-violet-700">
          <span className="font-semibold">{t("email.synthesis.title")}:</span>{" "}
          {language === "de" ? SYNTHESIS_DE : SYNTHESIS_EN}
        </p>
      </div>

      {/* Email list */}
      <div className="max-h-[280px] overflow-y-auto">
        {emails.map((email) => {
          const isExpanded = expandedId === email.id;
          return (
            <div
              key={email.id}
              className={`border-b border-gray-50 ${
                email.filed
                  ? "bg-emerald-50/30"
                  : !email.read
                    ? "bg-blue-50/30"
                    : ""
              }`}
            >
              <button
                onClick={() => toggleExpand(email.id)}
                className="flex w-full items-start gap-2 px-4 py-2 text-left transition hover:bg-gray-50"
              >
                {email.filed ? (
                  <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-500" />
                ) : email.read ? (
                  <MailOpen className="mt-0.5 h-3.5 w-3.5 shrink-0 text-gray-400" />
                ) : (
                  <Mail className="mt-0.5 h-3.5 w-3.5 shrink-0 text-blue-500" />
                )}
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1">
                    <span
                      className={`text-xs ${
                        !email.read
                          ? "font-bold text-gray-900"
                          : "font-medium text-gray-600"
                      }`}
                    >
                      {email.from.split("@")[0]}
                    </span>
                    <span className="text-[9px] text-gray-400">
                      {new Date(email.received_at).toLocaleDateString(
                        language === "de" ? "de-DE" : "en-US",
                        { day: "2-digit", month: "2-digit" }
                      )}
                    </span>
                    {email.attachments.length > 0 && (
                      <span className="flex items-center gap-0.5 text-[9px] text-gray-400">
                        <Paperclip className="h-2.5 w-2.5" />
                        {email.attachments.length}
                      </span>
                    )}
                  </div>
                  <p
                    className={`text-[11px] leading-tight ${
                      !email.read
                        ? "font-semibold text-gray-800"
                        : "text-gray-500"
                    }`}
                  >
                    {email.subject}
                  </p>
                </div>
                {isExpanded ? (
                  <ChevronUp className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" />
                ) : (
                  <ChevronDown className="mt-0.5 h-3 w-3 shrink-0 text-gray-400" />
                )}
              </button>

              {/* Expanded */}
              {isExpanded && (
                <div className="border-t border-gray-100 px-4 pb-3 pt-2">
                  <pre className="mb-2 max-h-32 overflow-y-auto whitespace-pre-wrap text-[11px] font-sans leading-relaxed text-gray-600">
                    {email.body}
                  </pre>

                  {/* Attachments */}
                  {email.attachments.length > 0 && (
                    <div className="mb-2 flex flex-wrap gap-1">
                      {email.attachments.map((att) => (
                        <span
                          key={att.name}
                          className="flex items-center gap-1 rounded border border-gray-200 bg-gray-50 px-1.5 py-0.5 text-[9px] text-gray-500"
                        >
                          <FileText className="h-2.5 w-2.5" />
                          {att.name.length > 25
                            ? att.name.slice(0, 22) + "..."
                            : att.name}{" "}
                          ({att.size})
                        </span>
                      ))}
                    </div>
                  )}

                  {/* AI categorization + file button */}
                  {email.ai_suggestion && (
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-1.5 text-[10px] text-violet-600">
                        <Sparkles className="h-3 w-3" />
                        <span>
                          AI: {email.ai_suggestion.stage_title} &rarr;{" "}
                          {email.ai_suggestion.task_title}
                        </span>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          fileEmail(email.id);
                        }}
                        disabled={email.filed}
                        className={`ml-auto flex items-center gap-1 rounded px-2 py-0.5 text-[9px] font-medium transition ${
                          email.filed
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-violet-100 text-violet-700 hover:bg-violet-200"
                        }`}
                      >
                        {email.filed ? (
                          <>
                            <Check className="h-2.5 w-2.5" />
                            {t("email.aiFiled")}
                          </>
                        ) : (
                          <>
                            <ArrowRight className="h-2.5 w-2.5" />
                            {t("email.aiFile")}
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
