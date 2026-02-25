import {
  AlertTriangle,
  ArrowRight,
  Check,
  ChevronDown,
  ChevronUp,
  FileText,
  Inbox,
  Loader2,
  Mail,
  MailOpen,
  MessageSquare,
  Paperclip,
  Send,
  Sparkles,
  X,
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

interface EmailAction {
  action_type: string;
  label: string;
  description: string;
  document_id?: string;
}

export interface Email {
  id: string;
  from: string;
  subject: string;
  body: string;
  received_at: string;
  read: boolean;
  filed: boolean;
  attachments: Attachment[];
  ai_suggestion?: {
    stage_index: number;
    stage_title: string;
    task_template_id: string;
    task_title: string;
    reason: string;
  };
  ai_actions?: EmailAction[];
}

const SYNTHESIS_DE =
  "4 E-Mails eingegangen. BNetzA best\u00e4tigt Antragseingang (Vollst\u00e4ndigkeitspr\u00fcfung 4 Wochen). AELF fordert 3 Waldumwandlungs-Unterlagen nach (Frist: 28.02. \u2013 DRINGEND). Artenschutz-Zwischenbericht: 4 Fledermausarten, Wochenstube km 34,5 best\u00e4tigt \u2013 Planungsrelevanz hoch. Gemeinde Demohausen: 5 Fragenkomplexe Erdkabelverlegung (Antwort bis 15.03.).";
const SYNTHESIS_EN =
  "4 emails received. BNetzA confirms application receipt (completeness check 4 weeks). Forestry office requests 3 forest conversion documents (deadline: Feb 28 \u2013 URGENT). Species protection interim report: 4 bat species, roost at km 34.5 confirmed \u2013 high planning relevance. Municipality Demohausen: 5 question areas on underground cabling (response by Mar 15).";

const MOCK_EMAILS: Email[] = [
  {
    id: "email-001",
    from: "netzausbau@bnetza.de",
    subject: "Eingangsbest\u00e4tigung Antrag Bundesfachplanung \u2013 P-DE-TSO-001",
    body: "Sehr geehrte Damen und Herren,\n\nhiermit best\u00e4tigen wir den Eingang Ihres Antrags auf Bundesfachplanung gem\u00e4\u00df \u00a7 6 NABEG f\u00fcr das Vorhaben \"Nord-S\u00fcd-Link Abschnitt Demo A\" (Az.: BFP-2026-001).\n\nFolgende Verfahrensschritte teilen wir Ihnen mit:\n\n1. Vollst\u00e4ndigkeitspr\u00fcfung\nDie eingereichten Unterlagen werden innerhalb von 4 Wochen gepr\u00fcft. Eingereicht wurden:\n- Antrag auf Bundesfachplanung (Formblatt BFP-A, 47 Seiten)\n- Erl\u00e4uterungsbericht mit Vorschlag Untersuchungsrahmen (128 Seiten)\n- \u00dcbersichtskarte Trassenkorridore 1:100.000\n- UVP-Bericht (Vorentwurf)\n- Natura 2000-Vorpr\u00fcfung\n\n2. Antragskonferenz\nNach positiver Pr\u00fcfung wird die Antragskonferenz gem\u00e4\u00df \u00a7 7 NABEG einberufen. Voraussichtlicher Termin: KW 14-16/2026.\n\n3. Festlegung Untersuchungsrahmen\nAuf Grundlage der Antragskonferenz wird der Untersuchungsrahmen gem\u00e4\u00df \u00a7 7 Abs. 4 NABEG festgelegt (Frist: 2 Monate).\n\nBitte beachten Sie, dass gem\u00e4\u00df \u00a7 6 Abs. 3 NABEG weitere Unterlagen nachgefordert werden k\u00f6nnen.\n\nAnsprechpartner: Dr. Thomas Weber, Referat N3\nTel.: +49 (0)228 14-6789\n\nMit freundlichen Gr\u00fc\u00dfen\nBundesnetzagentur\nAbteilung Netzausbau",
    received_at: "2026-02-04T09:15:00",
    read: true,
    filed: false,
    attachments: [
      { name: "Eingangsbest\u00e4tigung_BFP-2026-001.pdf", type: "pdf", size: "0.3 MB" },
    ],
    ai_suggestion: {
      stage_index: 0,
      stage_title: "Scope & Rechtsrahmen",
      task_template_id: "s1_t1",
      task_title: "Rechtsrahmen & Zust\u00e4ndigkeit",
      reason: "Bezug auf \u00a7 6 NABEG Antrag, Eingangsbest\u00e4tigung der BNetzA",
    },
    ai_actions: [
      { action_type: "assign_task", label: "Aufgabe zuordnen", description: "Zu Scope & Rechtsrahmen zuordnen" },
      { action_type: "respond", label: "Antworten", description: "Best\u00e4tigung des Erhalts senden" },
    ],
  },
  {
    id: "email-002",
    from: "forst@aelf-musterstadt.bayern.de",
    subject: "R\u00fcckfrage Waldumwandlung \u2013 Unterlagen unvollst\u00e4ndig",
    body: "Sehr geehrte Damen und Herren,\n\nbezugnehmend auf Ihre Anfrage zur Waldumwandlungsgenehmigung gem\u00e4\u00df Art. 9 BayWaldG vom 28.01.2026 (Az.: AELF-MS-2026-0342) teilen wir mit, dass die Unterlagen nach Fachpr\u00fcfung unvollst\u00e4ndig sind.\n\nFehlende Unterlagen:\n\n1. Detailkarte der Waldtypen\nErforderlich im Ma\u00dfstab 1:5.000 (eingereicht: nur 1:10.000) mit:\n- Baumartenzusammensetzung je Bestand\n- Altersklassen und Bestockungsgrad\n- Schutzstatus (Bannwald, Schutzwald, Erholungswald)\n- Biotopb\u00e4ume und Totholzanteile\n\n2. Trassenalternativen im Waldbereich\nGem\u00e4\u00df Art. 9 Abs. 4 BayWaldG ist nachzuweisen, dass keine zumutbare Alternative besteht. Detaillierte Variantenuntersuchung erforderlich f\u00fcr km 8,2\u201312,7 und km 18,1\u201321,3.\n\n3. Aktualisiertes Waldausgleichskonzept\nStand September 2024 veraltet. Bitte \u00fcberarbeiten mit:\n- Aktuelle Fl\u00e4chenverf\u00fcgbarkeit (Kataster Stand 01.01.2026)\n- Erstaufforstungsfaktor 1:2 f\u00fcr Bannwaldbereiche\n- Zeitplanung Aufforstungsma\u00dfnahmen\n\nFrist: 28.02.2026. Bei Nichteinhaltung ruht die Bearbeitung.\nFristverl\u00e4ngerung auf begr\u00fcndeten Antrag m\u00f6glich.\n\nR\u00fcckfragen: Frau Dipl.-Ing. Sabine Forster, Tel.: 08421/70-234\n\nMit freundlichen Gr\u00fc\u00dfen\nAmt f\u00fcr Ern\u00e4hrung, Landwirtschaft und Forsten Musterstadt\nBereich Forsten",
    received_at: "2026-02-05T14:30:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Pr\u00fcfvermerk_Waldumwandlung_2026-0342.pdf", type: "pdf", size: "1.2 MB" },
      { name: "Checkliste_fehlende_Unterlagen.xlsx", type: "xlsx", size: "0.1 MB" },
    ],
    ai_suggestion: {
      stage_index: 2,
      stage_title: "Untersuchungsrahmen",
      task_template_id: "s3_t3",
      task_title: "Forstbeh\u00f6rde-Anfrage",
      reason: "Direkte Antwort auf Forstanfrage, Nachforderung fehlender Unterlagen",
    },
    ai_actions: [
      { action_type: "assign_task", label: "Aufgabe zuordnen", description: "Zu Forstbeh\u00f6rde-Anfrage zuordnen" },
      { action_type: "send_document", label: "Dokument senden", description: "Waldtypenkarte (DOC-024) nachreichen", document_id: "DOC-024" },
      { action_type: "respond", label: "Antworten", description: "Fristverl\u00e4ngerung beantragen" },
      { action_type: "create_blocker", label: "Blocker erstellen", description: "Fehlende Waldunterlagen als Blocker" },
    ],
  },
  {
    id: "email-003",
    from: "dr.schmidt@oeko-gutachten.de",
    subject: "Zwischenbericht Artenschutzkartierung \u2013 Fledermausdaten",
    body: "Sehr geehrte Projektleitung,\n\nanbei der Zwischenbericht Nr. 3 der Fledermaus-Detektorbegehungen (Zeitraum: Okt. 2025 \u2013 Jan. 2026, Stand: 60%).\n\nA) Artenspektrum (4 von gesch\u00e4tzt 6-8 Arten)\n- Gro\u00dfes Mausohr (Myotis myotis) \u2013 FFH Anh. II/IV, 12 von 18 Transekten\n- Zwergfledermaus (Pipistrellus pipistrellus) \u2013 FFH Anh. IV, alle Transekte\n- Breitfl\u00fcgelfledermaus (Eptesicus serotinus) \u2013 vereinzelt, siedlungsnah\n- Gro\u00dfer Abendsegler (Nyctalus noctula) \u2013 \u00dcberfl\u00fcge, Herbstzug relevant\n\nB) Quartiere\n- km 34,5: Wochenstube Gro\u00dfes Mausohr BEST\u00c4TIGT (alte Eiche, ~40-60 Ind.)\n  \u2192 H\u00f6chster Schutzstatus (\u00a7 44 Abs. 1 Nr. 3 BNatSchG), erhebliche Planungsrelevanz\n- km 28,3: Quartierverdacht Zwergfledermaus (Best\u00e4tigung KW 8)\n- km 41,2: Winterquartiersuche alte Bunkeranlagen ausstehend\n\nC) Flugrouten\n- Hauptflugroute: Waldkante km 12-18 (Transferfl\u00fcge Gro\u00dfes Mausohr)\n- Jagdhabitate: Feuchtwiesen km 15,5, Streuobstwiese km 17,2\n- Kollisionsrisiko Freileitung: HOCH im Bereich km 14-16\n\nD) Vorl\u00e4ufige Empfehlungen\n- Erdkabel-Vorzug km 12-18 (Kollisionsvermeidung)\n- Bauzeitenbeschr\u00e4nkung 200m um Quartiere (April-August)\n- CEF-Ma\u00dfnahme: 20 Fledermausk\u00e4sten\n- \u00d6kologische Baubegleitung bei Trassenfreimachung\n\nAbschlussbericht bis 20.02.2026.\n\nBeste Gr\u00fc\u00dfe\nDr. Anna Schmidt\n\u00d6kologische Fachgutachten Schmidt & Partner\nHauptstra\u00dfe 42, 91054 Erlangen",
    received_at: "2026-02-05T16:45:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Zwischenbericht_Fledermaus_Nr3_2026.pdf", type: "pdf", size: "4.7 MB" },
      { name: "Karte_Fledermaus_Nachweise.pdf", type: "pdf", size: "2.1 MB" },
      { name: "Transektdaten_Rohdaten.xlsx", type: "xlsx", size: "0.8 MB" },
    ],
    ai_suggestion: {
      stage_index: 2,
      stage_title: "Untersuchungsrahmen",
      task_template_id: "s3_t1",
      task_title: "Artenschutz-Vorpr\u00fcfung",
      reason: "Artenschutzkartierung Flederm\u00e4use, direkt relevant f\u00fcr ASP",
    },
    ai_actions: [
      { action_type: "assign_task", label: "Aufgabe zuordnen", description: "Zu Artenschutzbeitrag zuordnen" },
      { action_type: "respond", label: "Antworten", description: "Eingangs- und Dankesbest\u00e4tigung" },
    ],
  },
  {
    id: "email-004",
    from: "mueller.k@demohausen.de",
    subject: "Anfrage Erdkabelverlegung \u2013 Auswirkungen auf Gemeindestra\u00dfe",
    body: "Sehr geehrte Damen und Herren,\n\nals B\u00fcrgermeisterin der Gemeinde Demohausen wende ich mich bezgl. der Erdkabelverlegung \"Nord-S\u00fcd-Link\" (Gemarkung Demohausen, Fl. 887/3, 887/5, 888/1, 889/2).\n\nDer Gemeinderat hat am 15.01.2026 folgende Fragen formuliert:\n\n1. Bauphase\n- Wie lang dauert die Bauphase an der Gemeindestra\u00dfe \"Am Wiesengrund\" (DH-14)?\n- In welchem Zeitraum sind Hauptbauarbeiten geplant?\n- Kann au\u00dferhalb der Erntesaison (Juni-Sept.) gebaut werden?\n\n2. Verkehrsf\u00fchrung\n- Vollsperrung oder Behelfsumfahrung?\n- Erreichbarkeit der Betriebe Huber (Fl. 887/5) und Meier (Fl. 889/2)?\n- Rettungsfahrzeug-Zufahrt gesichert?\n\n3. Wiederherstellung & Kosten\n- Kostentr\u00e4ger f\u00fcr Stra\u00dfenwiederherstellung und Wirtschaftswege?\n- Wiederherstellung auf Vor-Bau-Standard oder Ausbau?\n- Haftung f\u00fcr Folgesch\u00e4den (Setzungssch\u00e4den)?\n\n4. B\u00fcrgerbeteiligung\n- Informationsveranstaltung geplant? Wann?\n- Feste Ansprechperson w\u00e4hrend Bauphase?\n- Informationsbroschu00fcre fu00fcr Anwohner verfu00fcgbar?\n\n5. Entsch\u00e4digung Landwirtschaft\n- Entsch\u00e4digungsregelungen f\u00fcr nicht bewirtschaftbare Fl\u00e4chen?\n- Vorab-Vereinbarung Flurschadensregulierung?\n\nAntwort bitte bis 15.03.2026 (Gemeinderatssitzung 20.03.2026).\n\nMit freundlichen Gr\u00fc\u00dfen\nKatrin M\u00fcller, B\u00fcrgermeisterin\nGemeinde Demohausen\nRathausplatz 1, 36251 Demohausen\nTel.: 06625/921-0",
    received_at: "2026-02-06T08:20:00",
    read: false,
    filed: false,
    attachments: [
      { name: "Gemeinderatsbeschluss_15012026.pdf", type: "pdf", size: "0.4 MB" },
      { name: "Lageplan_betroffene_Flurst\u00fccke.pdf", type: "pdf", size: "1.8 MB" },
    ],
    ai_suggestion: {
      stage_index: 1,
      stage_title: "Korridorfindung",
      task_template_id: "s2_t2",
      task_title: "GIS-Verschneidung",
      reason: "Betrifft Flurst\u00fcck HE-044-887-03, Erdkabelabschnitt bei Demohausen",
    },
    ai_actions: [
      { action_type: "respond", label: "Antworten", description: "Informationsschreiben an Gemeinde" },
      { action_type: "send_document", label: "Dokument senden", description: "Projektsteckbrief (DOC-001) \u00fcbersenden", document_id: "DOC-001" },
      { action_type: "forward", label: "Weiterleiten", description: "An Wegerechtsteam weiterleiten" },
    ],
  },
];

