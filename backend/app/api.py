from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, HTTPException

from . import mock_db
from .models import (
    AIFieldRequest,
    AIFieldResponse,
    Project,
    ProjectCreateRequest,
    TaskCompleteRequest,
    TaskStatus,
    WorkflowResponse,
)
from .workflow_engine import (
    create_project_stages,
    determine_pfad,
    evaluate_stage,
    find_task_in_project,
    get_task_template_id,
    get_template,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Project endpoints
# ---------------------------------------------------------------------------

@router.post("/project/create", response_model=WorkflowResponse)
def create_project(req: ProjectCreateRequest):
    pfad = determine_pfad(req.kv_level)
    template = get_template(pfad)
    project = Project(
        name=req.name,
        pfad=pfad,
        kv_level=req.kv_level,
        stages=create_project_stages(template),
    )
    mock_db.projects[project.id] = project
    return WorkflowResponse(project=project, template=template)


@router.get("/project/{project_id}/workflow", response_model=WorkflowResponse)
def get_workflow(project_id: str):
    project = mock_db.projects.get(project_id)
    if not project:
        raise HTTPException(404, "Projekt nicht gefunden")
    template = get_template(project.pfad)
    return WorkflowResponse(project=project, template=template)


@router.get("/projects", response_model=list[Project])
def list_projects():
    return list(mock_db.projects.values())


# ---------------------------------------------------------------------------
# Task endpoints
# ---------------------------------------------------------------------------

@router.post("/task/{task_id}/complete")
def complete_task(task_id: str, req: TaskCompleteRequest, project_id: str):
    project = mock_db.projects.get(project_id)
    if not project:
        raise HTTPException(404, "Projekt nicht gefunden")
    location = find_task_in_project(project, task_id)
    if location is None:
        raise HTTPException(404, "Task nicht gefunden")
    si, ti = location
    task = project.stages[si].tasks[ti]
    task.status = TaskStatus.DONE
    task.form_data = req.form_data
    task.completed_checklist = req.completed_checklist
    task.updated_at = datetime.now()
    template = get_template(project.pfad)
    evaluate_stage(project, template)
    return {"status": "ok", "project": project}


@router.post("/task/{task_id}/save")
def save_task(task_id: str, req: TaskCompleteRequest, project_id: str):
    project = mock_db.projects.get(project_id)
    if not project:
        raise HTTPException(404, "Projekt nicht gefunden")
    location = find_task_in_project(project, task_id)
    if location is None:
        raise HTTPException(404, "Task nicht gefunden")
    si, ti = location
    task = project.stages[si].tasks[ti]
    task.form_data = req.form_data
    task.completed_checklist = req.completed_checklist
    task.updated_at = datetime.now()
    if task.status == TaskStatus.PENDING:
        task.status = TaskStatus.IN_PROGRESS
    template = get_template(project.pfad)
    evaluate_stage(project, template)
    return {"status": "ok"}


@router.patch("/task/{task_id}/reopen")
def reopen_task(task_id: str, project_id: str):
    project = mock_db.projects.get(project_id)
    if not project:
        raise HTTPException(404, "Projekt nicht gefunden")
    location = find_task_in_project(project, task_id)
    if location is None:
        raise HTTPException(404, "Task nicht gefunden")
    si, ti = location
    task = project.stages[si].tasks[ti]
    task.status = TaskStatus.IN_PROGRESS
    task.updated_at = datetime.now()
    template = get_template(project.pfad)
    evaluate_stage(project, template)
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# AI field generation (mock – per field)
# ---------------------------------------------------------------------------

@router.post("/ai/generate-field", response_model=AIFieldResponse)
def generate_field(req: AIFieldRequest):
    project = mock_db.projects.get(req.project_id)
    if not project:
        raise HTTPException(404, "Projekt nicht gefunden")

    template_id = get_task_template_id(project, req.task_instance_id)
    if not template_id:
        raise HTTPException(404, "Task nicht gefunden")

    text = _generate_for_field(project, template_id, req.field_name, req.field_label)
    return AIFieldResponse(text=text)


def _generate_for_field(
    project: Project, task_tpl_id: str, field_name: str, field_label: str
) -> str:
    """Generate realistic German regulatory text for any form field."""
    p = project

    # Gather previous form data for context
    prev_data: dict[str, str] = {}
    for stage in p.stages:
        for task in stage.tasks:
            prev_data.update(task.form_data)

    # Specific generators keyed by (task_template_id, field_name)
    specific: dict[tuple[str, str], str] = {
        # Stage 1 - Rechtsrahmen
        ("s1_t1", "rechtsrahmen"): (
            f"Das Vorhaben \"{p.name}\" ist als länderübergreifende Höchstspannungsleitung "
            f"({p.kv_level} kV {p.technology}) im Bundesbedarfsplan (BBPlG) enthalten. "
            f"Gemäß § 2 Abs. 1 NABEG findet das NABEG Anwendung, da das Vorhaben die "
            f"Bundesländer {' und '.join(p.states_crossed)} quert und eine Spannungsebene "
            f"≥ 220 kV aufweist. Die Bundesfachplanung nach §§ 4–17 NABEG ist durchzuführen."
        ),
        ("s1_t1", "zustaendige_behoerde"): "Bundesnetzagentur (BNetzA), Referat für Netzausbau",
        ("s1_t1", "begruendung"): (
            f"Die Zuordnung zum NABEG ergibt sich aus der Kennzeichnung im BBPlG als "
            f"länderübergreifend (§ 2 Abs. 1 BBPlG). Die BNetzA ist gemäß § 31 NABEG "
            f"zuständige Behörde. Das Vorhaben quert die Bundesländer "
            f"{' und '.join(p.states_crossed)} auf einer Länge von {p.length_km} km."
        ),
        # Stage 1 - Projektsteckbrief
        ("s1_t2", "vorhaben_titel"): p.name,
        ("s1_t2", "technologie"): f"HGÜ ({p.technology}), {p.kv_level} kV, gemischte Bauweise (Freileitung/Erdkabel)",
        ("s1_t2", "trassenlaenge"): f"{p.length_km} km",
        ("s1_t2", "bundeslaender"): ", ".join(p.states_crossed),
        ("s1_t2", "zusammenfassung"): (
            f"Neubau einer {p.kv_level}-kV-HGÜ-Verbindung ({p.technology}) als Teil des "
            f"Nord-Süd-Links zur Übertragung von Windenergie aus Norddeutschland in die "
            f"Verbrauchszentren Süddeutschlands. Die Trasse verläuft in gemischter Bauweise "
            f"über {p.length_km} km durch {' und '.join(p.states_crossed)}. Das Vorhaben "
            f"dient der Umsetzung der Energiewende und ist im Bundesbedarfsplan als "
            f"vordringlicher Bedarf gekennzeichnet."
        ),
        # Stage 1 - Stakeholder
        ("s1_t3", "behoerden"): (
            "• Bundesnetzagentur (BNetzA) – Genehmigungsbehörde\n"
            "• Regierung von Oberfranken – Raumordnung BY\n"
            "• Regierungspräsidium Kassel – Raumordnung HE\n"
            "• Bayerisches Landesamt für Umwelt (LfU)\n"
            "• HLNUG Hessen"
        ),
        ("s1_t3", "eigentuemer"): (
            f"• Eigentümergruppe A – Flurstück BY-091-223-17 (privat, nicht kontaktiert)\n"
            f"• Gemeinde Demohausen – Flurstück HE-044-887-03 (kommunal, Verhandlung eingeleitet)"
        ),
        ("s1_t3", "verbaende"): (
            "• BUND Landesverband Bayern\n• NABU Hessen\n"
            "• LBV Bayern\n• Bürgerinitiative Trassenalternative e.V."
        ),
        # Stage 2 - Korridore
        ("s2_t1", "korridor_a"): (
            f"Westlicher Korridor: Verlauf entlang BAB A7, Länge 76,3 km, überwiegend "
            f"Freileitung. Querung von 2 FFH-Gebieten, Waldanteil 18%. "
            f"Minimaler Siedlungsabstand 450 m."
        ),
        ("s2_t1", "korridor_b"): (
            f"Östlicher Korridor: Trassenführung parallel zur DB-Strecke, 72,8 km, "
            f"Erdkabelanteil 35%. Querung von 1 FFH-Gebiet, Waldanteil 12%. "
            f"Gute Bündelungsmöglichkeit mit Bahninfrastruktur."
        ),
        ("s2_t1", "vorzugskorridor"): "Korridor B (östlich)",
        ("s2_t1", "begruendung_auswahl"): (
            "Korridor B wird empfohlen: (1) geringere FFH-Betroffenheit, "
            "(2) kürzere Strecke, (3) bessere Infrastrukturbündelung, "
            "(4) geringerer Gesamtraumwiderstand (Klasse II vs. III)."
        ),
        # Stage 2 - GIS
        ("s2_t2", "schutzgebiete"): (
            "• FFH-Gebiet 'Waldgebiet östlich Demo': 2,3 km Querung\n"
            "• Wasserschutzgebiet Zone III: 1,1 km Randberührung"
        ),
        ("s2_t2", "waldanteil"): (
            f"Waldquerung ca. 8,7 km (12% der Gesamtstrecke). "
            f"Überwiegend Wirtschaftswald (Fichte), 2,1 km Laubmischwald mit Biotopfunktion."
        ),
        ("s2_t2", "siedlungsabstand"): (
            "• Musterstadt: 320 m (Freileitung)\n"
            "• Demohausen: 220 m (Erdkabel geplant)\n"
            "• Beispielhof: 580 m (Freileitung)"
        ),
        ("s2_t2", "konflikte"): (
            "2 Geometrie-Konflikte >5m:\n"
            "• BY-091-223-17: Überlappung mit Maststandort M-34\n"
            "• HE-044-887-03: Erdkabeltrasse tangiert Gemeindestraße"
        ),
        # Stage 2 - Bericht
        ("s2_t3", "methodik"): (
            "Raumwiderstandsanalyse nach BNetzA-Leitfaden (2023), 3-stufiges "
            "Bewertungsverfahren: (1) Raumwiderstandskartierung 1:25.000, "
            "(2) Multikriterielle Bewertung mit 14 Kriterien, "
            "(3) Gesamtabwägung inkl. technischer Realisierbarkeit."
        ),
        ("s2_t3", "bewertungsergebnis"): (
            "Korridor B: Raumwiderstandsklasse II (mittel) – 67/100 Pkt.\n"
            "Korridor A: Raumwiderstandsklasse III (hoch) – 48/100 Pkt."
        ),
        ("s2_t3", "empfehlung"): (
            "Empfehlung: Weiterverfolgung Korridor B (östlich) als Vorzugskorridor "
            "in der Bundesfachplanung."
        ),
        # Stage 3 - Artenschutz
        ("s3_t1", "betroffene_arten"): (
            "• Rotmilan (Milvus milvus) – 3 Brutpaare im 1-km-Radius\n"
            "• Schwarzstorch (Ciconia nigra) – 1 Horst, 800 m Abstand\n"
            "• Fledermäuse (Myotis spp.) – Quartiersverdacht bei km 34,5"
        ),
        ("s3_t1", "kartierungsstatus"): (
            "Brutzeitfenster-Kartierung für Rotmilan und Schwarzstorch läuft. "
            "Fledermaus-Detektorbegehungen zu 60% abgeschlossen. "
            "Frist: 20.02.2026."
        ),
        ("s3_t1", "vermeidungsmassnahmen"): (
            "• Bauzeitenregelung: Keine Bauarbeiten März–Juli im Umkreis "
            "von 500 m um Rotmilan-Horste\n"
            "• Vogelschutzmarker an Erdseilen im Bereich km 12–18\n"
            "• Ökologische Baubegleitung während der gesamten Bauphase\n"
            "• Nächtliches Bauverbot im Bereich der Fledermausquartiere"
        ),
        ("s3_t1", "kompensation"): (
            "• Ersatzhabitat Rotmilan: Anlage von 3 ha extensivem Grünland "
            "als Nahrungshabitat (Verhältnis 1:1,5)\n"
            "• Fledermauskästen: Installation von 20 Kästen in angrenzenden "
            "Waldbeständen\n"
            "• CEF-Maßnahme Schwarzstorch: Beruhigungszone 500 m um Horst"
        ),
        # Stage 3 - Scoping
        ("s3_t2", "schutzgueter"): (
            "• Mensch (Wohnen, Erholung): Siedlungsabstände, Lärmimmissionen\n"
            "• Tiere/Pflanzen/Biodiversität: FFH-Verträglichkeit, Artenschutz\n"
            "• Boden/Fläche: Versiegelung, Bodenverdichtung bei Erdkabel\n"
            "• Wasser: WSG Zone III Betroffenheit, Grundwasserschutz\n"
            "• Klima/Luft: Kaltluftschneisen, Waldrodung\n"
            "• Landschaft: Sichtbarkeit Freileitungsmasten, Landschaftsbild\n"
            "• Kulturelles Erbe: Bodendenkmäler im Trassenbereich"
        ),
        ("s3_t2", "untersuchungsraum"): (
            f"Untersuchungsraum: 1.000 m beiderseits der Trassenachse (Korridor B). "
            f"Gesamtfläche ca. 145 km². Abgrenzung basierend auf der Reichweite "
            f"relevanter Wirkfaktoren (EMF, Schall, visuelle Wirkung). "
            f"Erweiterter Untersuchungsraum (3 km) für avifaunistische Kartierung."
        ),
        ("s3_t2", "methodik_umwelt"): (
            "UVP-Methodik gemäß § 16 UVPG:\n"
            "1. Bestandsaufnahme: Auswertung vorhandener Daten + Geländekartierung\n"
            "2. Wirkungsprognose: Überlagerung Empfindlichkeit × Wirkintensität\n"
            "3. Bewertung: 5-stufige Erheblichkeitsskala (nicht erheblich bis sehr hoch)\n"
            "4. Maßnahmenkonzept: Vermeidung, Minimierung, Kompensation\n"
            "5. Variantenvergleich: Gegenüberstellung der Umweltauswirkungen"
        ),
        # Stage 3 - Forstanfrage
        ("s3_t3", "empfaenger"): (
            "Amt für Ernährung, Landwirtschaft und Forsten (AELF)\n"
            "Abteilung Forsten\nBeispielstraße 12\n95000 Musterstadt"
        ),
        ("s3_t3", "betreff"): (
            f"Anfrage zur Waldumwandlung gemäß Art. 9 BayWaldG – "
            f"Vorhaben \"{p.name}\""
        ),
        ("s3_t3", "anschreiben"): (
            f"Sehr geehrte Damen und Herren,\n\n"
            f"im Rahmen des Vorhabens \"{p.name}\" ({p.kv_level} kV {p.technology}, "
            f"Bundesfachplanung nach NABEG) ist die Inanspruchnahme von Waldflächen "
            f"im Bereich des Korridors B (östlich) erforderlich.\n\n"
            f"Betroffen sind ca. 8,7 km Waldquerung (12% der Gesamtstrecke von "
            f"{p.length_km} km), davon:\n"
            f"• ca. 6,6 km Wirtschaftswald (Fichte)\n"
            f"• ca. 2,1 km Laubmischwald mit Biotopfunktion\n\n"
            f"Wir bitten um eine frühzeitige Abstimmung hinsichtlich:\n"
            f"1. Umfang der erforderlichen Waldumwandlungsgenehmigung\n"
            f"2. Anforderungen an den Waldausgleich\n"
            f"3. Mögliche Auflagen und Bedingungen\n\n"
            f"Die detaillierten Unterlagen sind als Anlagen beigefügt.\n\n"
            f"Mit freundlichen Grüßen"
        ),
        ("s3_t3", "anlagen"): (
            "1. Übersichtskarte Trassenführung im Waldbereich (1:10.000)\n"
            "2. Bestandskarte Waldtypen (1:5.000)\n"
            "3. Flächenaufstellung der betroffenen Flurstücke\n"
            "4. Vorläufiges Konzept zum Waldausgleich\n"
            "5. Auszug aus dem Korridoralternativenbericht (DOC-017, v0.9)"
        ),
    }

    key = (task_tpl_id, field_name)
    if key in specific:
        return specific[key]

    # ── Generic fallback based on field_name patterns ──
    return _generic_fallback(p, field_name, field_label, prev_data)


def _generic_fallback(
    p: Project, field_name: str, field_label: str, prev_data: dict
) -> str:
    """Generate generic text for fields not in the specific map."""

    name_lower = field_name.lower()
    label_lower = field_label.lower()

    if "empfaenger" in name_lower or "empfänger" in label_lower:
        return (
            "Bundesnetzagentur\nReferat für Netzausbau\n"
            "Tulpenfeld 4\n53113 Bonn"
        )

    if "betreff" in name_lower:
        return f"Betr.: Vorhaben \"{p.name}\" – {p.kv_level} kV {p.technology} – {field_label}"

    if "anschreiben" in name_lower or "schreiben" in name_lower:
        return (
            f"Sehr geehrte Damen und Herren,\n\n"
            f"im Rahmen des Vorhabens \"{p.name}\" ({p.kv_level} kV {p.technology}) "
            f"übersenden wir Ihnen die nachfolgenden Unterlagen zur Prüfung.\n\n"
            f"Das Vorhaben erstreckt sich über {p.length_km} km durch die Bundesländer "
            f"{' und '.join(p.states_crossed)}.\n\n"
            f"Für Rückfragen stehen wir Ihnen jederzeit zur Verfügung.\n\n"
            f"Mit freundlichen Grüßen"
        )

    if "begruendung" in name_lower or "begründung" in label_lower:
        return (
            f"Die Maßnahme ist erforderlich im Rahmen des Vorhabens \"{p.name}\" "
            f"({p.kv_level} kV {p.technology}). Die Notwendigkeit ergibt sich aus "
            f"der Einstufung im Bundesbedarfsplan als Vorhaben mit vordringlichem Bedarf "
            f"zur Sicherstellung der Versorgungssicherheit."
        )

    if "methodik" in name_lower:
        return (
            "Die Bewertung erfolgt nach anerkannten Methoden gemäß dem aktuellen "
            "BNetzA-Leitfaden. Es wird ein mehrstufiges Verfahren angewandt, das "
            "quantitative und qualitative Kriterien berücksichtigt."
        )

    if any(k in name_lower for k in ["zusammenfassung", "beschreibung", "ergebnis"]):
        return (
            f"Das Vorhaben \"{p.name}\" umfasst den Neubau einer {p.kv_level}-kV-"
            f"HGÜ-Leitung ({p.technology}) über {p.length_km} km durch "
            f"{' und '.join(p.states_crossed)}. "
            f"Die gemischte Bauweise (Freileitung/Erdkabel) trägt den örtlichen "
            f"Gegebenheiten Rechnung."
        )

    if "anlagen" in name_lower:
        return (
            "1. Übersichtskarte (1:25.000)\n"
            "2. Detailkarten der betroffenen Abschnitte\n"
            "3. Technische Erläuterungen\n"
            "4. Relevante Gutachten und Nachweise"
        )

    # Ultimate fallback
    return (
        f"[{field_label}] – Entwurf für das Vorhaben \"{p.name}\" "
        f"({p.kv_level} kV {p.technology}, {p.length_km} km, "
        f"Bundesländer: {', '.join(p.states_crossed)}). "
        f"Dieser Textbaustein wurde automatisch generiert und sollte "
        f"fachlich geprüft und ergänzt werden."
    )
