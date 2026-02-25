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
    translate_project_display,
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
def get_workflow(project_id: str, lang: str = "de"):
    project = mock_db.projects.get(project_id)
    if not project:
        msg = "Project not found" if lang == "en" else "Projekt nicht gefunden"
        raise HTTPException(404, msg)
    template = get_template(project.pfad, lang=lang)
    display_project = translate_project_display(project, lang) if lang != "de" else project
    return WorkflowResponse(project=display_project, template=template)


@router.get("/projects", response_model=list[Project])
def list_projects():
    return list(mock_db.projects.values())


# ---------------------------------------------------------------------------
# Task endpoints
# ---------------------------------------------------------------------------

@router.post("/task/{task_id}/complete")
def complete_task(task_id: str, req: TaskCompleteRequest, project_id: str, lang: str = "de"):
    project = mock_db.projects.get(project_id)
    if not project:
        msg = "Project not found" if lang == "en" else "Projekt nicht gefunden"
        raise HTTPException(404, msg)
    location = find_task_in_project(project, task_id)
    if location is None:
        msg = "Task not found" if lang == "en" else "Task nicht gefunden"
        raise HTTPException(404, msg)
    section_id, si, ti = location
    if section_id:
        section = next(s for s in project.sections if s.id == section_id)
        task = section.stages[si].tasks[ti]
    else:
        task = project.stages[si].tasks[ti]
    task.status = TaskStatus.DONE
    task.form_data = req.form_data
    task.completed_checklist = req.completed_checklist
    task.updated_at = datetime.now()
    template = get_template(project.pfad)
    evaluate_stage(project, template)
    return {"status": "ok", "project": project}


@router.post("/task/{task_id}/save")
def save_task(task_id: str, req: TaskCompleteRequest, project_id: str, lang: str = "de"):
    project = mock_db.projects.get(project_id)
    if not project:
        msg = "Project not found" if lang == "en" else "Projekt nicht gefunden"
        raise HTTPException(404, msg)
    location = find_task_in_project(project, task_id)
    if location is None:
        msg = "Task not found" if lang == "en" else "Task nicht gefunden"
        raise HTTPException(404, msg)
    section_id, si, ti = location
    if section_id:
        section = next(s for s in project.sections if s.id == section_id)
        task = section.stages[si].tasks[ti]
    else:
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
def reopen_task(task_id: str, project_id: str, lang: str = "de"):
    project = mock_db.projects.get(project_id)
    if not project:
        msg = "Project not found" if lang == "en" else "Projekt nicht gefunden"
        raise HTTPException(404, msg)
    location = find_task_in_project(project, task_id)
    if location is None:
        msg = "Task not found" if lang == "en" else "Task nicht gefunden"
        raise HTTPException(404, msg)
    section_id, si, ti = location
    if section_id:
        section = next(s for s in project.sections if s.id == section_id)
        task = section.stages[si].tasks[ti]
    else:
        task = project.stages[si].tasks[ti]
    task.status = TaskStatus.IN_PROGRESS
    task.updated_at = datetime.now()
    template = get_template(project.pfad)
    evaluate_stage(project, template)
    return {"status": "ok"}


@router.post("/email/{email_id}/action")
def email_action(email_id: str, action_type: str = "assign_task"):
    return {"status": "ok", "email_id": email_id, "action": action_type}


# ---------------------------------------------------------------------------
# AI field generation (mock – per field)
# ---------------------------------------------------------------------------

@router.post("/ai/generate-field", response_model=AIFieldResponse)
def generate_field(req: AIFieldRequest):
    project = mock_db.projects.get(req.project_id)
    if not project:
        msg = "Project not found" if req.lang == "en" else "Projekt nicht gefunden"
        raise HTTPException(404, msg)

    template_id = get_task_template_id(project, req.task_instance_id)
    if not template_id:
        msg = "Task not found" if req.lang == "en" else "Task nicht gefunden"
        raise HTTPException(404, msg)

    text = _generate_for_field(project, template_id, req.field_name, req.field_label, lang=req.lang)
    return AIFieldResponse(text=text)


