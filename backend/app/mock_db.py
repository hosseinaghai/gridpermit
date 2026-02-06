"""In-memory database with rich demo data."""

from __future__ import annotations

from datetime import datetime

from .models import (
    Blocker,
    DraftTemplate,
    GeoLayer,
    HistoricalCase,
    LandParcel,
    Project,
    ProjectDocument,
    ProjectTask,
    RegulatoryRequirement,
    Risk,
    SimilarityFeatures,
    StageInstance,
    StageStatus,
    Stakeholder,
    TaskInstance,
    TaskStatus,
    VerfahrensPfad,
)

projects: dict[str, Project] = {}

DEMO_PROJECT_ID = "P-DE-TSO-001"


def seed_demo_data() -> None:
    demo = Project(
        id=DEMO_PROJECT_ID,
        name="Nord-Süd-Link Abschnitt Demo A",
        pfad=VerfahrensPfad.NABEG,
        kv_level=380,
        technology="DC",
        routing_type="mixed",
        states_crossed=["BY", "HE"],
        length_km=74.2,
        is_cross_border=False,
        is_multi_state=True,
        current_stage_index=2,
        created_at=datetime.now(),

        # ── Stage instances ──
        stages=[
            # Stage 1: Scope & Rechtsrahmen → COMPLETED (GREEN)
            StageInstance(
                id="si-s1",
                template_id="s1_scope_recht",
                status=StageStatus.COMPLETED,
                tasks=[
                    TaskInstance(
                        id="ti-s1-t1",
                        template_id="s1_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "rechtsrahmen": (
                                "Das Vorhaben \"Nord-Süd-Link Abschnitt Demo A\" ist als "
                                "länderübergreifende Höchstspannungsleitung (380 kV DC) im "
                                "Bundesbedarfsplan (BBPlG) enthalten. Gemäß § 2 Abs. 1 NABEG "
                                "findet das NABEG Anwendung, da das Vorhaben die Bundesländer "
                                "Bayern und Hessen quert und eine Spannungsebene ≥ 220 kV aufweist."
                            ),
                            "zustaendige_behoerde": "Bundesnetzagentur (BNetzA), Referat für Netzausbau",
                            "begruendung": (
                                "Die Zuordnung zum NABEG ergibt sich aus der Kennzeichnung des "
                                "Vorhabens im BBPlG als länderübergreifend (§ 2 Abs. 1 BBPlG). "
                                "Die BNetzA ist gemäß § 31 NABEG zuständige Behörde für die "
                                "Bundesfachplanung und Planfeststellung."
                            ),
                        },
                        updated_at=datetime(2026, 1, 15),
                    ),
                    TaskInstance(
                        id="ti-s1-t2",
                        template_id="s1_t2",
                        status=TaskStatus.DONE,
                        form_data={
                            "vorhaben_titel": "Nord-Süd-Link Abschnitt Demo A",
                            "technologie": "HGÜ (DC), 380 kV, gemischte Bauweise (Freileitung/Erdkabel)",
                            "trassenlaenge": "74,2 km",
                            "bundeslaender": "Bayern (BY), Hessen (HE)",
                            "zusammenfassung": (
                                "Neubau einer 380-kV-HGÜ-Verbindung als Teil des Nord-Süd-Links "
                                "zur Übertragung von Windenergie aus Norddeutschland in die "
                                "Verbrauchszentren Süddeutschlands. Die Trasse verläuft in "
                                "gemischter Bauweise (Freileitung und Erdkabel) über 74,2 km "
                                "durch Bayern und Hessen. Das Vorhaben dient der Umsetzung "
                                "der Energiewende und ist im Bundesbedarfsplan als vordringlicher "
                                "Bedarf gekennzeichnet."
                            ),
                        },
                        updated_at=datetime(2026, 1, 18),
                    ),
                    TaskInstance(
                        id="ti-s1-t3",
                        template_id="s1_t3",
                        status=TaskStatus.DONE,
                        form_data={
                            "behoerden": (
                                "• Bundesnetzagentur (BNetzA) – Genehmigungsbehörde\n"
                                "• Regierung von Oberfranken – Raumordnung BY\n"
                                "• Regierungspräsidium Kassel – Raumordnung HE\n"
                                "• Bayerisches Landesamt für Umwelt (LfU)\n"
                                "• Hessisches Landesamt für Naturschutz, Umwelt und Geologie (HLNUG)"
                            ),
                            "eigentuemer": (
                                "• Eigentümergruppe A (Demo) – Flurstück BY-091-223-17 (privat, "
                                "noch nicht kontaktiert)\n"
                                "• Gemeinde Demohausen – Flurstück HE-044-887-03 (kommunal, "
                                "Verhandlung eingeleitet)"
                            ),
                            "verbaende": (
                                "• BUND Landesverband Bayern\n"
                                "• NABU Hessen\n"
                                "• Landesbund für Vogelschutz in Bayern (LBV)\n"
                                "• Bürgerinitiative Trassenalternative e.V."
                            ),
                        },
                        updated_at=datetime(2026, 1, 22),
                    ),
                ],
            ),

            # Stage 2: Korridorfindung → COMPLETED (GREEN)
            StageInstance(
                id="si-s2",
                template_id="s2_korridor",
                status=StageStatus.COMPLETED,
                tasks=[
                    TaskInstance(
                        id="ti-s2-t1",
                        template_id="s2_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "korridor_a": (
                                "Westlicher Korridor: Verlauf entlang BAB A7, Länge 76,3 km, "
                                "überwiegend Freileitung. Querung von 2 FFH-Gebieten, "
                                "Waldanteil 18%. Minimaler Siedlungsabstand 450 m."
                            ),
                            "korridor_b": (
                                "Östlicher Korridor: Trassenführung parallel zur DB-Strecke, "
                                "72,8 km, Erdkabelanteil 35%. Querung von 1 FFH-Gebiet, "
                                "Waldanteil 12%. Minimaler Siedlungsabstand 220 m (Siedlung "
                                "Demohausen). Gute Bündelungsmöglichkeit mit Bahninfrastruktur."
                            ),
                            "vorzugskorridor": "Korridor B (östlich)",
                            "begruendung_auswahl": (
                                "Korridor B wird als Vorzugskorridor empfohlen aufgrund: "
                                "(1) geringere Betroffenheit von FFH-Gebieten (1 vs. 2), "
                                "(2) kürzere Gesamtstrecke (72,8 vs. 76,3 km), "
                                "(3) bessere Bündelung mit vorhandener Bahninfrastruktur, "
                                "(4) geringerer Gesamtraumwiderstand (Klasse II vs. III). "
                                "Der geringere Siedlungsabstand bei Demohausen (220 m) wird "
                                "durch den geplanten Erdkabelabschnitt kompensiert."
                            ),
                        },
                        updated_at=datetime(2026, 1, 28),
                    ),
                    TaskInstance(
                        id="ti-s2-t2",
                        template_id="s2_t2",
                        status=TaskStatus.DONE,
                        form_data={
                            "schutzgebiete": (
                                "• FFH-Gebiet 'Waldgebiet östlich Demo' (GL-FFH-001): "
                                "2,3 km Querung im Korridor B\n"
                                "• Wasserschutzgebiet Zone III (GL-WASSER-003): "
                                "1,1 km Randberührung im südlichen Abschnitt"
                            ),
                            "waldanteil": (
                                "Waldquerung (GL-WALD-014): ca. 8,7 km (12% der Gesamtstrecke). "
                                "Betroffene Waldflächen überwiegend Wirtschaftswald (Fichte), "
                                "2,1 km Laubmischwald mit Biotopfunktion."
                            ),
                            "siedlungsabstand": (
                                "• Ortslage Musterstadt: 320 m (Freileitung)\n"
                                "• Siedlung Demohausen: 220 m (Erdkabelabschnitt geplant)\n"
                                "• Weiler Beispielhof: 580 m (Freileitung)"
                            ),
                            "konflikte": (
                                "2 Geometrie-Konflikte >5m identifiziert:\n"
                                "• Flurstück BY-091-223-17: Überlappung mit Maststandort M-34 "
                                "(Verschiebung um 12 m möglich)\n"
                                "• Flurstück HE-044-887-03: Erdkabeltrasse tangiert "
                                "Gemeindestraße (Abstimmung mit Kommune erforderlich)"
                            ),
                        },
                        updated_at=datetime(2026, 1, 30),
                    ),
                    TaskInstance(
                        id="ti-s2-t3",
                        template_id="s2_t3",
                        status=TaskStatus.DONE,
                        form_data={
                            "methodik": (
                                "Raumwiderstandsanalyse nach BNetzA-Leitfaden (2023), "
                                "3-stufiges Bewertungsverfahren: (1) Raumwiderstandskartierung "
                                "im Maßstab 1:25.000, (2) Multikriterielle Korridorbewertung "
                                "mit 14 gewichteten Kriterien, (3) Gesamtabwägung unter "
                                "Berücksichtigung technischer Realisierbarkeit."
                            ),
                            "bewertungsergebnis": (
                                "Korridor B: Raumwiderstandsklasse II (mittel) – "
                                "Gesamtpunktzahl 67/100\n"
                                "Korridor A: Raumwiderstandsklasse III (hoch) – "
                                "Gesamtpunktzahl 48/100\n\n"
                                "Wesentliche Differenzierungskriterien: Schutzgebietsbetroffenheit "
                                "(+12 Pkt. für B), Bündelungspotenzial (+8 Pkt. für B), "
                                "Siedlungsabstand (-3 Pkt. für B)."
                            ),
                            "empfehlung": (
                                "Empfehlung zur Weiterverfolgung von Korridor B (östlich) "
                                "als Vorzugskorridor in der Bundesfachplanung. "
                                "Status: Bericht v0.9 – Überarbeitung der Kartenanhänge "
                                "erforderlich (DOC-017)."
                            ),
                        },
                        updated_at=datetime(2026, 2, 1),
                    ),
                ],
            ),

            # Stage 3: Untersuchungsrahmen → ACTIVE (YELLOW)
            StageInstance(
                id="si-s3",
                template_id="s3_untersuchungsrahmen",
                status=StageStatus.ACTIVE,
                tasks=[
                    TaskInstance(
                        id="ti-s3-t1",
                        template_id="s3_t1",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "betroffene_arten": (
                                "• Rotmilan (Milvus milvus) – 3 Brutpaare im 1-km-Radius "
                                "um Maststandorte M-12 bis M-18\n"
                                "• Schwarzstorch (Ciconia nigra) – 1 Horst im Waldgebiet "
                                "östlich Demo, 800 m Abstand zur Trasse\n"
                                "• Fledermäuse (Myotis spp.) – Quartiersverdacht in "
                                "Waldbestand bei km 34,5"
                            ),
                            "kartierungsstatus": (
                                "UNVOLLSTÄNDIG – Blocker BL-013: Kartierung Brutzeitfenster "
                                "für Rotmilan und Schwarzstorch noch ausstehend. "
                                "Fledermaus-Detektorbegehungen zu 60% abgeschlossen. "
                                "Frist für Abschluss: 20.02.2026."
                            ),
                            "vermeidungsmassnahmen": "",
                            "kompensation": "",
                        },
                        updated_at=datetime(2026, 2, 4),
                    ),
                    TaskInstance(
                        id="ti-s3-t2",
                        template_id="s3_t2",
                        status=TaskStatus.PENDING,
                        form_data={},
                    ),
                    TaskInstance(
                        id="ti-s3-t3",
                        template_id="s3_t3",
                        status=TaskStatus.PENDING,
                        form_data={},
                    ),
                ],
            ),
        ],

        # ── Rich project context ──
        blockers=[
            Blocker(
                blocker_id="BL-013",
                title="Artenschutzkartierung unvollständig",
                severity="HIGH",
                owner_role="Umweltplanung",
            ),
        ],
        geo_layers=[
            GeoLayer(
                layer_id="GL-FFH-001",
                type="FFH",
                source="public",
                geometry_ref="geojson://ffh_demo_01",
                last_update="2026-01-10",
            ),
            GeoLayer(
                layer_id="GL-WALD-014",
                type="Wald",
                source="public",
                geometry_ref="geojson://wald_demo_14",
                last_update="2025-12-15",
            ),
            GeoLayer(
                layer_id="GL-WASSER-003",
                type="Wasserschutzgebiet",
                source="public",
                geometry_ref="geojson://wsg_demo_03",
                last_update="2025-11-02",
            ),
        ],
        land_parcels=[
            LandParcel(
                parcel_id="BY-091-223-17",
                owner_type="private",
                rights_status="not_contacted",
                contact_ref="STK-OWN-101",
            ),
            LandParcel(
                parcel_id="HE-044-887-03",
                owner_type="municipal",
                rights_status="negotiation_started",
                contact_ref="STK-OWN-204",
            ),
        ],
        stakeholders=[
            Stakeholder(
                stakeholder_id="STK-OWN-101",
                type="land_owner",
                name="Eigentümergruppe A (Demo)",
                preferred_channel="letter",
            ),
            Stakeholder(
                stakeholder_id="STK-AUTH-001",
                type="authority",
                name="Zuständige Planfeststellungsbehörde (Demo)",
                preferred_channel="official_portal",
            ),
        ],
        historical_cases=[
            HistoricalCase(
                case_id="CASE-2019-047",
                title="380-kV Leitung Waldquerung Süd",
                similarity_features=SimilarityFeatures(
                    routing_type="overhead",
                    forest_crossing=True,
                    ffh_overlap=False,
                    state="BY",
                ),
                outcome="granted_with_conditions",
                key_reasons=[
                    "Frühzeitige Abstimmung mit Forstbehörde",
                    "Alternative Maststandorte belegt",
                ],
                reusable_docs=["DOC-TPL-ARTENSCHUTZ-02", "DOC-TPL-WALD-ANTRAG-01"],
            ),
            HistoricalCase(
                case_id="CASE-2021-112",
                title="Erdkabelabschnitt nahe Siedlung",
                similarity_features=SimilarityFeatures(
                    routing_type="underground",
                    settlement_distance_m=220,
                    wsg_overlap=True,
                    state="HE",
                ),
                outcome="delayed",
                key_reasons=[
                    "Hydrogeologisches Gutachten nachgefordert",
                    "Unvollständige Trassenalternativen",
                ],
                reusable_docs=["DOC-TPL-WSG-ANLAGE-03", "DOC-TPL-ALTERNATIVEN-01"],
            ),
        ],
        documents=[
            ProjectDocument(
                doc_id="DOC-001",
                doc_type="Projektsteckbrief",
                version="v1.3",
                status="approved_internal",
                source="internal",
                linked_stage="S1_SCOPE_RECHT",
            ),
            ProjectDocument(
                doc_id="DOC-017",
                doc_type="Korridoralternativenbericht",
                version="v0.9",
                status="needs_revision",
                source="internal",
                linked_stage="S2_KORRIDOR",
            ),
            ProjectDocument(
                doc_id="DOC-024",
                doc_type="Artenschutzbeitrag",
                version="v0.6",
                status="draft",
                source="internal",
                linked_stage="S3_UNTERSUCHUNGSRAHMEN",
            ),
        ],
        project_tasks=[
            ProjectTask(
                task_id="TSK-3001",
                title="Kartierung Brutzeitfenster abschließen",
                owner_role="Umweltplanung",
                due_date="2026-02-20",
                dependencies=[],
                done_definition="Vollständige Artenliste + Kartenanhänge",
            ),
            ProjectTask(
                task_id="TSK-3002",
                title="Flurstücksliste mit Korridor V2 synchronisieren",
                owner_role="GIS",
                due_date="2026-02-14",
                dependencies=["TSK-3001"],
                done_definition="Keine Geometrie-Konflikte > 5m",
            ),
        ],
        risks=[
            Risk(
                risk_id="R-11",
                category="biodiversity",
                probability=0.7,
                impact=0.8,
                mitigation="Zusatzkartierung + Trassenmikroshift",
                owner="Umweltplanung",
            ),
            Risk(
                risk_id="R-22",
                category="land_rights",
                probability=0.5,
                impact=0.9,
                mitigation="Frühzeitige Eigentümerdialoge + Alternativzufahrten",
                owner="Wegerechtsteam",
            ),
        ],
        regulatory_requirements=[
            RegulatoryRequirement(
                requirement_id="REQ-NABEG-001",
                legal_basis="NABEG",
                trigger_condition="Länderübergreifende Höchstspannungsleitung",
                required_artifacts=["Antrag_Bundesfachplanung", "Korridoralternativenbericht"],
                authority="Bundesnetzagentur",
            ),
            RegulatoryRequirement(
                requirement_id="REQ-ENWG-043",
                legal_basis="EnWG_43",
                trigger_condition="Nicht-NABEG-Fall",
                required_artifacts=["Planfeststellungsantrag", "Technische_Plansätze"],
                authority="Landesbehörde",
            ),
        ],
        draft_templates=[
            DraftTemplate(
                template_id="TPL-ANFRAGE-FORST-001",
                output_type="authority_letter",
                applicable_stage="S3_UNTERSUCHUNGSRAHMEN",
                placeholders=["behoerde_name", "vorhaben_name", "flurstuecke", "anlagenverzeichnis"],
            ),
            DraftTemplate(
                template_id="TPL-OWNER-CONTACT-002",
                output_type="land_owner_letter",
                applicable_stage="S5_BETEILIGUNG",
                placeholders=["owner_group", "trassenabschnitt", "kontakttermin", "faq_link"],
            ),
        ],
    )

    projects[demo.id] = demo