const ACTION_ICONS: Record<string, typeof Mail> = {
  respond: MessageSquare,
  send_document: FileText,
  assign_task: ArrowRight,
  forward: Send,
  create_blocker: AlertTriangle,
};

/* AI-generated response templates per action type */
const AI_RESPONSES: Record<string, string> = {
  respond:
    "Sehr geehrte Damen und Herren,\n\nvielen Dank f\u00fcr Ihre Nachricht. Wir haben Ihr Anliegen zur Kenntnis genommen und werden uns zeitnah mit einer ausf\u00fchrlichen Stellungnahme bei Ihnen melden.\n\nMit freundlichen Gr\u00fc\u00dfen\nProjektteam Nord-S\u00fcd-Link",
  send_document:
    "Anbei \u00fcbersenden wir Ihnen das angeforderte Dokument. Bitte best\u00e4tigen Sie den Eingang.\n\nMit freundlichen Gr\u00fc\u00dfen\nProjektteam Nord-S\u00fcd-Link",
  forward:
    "Zur Bearbeitung/Kenntnisnahme. Bitte um R\u00fcckmeldung bis Ende der Woche.",
};

interface ActiveAction {
  email: Email;
  action: EmailAction;
}

interface Props {
  project: Project;
  template: ProcessTemplate;
  isOpen: boolean;
  onClose: () => void;
}