def _generate_for_field(
    project: Project, task_tpl_id: str, field_name: str, field_label: str, lang: str = "de"
) -> str:
    """Generate realistic regulatory text for any form field."""
    p = project

    # Gather previous form data for context
    prev_data: dict[str, str] = {}
    for section in p.sections:
        for stage in section.stages:
            for task in stage.tasks:
                prev_data.update(task.form_data)
    for stage in p.stages:
        for task in stage.tasks:
            prev_data.update(task.form_data)

    # ── German specific generators keyed by (task_template_id, field_name) ──
    specific_de: dict[tuple[str, str], str] = {
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

    # ── English specific generators keyed by (task_template_id, field_name) ──
    specific_en: dict[tuple[str, str], str] = {
        # Stage 1 - Rechtsrahmen
        ("s1_t1", "rechtsrahmen"): (
            f'The project "{p.name}" is listed as a cross-state extra-high voltage line '
            f"({p.kv_level} kV {p.technology}) in the Federal Requirements Plan (BBPlG). "
            f"Pursuant to \u00a7 2(1) NABEG, NABEG applies as the project crosses the federal states "
            f"{' and '.join(p.states_crossed)} and has a voltage level \u2265 220 kV. "
            f"Federal sectoral planning pursuant to \u00a7\u00a7 4\u201317 NABEG is required."
        ),
        ("s1_t1", "zustaendige_behoerde"): "Federal Network Agency (BNetzA), Grid Expansion Division",
        ("s1_t1", "begruendung"): (
            f"The assignment to NABEG results from the designation in the BBPlG as cross-state "
            f"(\u00a7 2(1) BBPlG). The BNetzA is the responsible authority pursuant to \u00a7 31 NABEG. "
            f"The project crosses the federal states "
            f"{' and '.join(p.states_crossed)} over a length of {p.length_km} km."
        ),
        # Stage 1 - Projektsteckbrief
        ("s1_t2", "vorhaben_titel"): p.name,
        ("s1_t2", "technologie"): f"HVDC ({p.technology}), {p.kv_level} kV, mixed construction (overhead line/underground cable)",
        ("s1_t2", "trassenlaenge"): f"{p.length_km} km",
        ("s1_t2", "bundeslaender"): ", ".join(p.states_crossed),
        ("s1_t2", "zusammenfassung"): (
            f"Construction of a {p.kv_level} kV HVDC connection ({p.technology}) as part of "
            f"the North-South Link for transmitting wind energy from northern Germany to "
            f"consumption centers in southern Germany. The route runs in mixed construction "
            f"over {p.length_km} km through {' and '.join(p.states_crossed)}. The project "
            f"serves the implementation of the energy transition and is designated as a "
            f"priority need in the Federal Requirements Plan."
        ),
        # Stage 1 - Stakeholder
        ("s1_t3", "behoerden"): (
            "• Federal Network Agency (BNetzA) \u2013 Permitting authority\n"
            "• Government of Upper Franconia \u2013 Spatial planning BY\n"
            "• District Government Kassel \u2013 Spatial planning HE\n"
            "• Bavarian State Office for the Environment (LfU)\n"
            "• HLNUG Hesse"
        ),
        ("s1_t3", "eigentuemer"): (
            "• Owner Group A \u2013 Parcel BY-091-223-17 (private, not contacted)\n"
            "• Municipality Demohausen \u2013 Parcel HE-044-887-03 (municipal, negotiation initiated)"
        ),
        ("s1_t3", "verbaende"): (
            "• BUND State Association Bavaria\n• NABU Hesse\n"
            "• LBV Bavaria\n• Citizens' Initiative Route Alternative e.V."
        ),
        # Stage 2 - Korridore
        ("s2_t1", "korridor_a"): (
            "Western Corridor: Routing along BAB A7, length 76.3 km, predominantly overhead "
            "line. Crossing of 2 FFH areas, forest share 18%. Minimum settlement distance 450 m."
        ),
        ("s2_t1", "korridor_b"): (
            "Eastern Corridor: Routing parallel to DB railway line, 72.8 km, underground cable "
            "share 35%. Crossing of 1 FFH area, forest share 12%. Good bundling potential with "
            "railway infrastructure."
        ),
        ("s2_t1", "vorzugskorridor"): "Corridor B (eastern)",
        ("s2_t1", "begruendung_auswahl"): (
            "Corridor B is recommended: (1) lower FFH impact, (2) shorter route, "
            "(3) better infrastructure bundling, (4) lower overall spatial resistance "
            "(Class II vs. III)."
        ),
        # Stage 2 - GIS
        ("s2_t2", "schutzgebiete"): (
            "• FFH area 'Forest area east of Demo': 2.3 km crossing\n"
            "• Water protection zone III: 1.1 km edge contact"
        ),
        ("s2_t2", "waldanteil"): (
            "Forest crossing approx. 8.7 km (12% of total route). Predominantly commercial "
            "forest (spruce), 2.1 km mixed deciduous forest with biotope function."
        ),
        ("s2_t2", "siedlungsabstand"): (
            "• Musterstadt: 320 m (overhead line)\n"
            "• Demohausen: 220 m (underground cable planned)\n"
            "• Beispielhof: 580 m (overhead line)"
        ),
        ("s2_t2", "konflikte"): (
            "2 geometry conflicts >5m:\n"
            "• BY-091-223-17: Overlap with mast location M-34\n"
            "• HE-044-887-03: Underground cable route tangent to municipal road"
        ),
        # Stage 2 - Bericht
        ("s2_t3", "methodik"): (
            "Spatial resistance analysis per BNetzA guideline (2023), 3-stage assessment: "
            "(1) Spatial resistance mapping 1:25,000, (2) Multi-criteria assessment with "
            "14 criteria, (3) Overall evaluation incl. technical feasibility."
        ),
        ("s2_t3", "bewertungsergebnis"): (
            "Corridor B: Spatial resistance class II (medium) \u2013 67/100 pts.\n"
            "Corridor A: Spatial resistance class III (high) \u2013 48/100 pts."
        ),
        ("s2_t3", "empfehlung"): (
            "Recommendation: Continue with Corridor B (eastern) as preferred corridor "
            "in federal sectoral planning."
        ),
        # Stage 3 - Artenschutz
        ("s3_t1", "betroffene_arten"): (
            "• Red kite (Milvus milvus) \u2013 3 breeding pairs within 1 km radius\n"
            "• Black stork (Ciconia nigra) \u2013 1 nest, 800 m distance\n"
            "• Bats (Myotis spp.) \u2013 Roost suspicion at km 34.5"
        ),
        ("s3_t1", "kartierungsstatus"): (
            "Breeding season survey for red kite and black stork ongoing. "
            "Bat detector surveys 60% completed. Deadline: 20.02.2026."
        ),
        ("s3_t1", "vermeidungsmassnahmen"): (
            "• Construction timing restriction: No construction March\u2013July within 500 m "
            "of red kite nests\n"
            "• Bird protection markers on earth wires in section km 12\u201318\n"
            "• Ecological construction supervision throughout\n"
            "• Night construction ban near bat roosts"
        ),
        ("s3_t1", "kompensation"): (
            "• Red kite replacement habitat: Creation of 3 ha extensive grassland as "
            "foraging habitat (ratio 1:1.5)\n"
            "• Bat boxes: Installation of 20 boxes in adjacent forest\n"
            "• CEF measure black stork: Buffer zone 500 m around nest"
        ),
        # Stage 3 - Scoping
        ("s3_t2", "schutzgueter"): (
            "• Humans (residential, recreation): Settlement distances, noise emissions\n"
            "• Wildlife/flora/biodiversity: FFH compatibility, species protection\n"
            "• Soil/land use: Sealing, soil compaction for underground cable\n"
            "• Water: WPA Zone III impact, groundwater protection\n"
            "• Climate/air: Cold air corridors, forest clearing\n"
            "• Landscape: Visibility of overhead line masts, landscape character\n"
            "• Cultural heritage: Ground monuments in route area"
        ),
        ("s3_t2", "untersuchungsraum"): (
            f"Study area: 1,000 m on both sides of the route axis (Corridor B). "
            f"Total area approx. 145 km\u00b2. Delimitation based on the range of relevant "
            f"impact factors (EMF, noise, visual impact). Extended study area (3 km) for "
            f"avifaunal surveys."
        ),
        ("s3_t2", "methodik_umwelt"): (
            "EIA methodology pursuant to \u00a7 16 UVPG:\n"
            "1. Baseline survey: Analysis of existing data + field mapping\n"
            "2. Impact assessment: Overlay of sensitivity \u00d7 impact intensity\n"
            "3. Evaluation: 5-level significance scale (not significant to very high)\n"
            "4. Mitigation concept: Avoidance, minimization, compensation\n"
            "5. Alternatives comparison: Comparison of environmental impacts"
        ),
        # Stage 3 - Forstanfrage
        ("s3_t3", "empfaenger"): (
            "Office for Food, Agriculture and Forestry (AELF)\n"
            "Forestry Department\nBeispielstra\u00dfe 12\n95000 Musterstadt"
        ),
        ("s3_t3", "betreff"): (
            f'Request for forest conversion pursuant to Art. 9 BayWaldG \u2013 '
            f'Project "{p.name}"'
        ),
        ("s3_t3", "anschreiben"): (
            f"Dear Sir or Madam,\n\n"
            f'In the context of the project "{p.name}" ({p.kv_level} kV {p.technology}, '
            f"federal sectoral planning under NABEG), the use of forest areas in the area "
            f"of Corridor B (eastern) is required.\n\n"
            f"Affected: approx. 8.7 km forest crossing (12% of total route of "
            f"{p.length_km} km), thereof:\n"
            f"\u2022 approx. 6.6 km commercial forest (spruce)\n"
            f"\u2022 approx. 2.1 km mixed deciduous forest with biotope function\n\n"
            f"We request early coordination regarding:\n"
            f"1. Scope of required forest conversion permit\n"
            f"2. Requirements for forest compensation\n"
            f"3. Possible conditions and stipulations\n\n"
            f"Detailed documents are enclosed.\n\n"
            f"Yours sincerely"
        ),
        ("s3_t3", "anlagen"): (
            "1. Overview map of route in forest area (1:10,000)\n"
            "2. Forest type inventory map (1:5,000)\n"
            "3. List of affected parcels\n"
            "4. Preliminary forest compensation concept\n"
            "5. Extract from corridor alternatives report (DOC-017, v0.9)"
        ),
    }

    # Select the correct language dictionary
    specific = specific_en if lang == "en" else specific_de

    key = (task_tpl_id, field_name)
    if key in specific:
        return specific[key]

    # ── Generic fallback based on field_name patterns ──
    return _generic_fallback(p, field_name, field_label, prev_data, lang=lang)


def _generic_fallback(
    p: Project, field_name: str, field_label: str, prev_data: dict, lang: str = "de"
) -> str:
    """Generate generic text for fields not in the specific map."""

    name_lower = field_name.lower()
    label_lower = field_label.lower()

    if lang == "en":
        return _generic_fallback_en(p, field_name, field_label, name_lower, label_lower)

    # ── German fallback (default) ──
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


def _generic_fallback_en(
    p: Project, field_name: str, field_label: str, name_lower: str, label_lower: str
) -> str:
    """Generate generic English text for fields not in the specific map."""

    if "empfaenger" in name_lower or "empfänger" in label_lower:
        return (
            "Federal Network Agency\nGrid Expansion Division\n"
            "Tulpenfeld 4\n53113 Bonn"
        )

    if "betreff" in name_lower:
        return f'Re: Project "{p.name}" \u2013 {p.kv_level} kV {p.technology} \u2013 {field_label}'

    if "anschreiben" in name_lower or "schreiben" in name_lower:
        return (
            f"Dear Sir or Madam,\n\n"
            f'In the context of the project "{p.name}" ({p.kv_level} kV {p.technology}), '
            f"we submit the following documents for review.\n\n"
            f"The project extends over {p.length_km} km through the federal states "
            f"{' and '.join(p.states_crossed)}.\n\n"
            f"We are available for any questions.\n\n"
            f"Yours sincerely"
        )

    if "begruendung" in name_lower or "begründung" in label_lower:
        return (
            f'The measure is required within the scope of the project "{p.name}" '
            f"({p.kv_level} kV {p.technology}). The necessity arises from the designation "
            f"in the Federal Requirements Plan as a priority need project to ensure "
            f"security of supply."
        )

    if "methodik" in name_lower:
        return (
            "The assessment follows recognized methods per the current BNetzA guideline. "
            "A multi-stage procedure is applied that considers quantitative and qualitative "
            "criteria."
        )

    if any(k in name_lower for k in ["zusammenfassung", "beschreibung", "ergebnis"]):
        return (
            f'The project "{p.name}" comprises the construction of a {p.kv_level} kV '
            f"HVDC line ({p.technology}) over {p.length_km} km through "
            f"{' and '.join(p.states_crossed)}. The mixed construction (overhead line/"
            f"underground cable) takes local conditions into account."
        )

    if "anlagen" in name_lower:
        return (
            "1. Overview map (1:25,000)\n"
            "2. Detailed maps of affected sections\n"
            "3. Technical explanations\n"
            "4. Relevant reports and evidence"
        )

    # Ultimate fallback
    return (
        f'[{field_label}] \u2013 Draft for the project "{p.name}" '
        f"({p.kv_level} kV {p.technology}, {p.length_km} km, "
        f"Federal states: {', '.join(p.states_crossed)}). "
        f"This text block was automatically generated and should be reviewed "
        f"and supplemented by experts."
    )
