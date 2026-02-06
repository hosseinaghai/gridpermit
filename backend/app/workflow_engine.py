from __future__ import annotations

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
# NABEG process template (3 stages)
# ---------------------------------------------------------------------------

NABEG_TEMPLATE = ProcessTemplate(
    pfad=VerfahrensPfad.NABEG,
    label="NABEG – Bundesfachplanung (Höchstspannung)",
    description="Verfahren nach dem Netzausbaubeschleunigungsgesetz für Höchstspannungsleitungen (ab 220 kV).",
    stages=[
        # ── Stage 1: Scope & Rechtsrahmen ──
        StageTemplate(
            id="s1_scope_recht",
            title="Scope & Rechtsrahmen",
            law_reference="§ 4ff. NABEG / BBPlG",
            description="Identifikation des anwendbaren Rechtsrahmens, Erstellung des Projektsteckbriefs und initiale Stakeholder-Erfassung.",
            info_text=(
                "§ 4 NABEG i.V.m. BBPlG: Die im Bundesbedarfsplangesetz als länderübergreifend "
                "oder grenzüberschreitend gekennzeichneten Vorhaben unterliegen dem NABEG. "
                "Der Vorhabenträger identifiziert den anwendbaren Rechtsrahmen und bereitet "
                "die erforderlichen Antragsunterlagen vor."
            ),
            tasks=[
                TaskTemplate(
                    id="s1_t1",
                    title="Anwendbares Recht identifizieren",
                    description="Prüfen Sie den anwendbaren Rechtsrahmen (NABEG vs. EnWG) und identifizieren Sie die zuständige Behörde.",
                    form_fields=[
                        FormField(name="rechtsrahmen", label="Anwendbarer Rechtsrahmen", type="textarea"),
                        FormField(name="zustaendige_behoerde", label="Zuständige Behörde", type="text"),
                        FormField(name="begruendung", label="Begründung der Zuordnung", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t2",
                    title="Projektsteckbrief erstellen",
                    description="Erstellen Sie den Projektsteckbrief mit allen technischen und räumlichen Eckdaten.",
                    form_fields=[
                        FormField(name="vorhaben_titel", label="Vorhabenbezeichnung", type="text"),
                        FormField(name="technologie", label="Technologie & Spannungsebene", type="text"),
                        FormField(name="trassenlaenge", label="Trassenlänge", type="text"),
                        FormField(name="bundeslaender", label="Betroffene Bundesländer", type="text"),
                        FormField(name="zusammenfassung", label="Projektzusammenfassung", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s1_t3",
                    title="Stakeholder-Ersterfassung durchführen",
                    description="Identifizieren Sie alle relevanten Stakeholder: Behörden, Grundeigentümer, Verbände.",
                    form_fields=[
                        FormField(name="behoerden", label="Beteiligte Behörden", type="textarea"),
                        FormField(name="eigentuemer", label="Betroffene Grundeigentümer", type="textarea"),
                        FormField(name="verbaende", label="Relevante Verbände & TöB", type="textarea"),
                    ],
                ),
            ],
        ),
        # ── Stage 2: Korridorfindung ──
        StageTemplate(
            id="s2_korridor",
            title="Korridorfindung",
            law_reference="§ 6 NABEG",
            description="Definition und Bewertung von Trassenkorridoralternativen, GIS-Analyse und Erstellung des Korridoralternativenberichts.",
            info_text=(
                "§ 6 NABEG: Der Vorhabenträger beantragt die Bundesfachplanung bei der "
                "Bundesnetzagentur. Hierzu gehört die Darstellung der in Betracht kommenden "
                "Trassenkorridore mit einer Bewertung der Raumverträglichkeit. Die BNetzA "
                "führt anschließend eine Antragskonferenz durch."
            ),
            tasks=[
                TaskTemplate(
                    id="s2_t1",
                    title="Korridoralternativen definieren",
                    description="Definieren Sie mindestens zwei Trassenkorridore mit technischer Bewertung.",
                    form_fields=[
                        FormField(name="korridor_a", label="Korridor A – Beschreibung", type="textarea"),
                        FormField(name="korridor_b", label="Korridor B – Beschreibung", type="textarea"),
                        FormField(name="vorzugskorridor", label="Vorzugskorridor", type="text"),
                        FormField(name="begruendung_auswahl", label="Begründung der Vorzugswahl", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s2_t2",
                    title="GIS-Verschneidung durchführen",
                    description="Führen Sie eine GIS-gestützte Raumanalyse mit Schutzgebiets- und Infrastruktur-Layern durch.",
                    form_fields=[
                        FormField(name="schutzgebiete", label="Betroffene Schutzgebiete", type="textarea"),
                        FormField(name="waldanteil", label="Waldquerungen", type="textarea"),
                        FormField(name="siedlungsabstand", label="Siedlungsabstände", type="textarea"),
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
        # ── Stage 3: Untersuchungsrahmen ──
        StageTemplate(
            id="s3_untersuchungsrahmen",
            title="Untersuchungsrahmen",
            law_reference="§ 7 NABEG",
            description="Erstellung des Artenschutzbeitrags, der umweltfachlichen Scoping-Unterlage und behördlicher Anfragen.",
            info_text=(
                "§ 7 NABEG: Die BNetzA legt nach Durchführung der Antragskonferenz den "
                "Untersuchungsrahmen für die Bundesfachplanung fest. Der Vorhabenträger "
                "erstellt die festgelegten Unterlagen, darunter den Umweltbericht und "
                "artenschutzrechtliche Prüfungen."
            ),
            tasks=[
                TaskTemplate(
                    id="s3_t1",
                    title="Artenschutzbeitrag erstellen",
                    description="Erstellen Sie den Artenschutzbeitrag (ASP Stufe I/II) mit Kartierungsdaten und Maßnahmenkonzept.",
                    form_fields=[
                        FormField(name="betroffene_arten", label="Betroffene Arten", type="textarea"),
                        FormField(name="kartierungsstatus", label="Kartierungsstatus", type="textarea"),
                        FormField(name="vermeidungsmassnahmen", label="Vermeidungsmaßnahmen", type="textarea"),
                        FormField(name="kompensation", label="Kompensationsmaßnahmen", type="textarea"),
                    ],
                ),
                TaskTemplate(
                    id="s3_t2",
                    title="Umweltfachliche Scoping-Unterlage erstellen",
                    description="Erstellen Sie die Scoping-Unterlage für die Umweltverträglichkeitsprüfung.",
                    form_fields=[
                        FormField(name="schutzgueter", label="Betroffene Schutzgüter", type="textarea"),
                        FormField(name="untersuchungsraum", label="Untersuchungsraum & Abgrenzung", type="textarea"),
                        FormField(name="methodik_umwelt", label="UVP-Methodik", type="textarea"),
                    ],
                    checklist=[
                        "Schutzgut Mensch bewertet",
                        "Schutzgut Tiere/Pflanzen/Biodiversität bewertet",
                        "Schutzgut Boden/Fläche bewertet",
                        "Schutzgut Wasser bewertet",
                        "Schutzgut Klima/Luft bewertet",
                        "Schutzgut Landschaft bewertet",
                        "Schutzgut kulturelles Erbe bewertet",
                    ],
                ),
                TaskTemplate(
                    id="s3_t3",
                    title="Forstbehördliche Anfrage vorbereiten",
                    description="Erstellen Sie die formelle Anfrage an die zuständige Forstbehörde zur Waldumwandlung.",
                    form_fields=[
                        FormField(name="empfaenger", label="Empfänger (Forstbehörde)", type="text"),
                        FormField(name="betreff", label="Betreff", type="text"),
                        FormField(name="anschreiben", label="Anschreiben", type="textarea"),
                        FormField(name="anlagen", label="Anlagenverzeichnis", type="textarea"),
                    ],
                ),
            ],
        ),
    ],
)

# EnWG template (simplified for now)
ENWG_TEMPLATE = ProcessTemplate(
    pfad=VerfahrensPfad.ENWG,
    label="EnWG – Planfeststellung (110 kV)",
    description="Planfeststellungsverfahren nach dem Energiewirtschaftsgesetz für 110-kV-Leitungen.",
    stages=[
        StageTemplate(
            id="enwg_s1",
            title="Scoping-Termin",
            law_reference="§ 43 EnWG / § 15 UVPG",
            description="Abstimmung mit der Bezirksregierung über den Untersuchungsumfang.",
            info_text="§ 43 EnWG i.V.m. § 15 UVPG: Scoping-Termin mit der Anhörungsbehörde.",
            tasks=[
                TaskTemplate(
                    id="enwg_s1_t1",
                    title="Scoping-Unterlagen vorbereiten",
                    description="Erstellen Sie die Unterlagen für den Scoping-Termin.",
                    form_fields=[
                        FormField(name="behoerde", label="Zuständige Bezirksregierung", type="text"),
                        FormField(name="termin", label="Geplanter Termin", type="date"),
                        FormField(name="tagesordnung", label="Tagesordnung", type="textarea"),
                    ],
                ),
            ],
        ),
        StageTemplate(
            id="enwg_s2",
            title="Planfeststellungsunterlagen",
            law_reference="§ 43 EnWG",
            description="Erstellung der vollständigen Planfeststellungsunterlagen.",
            info_text="§ 43 EnWG: Einreichung der Planfeststellungsunterlagen.",
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
            title="Anhörungsverfahren",
            law_reference="§ 43a EnWG",
            description="Durchführung des Anhörungsverfahrens.",
            info_text="§ 43a EnWG i.V.m. § 73 VwVfG: Öffentliche Auslegung und Erörterung.",
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

TEMPLATES: dict[VerfahrensPfad, ProcessTemplate] = {
    VerfahrensPfad.NABEG: NABEG_TEMPLATE,
    VerfahrensPfad.ENWG: ENWG_TEMPLATE,
}


# ---------------------------------------------------------------------------
# Workflow engine functions
# ---------------------------------------------------------------------------

def get_template(pfad: VerfahrensPfad) -> ProcessTemplate:
    return TEMPLATES[pfad]


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