/* ---------- Action Dialog with AI Fill ---------- */
function ActionDialog({
  activeAction,
  onExecute,
  onClose,
}: {
  activeAction: ActiveAction;
  onExecute: () => void;
  onClose: () => void;
}) {
  const { email, action } = activeAction;
  const t = useT();
  const [text, setText] = useState("");
  const [filling, setFilling] = useState(false);

  const handleAIFill = () => {
    setFilling(true);
    setTimeout(() => {
      setText(AI_RESPONSES[action.action_type] ?? "");
      setFilling(false);
    }, 400);
  };

  const renderContent = () => {
    switch (action.action_type) {
      case "respond":
        return (
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.to")}</label>
              <p className="mt-0.5 rounded border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700">
                {email.from}
              </p>
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.subject")}</label>
              <p className="mt-0.5 rounded border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700">
                Re: {email.subject}
              </p>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-gray-500">{t("email.action.message")}</label>
                <button
                  onClick={handleAIFill}
                  disabled={filling}
                  className="flex items-center gap-1 rounded-md bg-violet-50 px-2 py-0.5 text-[10px] font-medium text-violet-700 transition hover:bg-violet-100 disabled:opacity-50"
                >
                  {filling ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />}
                  {t("email.aiFill")}
                </button>
              </div>
              <textarea
                rows={6}
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
          </div>
        );

      case "send_document":
        return (
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.to")}</label>
              <p className="mt-0.5 rounded border border-gray-200 bg-gray-50 px-3 py-2 text-sm text-gray-700">
                {email.from}
              </p>
            </div>
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-3">
              <div className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-sm font-medium text-blue-900">{action.document_id ?? "DOC"}</p>
                  <p className="text-xs text-blue-600">{action.description}</p>
                </div>
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-gray-500">{t("email.action.message")}</label>
                <button
                  onClick={handleAIFill}
                  disabled={filling}
                  className="flex items-center gap-1 rounded-md bg-violet-50 px-2 py-0.5 text-[10px] font-medium text-violet-700 transition hover:bg-violet-100 disabled:opacity-50"
                >
                  {filling ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />}
                  {t("email.aiFill")}
                </button>
              </div>
              <textarea
                rows={3}
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
          </div>
        );

      case "assign_task":
        return (
          <div className="space-y-3">
            {email.ai_suggestion && (
              <div className="rounded-lg border border-violet-200 bg-violet-50 p-4">
                <p className="text-xs font-medium text-violet-500">{t("email.action.assignTo")}</p>
                <p className="mt-1 text-sm font-semibold text-violet-900">
                  {email.ai_suggestion.stage_title}
                </p>
                <p className="flex items-center gap-1 text-sm text-violet-700">
                  <ArrowRight className="h-3 w-3" />
                  {email.ai_suggestion.task_title}
                </p>
                <p className="mt-2 text-xs text-violet-600">{email.ai_suggestion.reason}</p>
              </div>
            )}
          </div>
        );

      case "forward":
        return (
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.forwardTo")}</label>
              <input
                type="text"
                className="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="team@example.de"
              />
            </div>
            <div>
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-gray-500">{t("email.action.note")}</label>
                <button
                  onClick={handleAIFill}
                  disabled={filling}
                  className="flex items-center gap-1 rounded-md bg-violet-50 px-2 py-0.5 text-[10px] font-medium text-violet-700 transition hover:bg-violet-100 disabled:opacity-50"
                >
                  {filling ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />}
                  {t("email.aiFill")}
                </button>
              </div>
              <textarea
                rows={2}
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div className="rounded border border-gray-200 bg-gray-50 p-3">
              <p className="text-xs font-medium text-gray-500">Original:</p>
              <p className="mt-1 text-xs text-gray-600">
                {email.from} &mdash; {email.subject}
              </p>
            </div>
          </div>
        );

      case "create_blocker":
        return (
          <div className="space-y-3">
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.blockerTitle")}</label>
              <input
                type="text"
                className="mt-0.5 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                defaultValue={action.description}
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">{t("email.action.blockerSource")}</label>
              <p className="mt-0.5 rounded border border-gray-200 bg-gray-50 px-3 py-2 text-xs text-gray-600">
                {email.from} &mdash; {email.subject}
              </p>
            </div>
          </div>
        );

      default:
        return <p className="text-sm text-gray-500">{action.description}</p>;
    }
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40" onClick={onClose}>
      <div className="mx-4 w-full max-w-lg rounded-xl bg-white shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between border-b border-gray-100 px-5 py-4">
          <div className="flex items-center gap-2">
            {(() => {
              const Icon = ACTION_ICONS[action.action_type] ?? ArrowRight;
              return <Icon className="h-5 w-5 text-violet-600" />;
            })()}
            <h3 className="text-base font-bold text-gray-900">{action.label}</h3>
          </div>
          <button onClick={onClose} className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="px-5 py-4">{renderContent()}</div>
        <div className="flex items-center justify-end gap-2 border-t border-gray-100 px-5 py-3">
          <button
            onClick={onClose}
            className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-600 transition hover:bg-gray-50"
          >
            {t("email.action.cancel")}
          </button>
          <button
            onClick={onExecute}
            className="rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-violet-700"
          >
            {action.label}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ---------- Main Component ---------- */
export default function EmailInbox({ project, template, isOpen, onClose }: Props) {
  const [emails, setEmails] = useState<Email[]>(MOCK_EMAILS);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [executedActions, setExecutedActions] = useState<Set<string>>(new Set());
  const [activeAction, setActiveAction] = useState<ActiveAction | null>(null);
  const t = useT();
  const language = useWorkflowStore((s) => s.language);

  if (!isOpen) return null;

  const unreadCount = emails.filter((e) => !e.read).length;

  const markRead = (id: string) => {
    setEmails((prev) => prev.map((e) => (e.id === id ? { ...e, read: true } : e)));
  };

  const fileEmail = (id: string) => {
    setEmails((prev) => prev.map((e) => (e.id === id ? { ...e, filed: true, read: true } : e)));
  };

  const toggleExpand = (id: string) => {
    const email = emails.find((e) => e.id === id);
    if (email && !email.read) markRead(id);
    setExpandedId((prev) => (prev === id ? null : id));
  };

  const handleExecuteAction = () => {
    if (!activeAction) return;
    const key = `${activeAction.email.id}-${activeAction.action.action_type}`;
    setExecutedActions((prev) => new Set(prev).add(key));
    if (activeAction.action.action_type === "assign_task") {
      fileEmail(activeAction.email.id);
    }
    setActiveAction(null);
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
          <button onClick={onClose} className="rounded-lg p-2 text-gray-400 transition hover:bg-gray-100 hover:text-gray-600">
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* AI Synthesis */}
        <div className="flex items-start gap-2 border-b border-gray-100 bg-violet-50/50 px-5 py-3">
          <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-violet-500" />
          <div>
            <p className="text-xs font-semibold text-violet-800">{t("email.synthesis.title")}</p>
            <p className="mt-0.5 text-xs leading-relaxed text-violet-700">
              {language === "de" ? SYNTHESIS_DE : SYNTHESIS_EN}
            </p>
          </div>
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
                      <span className={`text-sm ${!email.read ? "font-bold text-gray-900" : "font-medium text-gray-700"}`}>
                        {email.from}
                      </span>
                      <span className="text-[10px] text-gray-400">
                        {new Date(email.received_at).toLocaleDateString(
                          language === "de" ? "de-DE" : "en-US",
                          { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" }
                        )}
                      </span>
                      {email.attachments.length > 0 && (
                        <span className="flex items-center gap-0.5 text-[10px] text-gray-400">
                          <Paperclip className="h-3 w-3" />
                          {email.attachments.length}
                        </span>
                      )}
                    </div>
                    <p className={`mt-0.5 text-sm ${!email.read ? "font-semibold text-gray-800" : "text-gray-600"}`}>
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

                    {/* Attachments */}
                    {email.attachments.length > 0 && (
                      <div className="mt-3">
                        <p className="mb-1.5 flex items-center gap-1.5 text-xs font-semibold text-gray-500">
                          <Paperclip className="h-3.5 w-3.5" />
                          {t("email.attachments")} ({email.attachments.length})
                        </p>
                        <div className="flex flex-wrap gap-2">
                          {email.attachments.map((att) => (
                            <div
                              key={att.name}
                              className="flex items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 px-3 py-2"
                            >
                              <FileText className="h-4 w-4 text-gray-400" />
                              <div>
                                <p className="text-xs font-medium text-gray-700">{att.name}</p>
                                <p className="text-[10px] text-gray-400">{att.size}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* AI suggestion + file button */}
                    {email.ai_suggestion && (
                      <div className="mt-3 rounded-lg border border-violet-200 bg-violet-50 p-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Sparkles className="h-4 w-4 text-violet-600" />
                            <span className="text-xs font-semibold text-violet-800">
                              {t("email.aiAssignment")}
                            </span>
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              fileEmail(email.id);
                            }}
                            disabled={email.filed}
                            className={`flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition ${
                              email.filed
                                ? "bg-emerald-100 text-emerald-700"
                                : "bg-violet-600 text-white hover:bg-violet-700"
                            }`}
                          >
                            {email.filed ? (
                              <>
                                <Check className="h-3.5 w-3.5" />
                                {t("email.aiFiled")}
                              </>
                            ) : (
                              <>
                                <ArrowRight className="h-3.5 w-3.5" />
                                {t("email.aiFile")}
                              </>
                            )}
                          </button>
                        </div>
                        <p className="mt-1 text-xs text-violet-700">
                          <span className="font-medium">{t("email.phase")}</span>{" "}
                          {email.ai_suggestion.stage_title} &rarr;{" "}
                          <span className="font-medium">{email.ai_suggestion.task_title}</span>
                        </p>
                        <p className="mt-0.5 text-[10px] text-violet-600">{email.ai_suggestion.reason}</p>
                      </div>
                    )}

                    {/* AI Action buttons — always visible, even after filing */}
                    {email.ai_actions && email.ai_actions.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {email.ai_actions.map((action) => {
                          const ActionIcon = ACTION_ICONS[action.action_type] ?? ArrowRight;
                          const key = `${email.id}-${action.action_type}`;
                          const isExecuted = executedActions.has(key);
                          return (
                            <button
                              key={action.action_type}
                              onClick={(e) => {
                                e.stopPropagation();
                                if (!isExecuted) setActiveAction({ email, action });
                              }}
                              disabled={isExecuted}
                              className={`flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-medium transition ${
                                isExecuted
                                  ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                                  : "border-violet-200 bg-white text-violet-700 hover:bg-violet-50"
                              }`}
                            >
                              {isExecuted ? <Check className="h-3.5 w-3.5" /> : <ActionIcon className="h-3.5 w-3.5" />}
                              {action.label}
                            </button>
                          );
                        })}
                      </div>
                    )}

                    {email.filed && (
                      <div className="mt-2 flex items-center gap-2 text-xs text-emerald-700">
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

      {/* Action dialog (secondary window) */}
      {activeAction && (
        <ActionDialog
          activeAction={activeAction}
          onExecute={handleExecuteAction}
          onClose={() => setActiveAction(null)}
        />
      )}
    </div>
  );
}
