from __future__ import annotations

import copy

from .models import (
    FormField,
    ProcessTemplate,
    Project,
    StageInstance,
    StageStatus,
    StageTemplate,
    TaskInstance,
    TaskStatus,
    TaskTemplate,
    VerfahrensPfad,
)

# ---------------------------------------------------------------------------
# NABEG process template – German (3 stages)
# ---------------------------------------------------------------------------

NABEG_TEMPLATE_DE = ProcessTemplate(
    pfad=VerfahrensPfad.NABEG,
    label="NABEG \u2013 Bundesfachplanung (H\u00f6chstspannung)",
    description="Verfahren nach dem Netzausbaubeschleunigungsgesetz f\u00fcr H\u00f6chstspannungsleitungen (ab 220 kV).",
    stages=[
        # -- Stage 1: Scope & Rechtsrahmen --
        StageTemplate(
            id="s1_scope_recht",
            title="Scope & Rechtsrahmen",
            law_reference="\u00a7 4ff. NABEG / BBPlG",
            description="Identifikation des anwendbaren Rechtsrahmens, Erstellung des Projektsteckbriefs und initiale Stakeholder-Erfassung.",
            info_text=(
                "\u00a7 4 NABEG i.V.m. BBPlG: Die im Bundesbedarfsplangesetz als l\u00e4nder\u00fcbergreifend "
                "oder grenz\u00fcberschreitend gekennzeichneten Vorhaben unterliegen dem NABEG. "
                "Der Vorhabentr\u00e4ger identifiziert den anwendbaren Rechtsrahmen und bereitet "
                "die erforderlichen Antragsunterlagen vor."
            ),
            tasks=[
                TaskTemplate(
                    id="s1_t1",
                    title="Anwendbares Recht identifizieren",
                    description="Pr\u00fcfen Sie den anwendbaren Rechtsrahmen (NABEG vs. EnWG) und identifizieren Sie die zust\u00e4ndige Beh\u00f6rde.",
                    form_fields=[
                        FormField(name="rechtsrahmen", label="Anwendbarer Rechtsrahmen", type="textarea"),
                        FormField(name="zustaendige_behoerde", label="Zust\u00e4ndige Beh\u00f6rde", type="text"),
                        FormField(name="begruendung", label="Begr\u00fcndung der Zuordnung", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t2",
                    title="Projektsteckbrief erstellen",
                    description="Erstellen Sie den Projektsteckbrief mit allen technischen und r\u00e4umlichen Eckdaten.",
                    form_fields=[
                        FormField(name="vorhaben_titel", label="Vorhabenbezeichnung", type="text"),
                        FormField(name="technologie", label="Technologie & Spannungsebene", type="text"),
                        FormField(name="trassenlaenge", label="Trassenl\u00e4nge", type="text"),
                        FormField(name="bundeslaender", label="Betroffene Bundesl\u00e4nder", type="text"),
                        FormField(name="zusammenfassung", label="Projektzusammenfassung", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t3",
                    title="Stakeholder-Ersterfassung durchf\u00fchren",
                    description="Identifizieren Sie alle relevanten Stakeholder: Beh\u00f6rden, Grundeigent\u00fcmer, Verb\u00e4nde.",
                    form_fields=[
                        FormField(name="behoerden", label="Beteiligte Beh\u00f6rden", type="textarea"),
                        FormField(name="eigentuemer", label="Betroffene Grundeigent\u00fcmer", type="textarea"),
                        FormField(name="verbaende", label="Relevante Verb\u00e4nde & T\u00f6B", type="textarea"),
                    ],
                ),
            ],
        ),
        # -- Stage 2: Korridorfindung --
        StageTemplate(
            id="s2_korridor",
            title="Korridorfindung",
            law_reference="\u00a7 6 NABEG",
            description="Definition und Bewertung von Trassenkorridoralternativen, GIS-Analyse und Erstellung des Korridoralternativenberichts.",
            info_text=(
                "\u00a7 6 NABEG: Der Vorhabentr\u00e4ger beantragt die Bundesfachplanung bei der "
                "Bundesnetzagentur. Hierzu geh\u00f6rt die Darstellung der in Betracht kommenden "
                "Trassenkorridore mit einer Bewertung der Raumvertr\u00e4glichkeit. Die BNetzA "
                "f\u00fchrt anschlie\u00dfend eine Antragskonferenz durch."
            ),
            tasks=[
                TaskTemplate(
                    id="s2_t1",
                    title="Korridoralternativen definieren",
                    description="Definieren Sie mindestens zwei Trassenkorridore mit technischer Bewertung.",
                    form_fields=[
                        FormField(name="korridor_a", label="Korridor A \u2013 Beschreibung", type="textarea"),
                        FormField(name="korridor_b", label="Korridor B \u2013 Beschreibung", type="textarea"),
                        FormField(name="vorzugskorridor", label="Vorzugskorridor", type="text"),
                        FormField(name="begruendung_auswahl", label="Begr\u00fcndung der Vorzugswahl", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s2_t2",
                    title="GIS-Verschneidung durchf\u00fchren",
                    description="F\u00fchren Sie eine GIS-gest\u00fctzte Raumanalyse mit Schutzgebiets- und Infrastruktur-Layern durch.",
                    form_fields=[
                        FormField(name="schutzgebiete", label="Betroffene Schutzgebiete", type="textarea"),
                        FormField(name="waldanteil", label="Waldquerungen", type="textarea"),
                        FormField(name="siedlungsabstand", label="Siedlungsabst\u00e4nde", type="textarea"),
                        FormField(name="konflikte", label="Identifizierte Konflikte", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s2_t3",
                    title="Korridoralternativenbericht erstellen",
                    description="Erstellen Sie den formellen Bericht zum Vergleich der Korridoralternativen.",
                    form_fields=[
                        FormField(name="methodik", label="Bewertungsmethodik", type="textarea"),
                        FormField(name="bewertungsergebnis", label="Bewertungsergebnis", type="textarea"),
                        FormField(name="empfehlung", label="Empfehlung", type="textarea"),
                    ],
                ),
            ],
        ),
        # -- Stage 3: Untersuchungsrahmen --
        StageTemplate(
            id="s3_untersuchungsrahmen",
            title="Untersuchungsrahmen",
            law_reference="\u00a7 7 NABEG",
            description="Erstellung des Artenschutzbeitrags, der umweltfachlichen Scoping-Unterlage und beh\u00f6rdlicher Anfragen.",
            info_text=(
                "\u00a7 7 NABEG: Die BNetzA legt nach Durchf\u00fchrung der Antragskonferenz den "
                "Untersuchungsrahmen f\u00fcr die Bundesfachplanung fest. Der Vorhabentr\u00e4ger "
                "erstellt die festgelegten Unterlagen, darunter den Umweltbericht und "
                "artenschutzrechtliche Pr\u00fcfungen."
            ),
            tasks=[
                TaskTemplate(
                    id="s3_t1",
                    title="Artenschutzbeitrag erstellen",
                    description="Erstellen Sie den Artenschutzbeitrag (ASP Stufe I/II) mit Kartierungsdaten und Ma\u00dfnahmenkonzept.",
                    form_fields=[
                        FormField(name="betroffene_arten", label="Betroffene Arten", type="textarea"),
                        FormField(name="kartierungsstatus", label="Kartierungsstatus", type="textarea"),
                        FormField(name="vermeidungsmassnahmen", label="Vermeidungsma\u00dfnahmen", type="textarea"),
                        FormField(name="kompensation", label="Kompensationsma\u00dfnahmen", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s3_t2",
                    title="Umweltfachliche Scoping-Unterlage erstellen",
                    description="Erstellen Sie die Scoping-Unterlage f\u00fcr die Umweltvertr\u00e4glichkeitspr\u00fcfung.",
                    form_fields=[
                        FormField(name="schutzgueter", label="Betroffene Schutzg\u00fcter", type="textarea"),
                        FormField(name="untersuchungsraum", label="Untersuchungsraum & Abgrenzung", type="textarea"),
                        FormField(name="methodik_umwelt", label="UVP-Methodik", type="textarea"),
                    ],
                    checklist=[
                        "Schutzgut Mensch bewertet",
                        "Schutzgut Tiere/Pflanzen/Biodiversit\u00e4t bewertet",
                        "Schutzgut Boden/Fl\u00e4che bewertet",
                        "Schutzgut Wasser bewertet",
                        "Schutzgut Klima/Luft bewertet",
                        "Schutzgut Landschaft bewertet",
                        "Schutzgut kulturelles Erbe bewertet",
                    ],
                ),
                TaskTemplate(
                    id="s3_t3",
                    title="Forstbeh\u00f6rdliche Anfrage vorbereiten",
                    description="Erstellen Sie die formelle Anfrage an die zust\u00e4ndige Forstbeh\u00f6rde zur Waldumwandlung.",
                    form_fields=[
                        FormField(name="empfaenger", label="Empf\u00e4nger (Forstbeh\u00f6rde)", type="text"),
                        FormField(name="betreff", label="Betreff", type="text"),
                        FormField(name="anschreiben", label="Anschreiben", type="textarea"),
                        FormField(name="anlagen", label="Anlagenverzeichnis", type="textarea"),
                    ],
                ),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# NABEG process template – English (3 stages)
# ---------------------------------------------------------------------------

NABEG_TEMPLATE_EN = ProcessTemplate(
    pfad=VerfahrensPfad.NABEG,
    label="NABEG \u2013 Federal Sectoral Planning (Extra-High Voltage)",
    description="Procedure under the Grid Expansion Acceleration Act for extra-high voltage lines (220 kV and above).",
    stages=[
        # -- Stage 1: Scope & Legal Framework --
        StageTemplate(
            id="s1_scope_recht",
            title="Scope & Legal Framework",
            law_reference="\u00a7 4ff. NABEG / BBPlG",
            description="Identify the applicable legal framework, create the project profile, and initial stakeholder mapping.",
            info_text=(
                "\u00a7 4 NABEG in conjunction with BBPlG: Projects designated as cross-state or "
                "cross-border in the Federal Requirements Plan are subject to NABEG. The project "
                "developer identifies the applicable legal framework and prepares the required "
                "application documents."
            ),
            tasks=[
                TaskTemplate(
                    id="s1_t1",
                    title="Identify Applicable Law",
                    description="Check the applicable legal framework (NABEG vs. EnWG) and identify the responsible authority.",
                    form_fields=[
                        FormField(name="rechtsrahmen", label="Applicable Legal Framework", type="textarea"),
                        FormField(name="zustaendige_behoerde", label="Responsible Authority", type="text"),
                        FormField(name="begruendung", label="Justification of Assignment", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t2",
                    title="Create Project Profile",
                    description="Create the project profile with all technical and spatial key data.",
                    form_fields=[
                        FormField(name="vorhaben_titel", label="Project Title", type="text"),
                        FormField(name="technologie", label="Technology & Voltage Level", type="text"),
                        FormField(name="trassenlaenge", label="Route Length", type="text"),
                        FormField(name="bundeslaender", label="Affected Federal States", type="text"),
                        FormField(name="zusammenfassung", label="Project Summary", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t3",
                    title="Conduct Initial Stakeholder Mapping",
                    description="Identify all relevant stakeholders: authorities, landowners, associations.",
                    form_fields=[
                        FormField(name="behoerden", label="Involved Authorities", type="textarea"),
                        FormField(name="eigentuemer", label="Affected Landowners", type="textarea"),
                        FormField(name="verbaende", label="Relevant Associations & Public Bodies", type="textarea"),
                    ],
                ),
            ],
        ),
        # -- Stage 2: Corridor Identification --
        StageTemplate(
            id="s2_korridor",
            title="Corridor Identification",
            law_reference="\u00a7 6 NABEG",
            description="Definition and evaluation of route corridor alternatives, GIS analysis, and preparation of the corridor alternatives report.",
            info_text=(
                "\u00a7 6 NABEG: The project developer applies for federal sectoral planning at the "
                "Federal Network Agency. This includes the presentation of potential route corridors "
                "with an assessment of spatial compatibility. The BNetzA then conducts an application "
                "conference."
            ),
            tasks=[
                TaskTemplate(
                    id="s2_t1",
                    title="Define Corridor Alternatives",
                    description="Define at least two route corridors with technical evaluation.",
                    form_fields=[
                        FormField(name="korridor_a", label="Corridor A \u2013 Description", type="textarea"),
                        FormField(name="korridor_b", label="Corridor B \u2013 Description", type="textarea"),
                        FormField(name="vorzugskorridor", label="Preferred Corridor", type="text"),
                        FormField(name="begruendung_auswahl", label="Justification of Preference", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s2_t2",
                    title="Conduct GIS Overlay Analysis",
                    description="Perform a GIS-based spatial analysis with protected area and infrastructure layers.",
                    form_fields=[
                        FormField(name="schutzgebiete", label="Affected Protected Areas", type="textarea"),
                        FormField(name="waldanteil", label="Forest Crossings", type="textarea"),
                        FormField(name="siedlungsabstand", label="Settlement Distances", type="textarea"),
                        FormField(name="konflikte", label="Identified Conflicts", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s2_t3",
                    title="Prepare Corridor Alternatives Report",
                    description="Prepare the formal report comparing corridor alternatives.",
                    form_fields=[
                        FormField(name="methodik", label="Assessment Methodology", type="textarea"),
                        FormField(name="bewertungsergebnis", label="Assessment Result", type="textarea"),
                        FormField(name="empfehlung", label="Recommendation", type="textarea"),
                    ],
                ),
            ],
        ),
        # -- Stage 3: Scope of Investigation --
        StageTemplate(
            id="s3_untersuchungsrahmen",
            title="Scope of Investigation",
            law_reference="\u00a7 7 NABEG",
            description="Preparation of the species protection report, environmental scoping document, and regulatory authority requests.",
            info_text=(
                "\u00a7 7 NABEG: The BNetzA defines the scope of investigation for federal sectoral "
                "planning after conducting the application conference. The project developer prepares "
                "the required documents, including the environmental report and species protection "
                "assessments."
            ),
            tasks=[
                TaskTemplate(
                    id="s3_t1",
                    title="Prepare Species Protection Report",
                    description="Prepare the species protection report (ASP Level I/II) with survey data and mitigation concept.",
                    form_fields=[
                        FormField(name="betroffene_arten", label="Affected Species", type="textarea"),
                        FormField(name="kartierungsstatus", label="Survey Status", type="textarea"),
                        FormField(name="vermeidungsmassnahmen", label="Avoidance Measures", type="textarea"),
                        FormField(name="kompensation", label="Compensation Measures", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s3_t2",
                    title="Prepare Environmental Scoping Document",
                    description="Prepare the scoping document for the Environmental Impact Assessment.",
                    form_fields=[
                        FormField(name="schutzgueter", label="Affected Environmental Assets", type="textarea"),
                        FormField(name="untersuchungsraum", label="Study Area & Delimitation", type="textarea"),
                        FormField(name="methodik_umwelt", label="EIA Methodology", type="textarea"),
                    ],
                    checklist=[
                        "Human welfare assessed",
                        "Wildlife/flora/biodiversity assessed",
                        "Soil/land use assessed",
                        "Water resources assessed",
                        "Climate/air assessed",
                        "Landscape assessed",
                        "Cultural heritage assessed",
                    ],
                ),
                TaskTemplate(
                    id="s3_t3",
                    title="Prepare Forestry Authority Request",
                    description="Prepare the formal request to the responsible forestry authority for forest conversion.",
                    form_fields=[
                        FormField(name="empfaenger", label="Recipient (Forestry Authority)", type="text"),
                        FormField(name="betreff", label="Subject", type="text"),
                        FormField(name="anschreiben", label="Cover Letter", type="textarea"),
                        FormField(name="anlagen", label="List of Attachments", type="textarea"),
                    ],
                ),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# EnWG process template – German
# ---------------------------------------------------------------------------

ENWG_TEMPLATE_DE = ProcessTemplate(
    pfad=VerfahrensPfad.ENWG,
    label="EnWG \u2013 Planfeststellung (110 kV)",
    description="Planfeststellungsverfahren nach dem Energiewirtschaftsgesetz f\u00fcr 110-kV-Leitungen.",
    stages=[
        StageTemplate(
            id="enwg_s1",
            title="Scoping-Termin",
            law_reference="\u00a7 43 EnWG / \u00a7 15 UVPG",
            description="Abstimmung mit der Bezirksregierung \u00fcber den Untersuchungsumfang.",
            info_text="\u00a7 43 EnWG i.V.m. \u00a7 15 UVPG: Scoping-Termin mit der Anh\u00f6rungsbeh\u00f6rde.",
            tasks=[
                TaskTemplate(
                    id="enwg_s1_t1",
                    title="Scoping-Unterlagen vorbereiten",
                    description="Erstellen Sie die Unterlagen f\u00fcr den Scoping-Termin.",
                    form_fields=[
                        FormField(name="behoerde", label="Zust\u00e4ndige Bezirksregierung", type="text"),
                        FormField(name="termin", label="Geplanter Termin", type="date"),
                        FormField(name="tagesordnung", label="Tagesordnung", type="textarea"),
                    ],
                ),
            ],
        ),
        StageTemplate(
            id="enwg_s2",
            title="Planfeststellungsunterlagen",
            law_reference="\u00a7 43 EnWG",
            description="Erstellung der vollst\u00e4ndigen Planfeststellungsunterlagen.",
            info_text="\u00a7 43 EnWG: Einreichung der Planfeststellungsunterlagen.",
            tasks=[
                TaskTemplate(
                    id="enwg_s2_t1",
                    title="Bauwerksverzeichnis erstellen",
                    description="Erstellen Sie das Bauwerksverzeichnis.",
                    form_fields=[
                        FormField(name="anzahl_masten", label="Anzahl Masten", type="text"),
                        FormField(name="masttypen", label="Masttypen", type="textarea"),
                    ],
                ),
            ],
        ),
        StageTemplate(
            id="enwg_s3",
            title="Anh\u00f6rungsverfahren",
            law_reference="\u00a7 43a EnWG",
            description="Durchf\u00fchrung des Anh\u00f6rungsverfahrens.",
            info_text="\u00a7 43a EnWG i.V.m. \u00a7 73 VwVfG: \u00d6ffentliche Auslegung und Er\u00f6rterung.",
            tasks=[
                TaskTemplate(
                    id="enwg_s3_t1",
                    title="Einwendungen bearbeiten",
                    description="Sichten und beantworten Sie die Einwendungen.",
                    form_fields=[
                        FormField(name="anzahl_einwendungen", label="Anzahl Einwendungen", type="text"),
                        FormField(name="kategorien", label="Kategorien", type="textarea"),
                        FormField(name="erwiderung", label="Erwiderung", type="textarea"),
                    ],
                ),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# EnWG process template – English
# ---------------------------------------------------------------------------

ENWG_TEMPLATE_EN = ProcessTemplate(
    pfad=VerfahrensPfad.ENWG,
    label="EnWG \u2013 Plan Approval (110 kV)",
    description="Plan approval procedure under the Energy Industry Act for 110 kV lines.",
    stages=[
        StageTemplate(
            id="enwg_s1",
            title="Scoping Meeting",
            law_reference="\u00a7 43 EnWG / \u00a7 15 UVPG",
            description="Coordination with the district government on the scope of investigation.",
            info_text="\u00a7 43 EnWG in conjunction with \u00a7 15 UVPG: Scoping meeting with the hearing authority.",
            tasks=[
                TaskTemplate(
                    id="enwg_s1_t1",
                    title="Prepare Scoping Documents",
                    description="Prepare the documents for the scoping meeting.",
                    form_fields=[
                        FormField(name="behoerde", label="Responsible District Government", type="text"),
                        FormField(name="termin", label="Scheduled Date", type="date"),
                        FormField(name="tagesordnung", label="Agenda", type="textarea"),
                    ],
                ),
            ],
        ),
        StageTemplate(
            id="enwg_s2",
            title="Plan Approval Documents",
            law_reference="\u00a7 43 EnWG",
            description="Preparation of the complete plan approval documents.",
            info_text="\u00a7 43 EnWG: Submission of plan approval documents.",
            tasks=[
                TaskTemplate(
                    id="enwg_s2_t1",
                    title="Create Structure Register",
                    description="Create the structure register.",
                    form_fields=[
                        FormField(name="anzahl_masten", label="Number of Masts", type="text"),
                        FormField(name="masttypen", label="Mast Types", type="textarea"),
                    ],
                ),
            ],
        ),
        StageTemplate(
            id="enwg_s3",
            title="Hearing Procedure",
            law_reference="\u00a7 43a EnWG",
            description="Conducting the hearing procedure.",
            info_text="\u00a7 43a EnWG in conjunction with \u00a7 73 VwVfG: Public display and discussion.",
            tasks=[
                TaskTemplate(
                    id="enwg_s3_t1",
                    title="Process Objections",
                    description="Review and respond to objections.",
                    form_fields=[
                        FormField(name="anzahl_einwendungen", label="Number of Objections", type="text"),
                        FormField(name="kategorien", label="Categories", type="textarea"),
                        FormField(name="erwiderung", label="Response", type="textarea"),
                    ],
                ),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# Template registry keyed by (VerfahrensPfad, lang)
# ---------------------------------------------------------------------------

TEMPLATES: dict[tuple[VerfahrensPfad, str], ProcessTemplate] = {
    (VerfahrensPfad.NABEG, "de"): NABEG_TEMPLATE_DE,
    (VerfahrensPfad.NABEG, "en"): NABEG_TEMPLATE_EN,
    (VerfahrensPfad.ENWG, "de"): ENWG_TEMPLATE_DE,
    (VerfahrensPfad.ENWG, "en"): ENWG_TEMPLATE_EN,
}


# ---------------------------------------------------------------------------
# Workflow engine functions
# ---------------------------------------------------------------------------

def get_template(pfad: VerfahrensPfad, lang: str = "de") -> ProcessTemplate:
    return TEMPLATES[(pfad, lang)]


def determine_pfad(kv_level: int) -> VerfahrensPfad:
    if kv_level >= 220:
        return VerfahrensPfad.NABEG
    return VerfahrensPfad.ENWG


def create_project_stages(template: ProcessTemplate) -> list[StageInstance]:
    stages: list[StageInstance] = []
    for i, stage_tpl in enumerate(template.stages):
        tasks = [TaskInstance(template_id=t.id) for t in stage_tpl.tasks]
        stages.append(
            StageInstance(
                template_id=stage_tpl.id,
                status=StageStatus.ACTIVE if i == 0 else StageStatus.PENDING,
                tasks=tasks,
            )
        )
    return stages


def evaluate_stage(project: Project, _template: ProcessTemplate) -> Project:
    """Update stage statuses based on task completion. No locking."""
    for i, stage in enumerate(project.stages):
        all_done = all(t.status == TaskStatus.DONE for t in stage.tasks)
        any_started = any(t.status != TaskStatus.PENDING for t in stage.tasks)

        if all_done and len(stage.tasks) > 0:
            stage.status = StageStatus.COMPLETED
        elif any_started:
            stage.status = StageStatus.ACTIVE
        # PENDING stages stay PENDING but are still accessible

    # Update current_stage_index to the first non-completed stage
    for i, stage in enumerate(project.stages):
        if stage.status != StageStatus.COMPLETED:
            project.current_stage_index = i
            break
    else:
        project.current_stage_index = len(project.stages) - 1

    return project


def find_task_in_project(project: Project, task_id: str) -> tuple[int, int] | None:
    for si, stage in enumerate(project.stages):
        for ti, task in enumerate(stage.tasks):
            if task.id == task_id:
                return si, ti
    return None


def get_task_template_id(project: Project, task_instance_id: str) -> str | None:
    for stage in project.stages:
        for task in stage.tasks:
            if task.id == task_instance_id:
                return task.template_id
    return None


# ---------------------------------------------------------------------------
# Demo project display translation (DE -> EN)
# ---------------------------------------------------------------------------

_DEMO_TRANSLATIONS: dict[str, str] = {
    # Blockers
    "Artenschutzkartierung unvollständig": "Species protection survey incomplete",
    "Umweltplanung": "Environmental Planning",
    # Historical case titles
    "380-kV Leitung Waldquerung Süd": "380 kV Line Forest Crossing South",
    "Erdkabelabschnitt nahe Siedlung": "Underground Cable Section Near Settlement",
    # Key reasons
    "Frühzeitige Abstimmung mit Forstbehörde": "Early coordination with forestry authority",
    "Alternative Maststandorte belegt": "Alternative mast locations documented",
    "Hydrogeologisches Gutachten nachgefordert": "Hydrogeological report requested additionally",
    "Unvollständige Trassenalternativen": "Incomplete route alternatives",
    # Document types
    "Projektsteckbrief": "Project Profile",
    "Korridoralternativenbericht": "Corridor Alternatives Report",
    "Artenschutzbeitrag": "Species Protection Report",
    # Project tasks
    "Kartierung Brutzeitfenster abschließen": "Complete breeding season survey",
    "Flurstücksliste mit Korridor V2 synchronisieren": "Synchronize parcel list with Corridor V2",
    "Vollständige Artenliste + Kartenanhänge": "Complete species list + map appendices",
    "Keine Geometrie-Konflikte > 5m": "No geometry conflicts > 5m",
    # Risk mitigation
    "Zusatzkartierung + Trassenmikroshift": "Additional survey + route microshift",
    "Frühzeitige Eigentümerdialoge + Alternativzufahrten": "Early landowner dialogues + alternative access roads",
    # Risk owner
    "Wegerechtsteam": "Land Rights Team",
}


def _t(text: str) -> str:
    """Translate a known demo string, or return it unchanged."""
    return _DEMO_TRANSLATIONS.get(text, text)


def translate_project_display(project: Project, lang: str) -> Project:
    """Return a copy of the project with display-facing demo fields translated.

    If lang is "de", the project is returned unchanged (no copy).
    For "en", a deep copy is made and known demo strings are translated.
    """
    if lang == "de":
        return project

    p = project.model_copy(deep=True)

    # Blockers
    for blocker in p.blockers:
        blocker.title = _t(blocker.title)
        blocker.owner_role = _t(blocker.owner_role)

    # Historical cases
    for case in p.historical_cases:
        case.title = _t(case.title)
        case.key_reasons = [_t(r) for r in case.key_reasons]

    # Documents
    for doc in p.documents:
        doc.doc_type = _t(doc.doc_type)

    # Project tasks
    for task in p.project_tasks:
        task.title = _t(task.title)
        task.owner_role = _t(task.owner_role)
        task.done_definition = _t(task.done_definition)

    # Risks
    for risk in p.risks:
        risk.mitigation = _t(risk.mitigation)
        risk.owner = _t(risk.owner)

    return p
