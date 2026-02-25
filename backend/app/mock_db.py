"""In-memory database with rich demo data."""

from __future__ import annotations

from datetime import datetime

from .models import (
    Blocker,
    DraftTemplate,
    GeoLayer,
    HistoricalCase,
    LandParcel,
    PermitStatus,
    PermitType,
    Project,
    ProjectDocument,
    ProjectTask,
    RegulatoryRequirement,
    Risk,
    Section,
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
    # ── Section A: Bayern Nord (km 0–25) — most advanced ──
    section_a = Section(
        id="sec_a",
        name="Bayern Nord",
        km_start=0.0,
        km_end=25.0,
        region="Bayern",
        stages=[
            # Stage 1: COMPLETED
            StageInstance(
                id="si-a-s1",
                template_id="s1_scope_recht",
                status=StageStatus.COMPLETED,
                tasks=[
                    TaskInstance(
                        id="ti-a-s1-t1",
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
                        id="ti-a-s1-t2",
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
                                "gemischter Bauweise über 74,2 km durch Bayern und Hessen."
                            ),
                        },
                        updated_at=datetime(2026, 1, 18),
                    ),
                    TaskInstance(
                        id="ti-a-s1-t3",
                        template_id="s1_t3",
                        status=TaskStatus.DONE,
                        form_data={
                            "behoerden": (
                                "• Bundesnetzagentur (BNetzA) – Genehmigungsbehörde\n"
                                "• Regierung von Oberfranken – Raumordnung BY\n"
                                "• Bayerisches Landesamt für Umwelt (LfU)"
                            ),
                            "eigentuemer": "• Eigentümergruppe A – Flurstück BY-091-223-17 (privat, nicht kontaktiert)",
                            "verbaende": "• BUND Landesverband Bayern\n• LBV Bayern",
                        },
                        updated_at=datetime(2026, 1, 22),
                    ),
                ],
            ),
            # Stage 2: COMPLETED
            StageInstance(
                id="si-a-s2",
                template_id="s2_korridor",
                status=StageStatus.COMPLETED,
                tasks=[
                    TaskInstance(
                        id="ti-a-s2-t1",
                        template_id="s2_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "korridor_a": "Westlicher Korridor: Verlauf entlang BAB A7, Länge 27,1 km, überwiegend Freileitung. Querung von 1 FFH-Gebiet, Waldanteil 22%.",
                            "korridor_b": "Östlicher Korridor: Trassenführung parallel zur DB-Strecke, 25,0 km, Erdkabelanteil 30%. Gute Bündelungsmöglichkeit.",
                            "vorzugskorridor": "Korridor B (östlich)",
                            "begruendung_auswahl": "Korridor B empfohlen: kürzere Strecke, bessere Infrastrukturbündelung, geringerer Raumwiderstand.",
                        },
                        updated_at=datetime(2026, 1, 28),
                    ),
                    TaskInstance(
                        id="ti-a-s2-t2",
                        template_id="s2_t2",
                        status=TaskStatus.DONE,
                        form_data={
                            "schutzgebiete": "• FFH-Gebiet 'Waldgebiet östlich Demo': 2,3 km Querung\n• Wasserschutzgebiet Zone III: 0,4 km Randberührung",
                            "waldanteil": "Waldquerung ca. 3,1 km (12% des Abschnitts). Überwiegend Wirtschaftswald (Fichte).",
                            "siedlungsabstand": "• Ortslage Musterstadt: 320 m (Freileitung)",
                            "konflikte": "1 Geometrie-Konflikt: BY-091-223-17 Überlappung mit Maststandort M-34.",
                        },
                        updated_at=datetime(2026, 1, 30),
                    ),
                    TaskInstance(
                        id="ti-a-s2-t3",
                        template_id="s2_t3",
                        status=TaskStatus.DONE,
                        form_data={
                            "methodik": "Raumwiderstandsanalyse nach BNetzA-Leitfaden (2023), 3-stufiges Bewertungsverfahren.",
                            "bewertungsergebnis": "Korridor B: Raumwiderstandsklasse II (mittel) – 67/100 Pkt.\nKorridor A: Klasse III (hoch) – 48/100 Pkt.",
                            "empfehlung": "Empfehlung: Weiterverfolgung Korridor B (östlich) als Vorzugskorridor.",
                        },
                        updated_at=datetime(2026, 2, 1),
                    ),
                    TaskInstance(
                        id="ti-a-s2-t4",
                        template_id="s2_t4",
                        status=TaskStatus.DONE,
                        form_data={
                            "kreuzung_bahn": "Kreuzung DB-Strecke 5919 (Nürnberg–Bamberg) bei km 14,3. Kreuzungsvereinbarung mit DB InfraGO AG abgeschlossen (Ref. KV-2026-0471). Antrag über DB Online-Portal Ril 878 eingereicht und genehmigt.",
                            "kreuzung_strasse": "Kreuzung BAB A73 bei km 18,7. Zustimmung Autobahn GmbH Nordbayern nach § 9 FStrG erteilt. Vereinbarung unterzeichnet. Schutzmaßnahmenkonzept (Sicherheitsnetze) abgestimmt.",
                            "kreuzung_wasserstrasse": "Keine Bundeswasserstraßen im Abschnitt betroffen.",
                            "kreuzung_sonstige": "Gewässerquerung Regnitz bei km 11,2 – wasserrechtliche Abstimmung parallel (s. Wasserrecht). Gasleitung Open Grid Europe bei km 20,1 – Kreuzungsvereinbarung geschlossen.",
                            "profilplaene": "Profilpläne für DB-Kreuzung km 14,3 und BAB-Kreuzung km 18,7 erstellt und genehmigt.",
                            "schutzmassnahmen_kreuzung": "Sicherheitsnetze über BAB A73 während Seilzug (3 Nächte Sperrung vereinbart). DB-Sperrpause für Seilzug: 2×8h.",
                            "kostenteilung": "Kostenteilung DB nach § 11 EBKrG: 100% Vorhabenträger. BAB nach § 12 FStrG: 100% Vorhabenträger.",
                            "vereinbarungen_status": "3 von 3 Vereinbarungen abgeschlossen.",
                        },
                        updated_at=datetime(2026, 2, 3),
                        completed_checklist=[0, 1, 2, 3, 5, 6, 7, 8, 9],
                    ),
                ],
            ),
            # Stage 3: ACTIVE
            StageInstance(
                id="si-a-s3",
                template_id="s3_untersuchungsrahmen",
                status=StageStatus.ACTIVE,
                tasks=[
                    TaskInstance(
                        id="ti-a-s3-t1",
                        template_id="s3_t1",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "betroffene_arten": (
                                "• Rotmilan (Milvus milvus) – 3 Brutpaare im 1-km-Radius\n"
                                "• Schwarzstorch (Ciconia nigra) – 1 Horst, 800 m Abstand\n"
                                "• Fledermäuse (Myotis spp.) – Quartiersverdacht bei km 12,5"
                            ),
                            "kartierungsstatus": "UNVOLLSTÄNDIG – Blocker BL-013: Kartierung Brutzeitfenster noch ausstehend. Fledermaus-Detektorbegehungen zu 60% abgeschlossen.",
                            "vermeidungsmassnahmen": "",
                            "kompensation": "",
                        },
                        updated_at=datetime(2026, 2, 4),
                    ),
                    TaskInstance(id="ti-a-s3-t2", template_id="s3_t2", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-a-s3-t3", template_id="s3_t3", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(
                        id="ti-a-s3-t4",
                        template_id="s3_t4",
                        status=TaskStatus.DONE,
                        form_data={
                            "gewaesserquerungen": "Regnitz-Querung bei km 11,2 (Überspannung, Spannfeld 180 m).\nKleingewässer bei km 22,1 (Erdkabelquerung, HDD-Bohrung, 45 m Bohrtiefe).",
                            "grundwasser": "Grundwasserflurabstand > 3 m im gesamten Abschnitt. Keine dauerhafte Beeinflussung erwartet. Bauwasserhaltung nur für Kabelgraben km 20–23 erforderlich (max. 15 m³/h).",
                            "schutzgebiete_wasser": "Wasserschutzgebiet Zone III bei km 9,5–10,8 (Randberührung). Kein Überschwemmungsgebiet betroffen.",
                            "hydrogeologie": "Hydrogeologisches Gutachten (Ing.-Büro Wassermann, Jan. 2026): Durchlässiger Aquifer (kf = 2×10⁻⁴ m/s), keine Grundwassergefährdung bei Einhaltung der Schutzmaßnahmen.",
                            "schutzmassnahmen_wasser": "Bauzeitliche Gewässerschutzmaßnahmen gemäß § 5 WHG. Ölhavariekonzept. Gewässerrandstreifen-Befreiung nach § 38 WHG erteilt.",
                            "antrag_status_wasser": "Wasserrechtliche Erlaubnis erteilt (Bescheid WWA-2026-0089 vom 15.01.2026). In PFB integriert (Konzentrationswirkung § 24 NABEG).",
                        },
                        updated_at=datetime(2026, 1, 25),
                        completed_checklist=[0, 1, 2, 3, 4, 5, 6, 8],
                    ),
                    TaskInstance(
                        id="ti-a-s3-t5",
                        template_id="s3_t5",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "bodendenkmale": "1 bekanntes Bodendenkmal (mittelalterliche Siedlungsreste, Denkmalliste Nr. D-4-6131-0047) bei km 8,4. Archäologische Baubegleitung erforderlich.",
                            "baudenkmale": "Keine Baudenkmale im direkten Trassenbereich. Denkmalensemble Schloss Musterheim (D-4-6131-0012) in 800 m Entfernung – Sichtbarkeitsanalyse durchgeführt: keine Beeinträchtigung.",
                            "prospektion": "Feldbegehungen abgeschlossen (km 0–25). Geomagnetische Prospektion zu 70% durchgeführt. Magnetometer-Survey ausstehend für km 6–10. Georadar für Verdachtsfläche km 8,4 beauftragt.",
                            "rettungsgrabung": "",
                            "trassenoptimierung": "Mikroverlagerung der Trasse um 15 m bei km 8,4 geprüft – Bodendenkmal kann nicht vollständig umgangen werden. Rettungsgrabung voraussichtlich erforderlich.",
                            "auflagen_denkmal": "",
                        },
                        updated_at=datetime(2026, 2, 10),
                        completed_checklist=[0, 1, 2, 3, 4],
                    ),
                    TaskInstance(
                        id="ti-a-s3-t6",
                        template_id="s3_t6",
                        status=TaskStatus.DONE,
                        form_data={
                            "leitungstyp": "380 kV DC (HGÜ), gemischte Bauweise (Freileitung km 0–18, Erdkabel km 18–25)",
                            "emf_berechnung": "EMF-Berechnung nach DIN EN 50413 für alle 47 Maststandorte und Erdkabelabschnitt. Maximale magnetische Flussdichte: 28 µT am nächsten Immissionsort (Grenzwert DC: 500 µT). Elektrische Feldstärke: 1,2 kV/m (Grenzwert: 5 kV/m).",
                            "immissionsorte": "Nächster Immissionsort: Wohngebiet Musterstadt, Abstand 320 m (Freileitung). Schule am Waldrand, Abstand 580 m. Alle Abstände > 200 m-Mindestabstand.",
                            "grenzwertvergleich": "Alle Grenzwerte der 26. BImSchV § 3 werden eingehalten. B-Feld: 28 µT / 500 µT (5,6% des Grenzwerts). E-Feld: 1,2 kV/m / 5 kV/m (24% des Grenzwerts).",
                            "minimierung": "Minimierungsmaßnahmen nach § 4: Kompaktmaste (Donaumast), optimierte Leiteranordnung, erhöhte Mastfußhöhe (+5 m) bei Siedlungsnähe. Keine Trassenführung über Wohngebäude (§ 4 Abs. 3).",
                            "schallprognose": "Koronageräusche: max. 35 dB(A) nachts an nächstgelegener Wohnbebauung (Grenzwert TA Lärm: 45 dB(A) allg. Wohngebiet nachts). Einhaltung mit Reserve.",
                            "anzeige_behoerde": "Anzeige nach § 7 an Immissionsschutzbehörde Oberfranken am 10.01.2026. Stellungnahme erhalten: keine Einwände.",
                        },
                        updated_at=datetime(2026, 1, 20),
                        completed_checklist=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                    ),
                ],
            ),
        ],
    )

    # ── Section B: Grenzbereich BY-HE (km 25–50) — medium progress ──
    section_b = Section(
        id="sec_b",
        name="Grenzbereich BY-HE",
        km_start=25.0,
        km_end=50.0,
        region="Bayern/Hessen",
        stages=[
            # Stage 1: COMPLETED
            StageInstance(
                id="si-b-s1",
                template_id="s1_scope_recht",
                status=StageStatus.COMPLETED,
                tasks=[
                    TaskInstance(
                        id="ti-b-s1-t1",
                        template_id="s1_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "rechtsrahmen": "NABEG anwendbar gemäß § 2 Abs. 1 BBPlG. Abschnitt quert Landesgrenze BY/HE.",
                            "zustaendige_behoerde": "Bundesnetzagentur (BNetzA)",
                            "begruendung": "Länderübergreifender Abschnitt, Spannungsebene 380 kV ≥ 220 kV.",
                        },
                        updated_at=datetime(2026, 1, 20),
                    ),
                    TaskInstance(
                        id="ti-b-s1-t2",
                        template_id="s1_t2",
                        status=TaskStatus.DONE,
                        form_data={
                            "vorhaben_titel": "Nord-Süd-Link – Grenzbereich BY-HE",
                            "technologie": "HGÜ (DC), 380 kV, Erdkabel",
                            "trassenlaenge": "25,0 km",
                            "bundeslaender": "Bayern (BY), Hessen (HE)",
                            "zusammenfassung": "Erdkabelabschnitt im Grenzbereich Bayern/Hessen. Besondere Herausforderungen durch Topographie und Gewässerquerungen.",
                        },
                        updated_at=datetime(2026, 1, 22),
                    ),
                    TaskInstance(
                        id="ti-b-s1-t3",
                        template_id="s1_t3",
                        status=TaskStatus.DONE,
                        form_data={
                            "behoerden": "• BNetzA\n• Regierungspräsidium Kassel\n• Regierung von Oberfranken",
                            "eigentuemer": "• Gemeinde Demohausen – Flurstück HE-044-887-03 (kommunal, Verhandlung eingeleitet)",
                            "verbaende": "• NABU Hessen\n• Bürgerinitiative Trassenalternative e.V.",
                        },
                        updated_at=datetime(2026, 1, 25),
                    ),
                ],
            ),
            # Stage 2: ACTIVE
            StageInstance(
                id="si-b-s2",
                template_id="s2_korridor",
                status=StageStatus.ACTIVE,
                tasks=[
                    TaskInstance(
                        id="ti-b-s2-t1",
                        template_id="s2_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "korridor_a": "Südlicher Korridor: 26,8 km, Erdkabel 100%, Querung von 2 Gewässern.",
                            "korridor_b": "Nördlicher Korridor: 24,5 km, Erdkabel 100%, Bündelung mit BAB A7.",
                            "vorzugskorridor": "Korridor B (nördlich)",
                            "begruendung_auswahl": "Kürzere Strecke, bessere Autobahnbündelung, geringere Gewässerquerung.",
                        },
                        updated_at=datetime(2026, 2, 5),
                    ),
                    TaskInstance(
                        id="ti-b-s2-t2",
                        template_id="s2_t2",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "schutzgebiete": "• Wasserschutzgebiet Zone III: 1,8 km Querung",
                            "waldanteil": "",
                            "siedlungsabstand": "",
                            "konflikte": "",
                        },
                        updated_at=datetime(2026, 2, 10),
                    ),
                    TaskInstance(id="ti-b-s2-t3", template_id="s2_t3", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(
                        id="ti-b-s2-t4",
                        template_id="s2_t4",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "kreuzung_bahn": "Keine Bahnkreuzung im Abschnitt BY-HE.",
                            "kreuzung_strasse": "Kreuzung BAB A7 bei km 32,5. Antrag auf Zustimmung nach § 9 FStrG bei Autobahn GmbH eingereicht. Technische Prüfung läuft.",
                            "kreuzung_wasserstrasse": "Mainquerung bei km 41,0 – Bundeswasserstraße! Anzeige nach § 31 WaStrG beim WSA Schweinfurt eingereicht. Technische Machbarkeitsstudie (HDD-Bohrung) beauftragt.",
                            "kreuzung_sonstige": "Erdgasleitung bayernets bei km 38,2 – Kreuzungsvereinbarung in Vorbereitung.",
                            "profilplaene": "Profilpläne für BAB A7 erstellt. Querungspläne Main in Bearbeitung.",
                            "schutzmassnahmen_kreuzung": "",
                            "kostenteilung": "",
                            "vereinbarungen_status": "0 von 3 Vereinbarungen abgeschlossen. Alle in Abstimmung.",
                        },
                        updated_at=datetime(2026, 2, 8),
                        completed_checklist=[0, 1, 3],
                    ),
                ],
            ),
            # Stage 3: PENDING
            StageInstance(
                id="si-b-s3",
                template_id="s3_untersuchungsrahmen",
                status=StageStatus.PENDING,
                tasks=[
                    TaskInstance(id="ti-b-s3-t1", template_id="s3_t1", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-b-s3-t2", template_id="s3_t2", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-b-s3-t3", template_id="s3_t3", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-b-s3-t4", template_id="s3_t4", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-b-s3-t5", template_id="s3_t5", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-b-s3-t6", template_id="s3_t6", status=TaskStatus.PENDING, form_data={}),
                ],
            ),
        ],
    )

    # ── Section C: Hessen Süd (km 50–74.2) — early stage ──
    section_c = Section(
        id="sec_c",
        name="Hessen Süd",
        km_start=50.0,
        km_end=74.2,
        region="Hessen",
        stages=[
            # Stage 1: ACTIVE
            StageInstance(
                id="si-c-s1",
                template_id="s1_scope_recht",
                status=StageStatus.ACTIVE,
                tasks=[
                    TaskInstance(
                        id="ti-c-s1-t1",
                        template_id="s1_t1",
                        status=TaskStatus.DONE,
                        form_data={
                            "rechtsrahmen": "NABEG anwendbar. Abschnitt liegt vollständig in Hessen.",
                            "zustaendige_behoerde": "Bundesnetzagentur (BNetzA)",
                            "begruendung": "Teil des länderübergreifenden Gesamtvorhabens gemäß BBPlG.",
                        },
                        updated_at=datetime(2026, 2, 8),
                    ),
                    TaskInstance(
                        id="ti-c-s1-t2",
                        template_id="s1_t2",
                        status=TaskStatus.IN_PROGRESS,
                        form_data={
                            "vorhaben_titel": "Nord-Süd-Link – Hessen Süd",
                            "technologie": "HGÜ (DC), 380 kV, gemischte Bauweise",
                            "trassenlaenge": "",
                            "bundeslaender": "",
                            "zusammenfassung": "",
                        },
                        updated_at=datetime(2026, 2, 12),
                    ),
                    TaskInstance(id="ti-c-s1-t3", template_id="s1_t3", status=TaskStatus.PENDING, form_data={}),
                ],
            ),
            # Stage 2: PENDING
            StageInstance(
                id="si-c-s2",
                template_id="s2_korridor",
                status=StageStatus.PENDING,
                tasks=[
                    TaskInstance(id="ti-c-s2-t1", template_id="s2_t1", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s2-t2", template_id="s2_t2", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s2-t3", template_id="s2_t3", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s2-t4", template_id="s2_t4", status=TaskStatus.PENDING, form_data={}),
                ],
            ),
            # Stage 3: PENDING
            StageInstance(
                id="si-c-s3",
                template_id="s3_untersuchungsrahmen",
                status=StageStatus.PENDING,
                tasks=[
                    TaskInstance(id="ti-c-s3-t1", template_id="s3_t1", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s3-t2", template_id="s3_t2", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s3-t3", template_id="s3_t3", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s3-t4", template_id="s3_t4", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s3-t5", template_id="s3_t5", status=TaskStatus.PENDING, form_data={}),
                    TaskInstance(id="ti-c-s3-t6", template_id="s3_t6", status=TaskStatus.PENDING, form_data={}),
                ],
            ),
        ],
    )

    # ── Permit statuses across sections ──
    permits = [
        # Section A permits
        PermitStatus(id="P-A-01", section_id="sec_a", permit_type=PermitType.NATURSCHUTZ, label="Naturschutzgenehmigung", status="in_progress"),
        PermitStatus(id="P-A-02", section_id="sec_a", permit_type=PermitType.NATURSCHUTZ, label="FFH-Verträglichkeitsprüfung", status="open"),
        PermitStatus(id="P-A-03", section_id="sec_a", permit_type=PermitType.WALDUMWANDLUNG, label="Waldumwandlungsgenehmigung", status="in_progress"),
        PermitStatus(id="P-A-04", section_id="sec_a", permit_type=PermitType.WASSERRECHT, label="Wasserrechtliche Erlaubnis", status="approved"),
        PermitStatus(id="P-A-05", section_id="sec_a", permit_type=PermitType.KREUZUNG, label="Kreuzungsvereinbarung DB", status="approved"),
        PermitStatus(id="P-A-06", section_id="sec_a", permit_type=PermitType.IMMISSION, label="Immissionsschutznachweis", status="approved"),
        PermitStatus(id="P-A-07", section_id="sec_a", permit_type=PermitType.DENKMALSCHUTZ, label="Denkmalschutzrechtliche Genehmigung (Bodendenkmal)", status="in_progress"),
        # Section B permits
        PermitStatus(id="P-B-01", section_id="sec_b", permit_type=PermitType.NATURSCHUTZ, label="Naturschutzgenehmigung", status="open"),
        PermitStatus(id="P-B-02", section_id="sec_b", permit_type=PermitType.WASSERRECHT, label="Wasserrechtliche Erlaubnis", status="open"),
        PermitStatus(id="P-B-03", section_id="sec_b", permit_type=PermitType.WASSERRECHT, label="Gew\u00e4sserquerungsgenehmigung", status="open"),
        PermitStatus(id="P-B-04", section_id="sec_b", permit_type=PermitType.KREUZUNG, label="Kreuzungsvereinbarung BAB", status="in_progress"),
        PermitStatus(id="P-B-05", section_id="sec_b", permit_type=PermitType.DENKMALSCHUTZ, label="Denkmalschutzrechtliche Genehmigung", status="open"),
        PermitStatus(id="P-B-06", section_id="sec_b", permit_type=PermitType.WALDUMWANDLUNG, label="Waldumwandlungsgenehmigung (Grenzbereich)", status="open"),
        PermitStatus(id="P-B-07", section_id="sec_b", permit_type=PermitType.IMMISSION, label="Immissionsschutznachweis (Grenzbereich)", status="open"),
        # Section C permits
        PermitStatus(id="P-C-01", section_id="sec_c", permit_type=PermitType.NATURSCHUTZ, label="Naturschutzgenehmigung", status="open"),
        PermitStatus(id="P-C-02", section_id="sec_c", permit_type=PermitType.WALDUMWANDLUNG, label="Waldumwandlungsgenehmigung", status="open"),
        PermitStatus(id="P-C-03", section_id="sec_c", permit_type=PermitType.WALDUMWANDLUNG, label="Waldausgleichsnachweis", status="open"),
        PermitStatus(id="P-C-04", section_id="sec_c", permit_type=PermitType.KREUZUNG, label="Kreuzungsvereinbarung DB", status="open"),
        PermitStatus(id="P-C-05", section_id="sec_c", permit_type=PermitType.IMMISSION, label="Immissionsschutznachweis", status="open"),
        PermitStatus(id="P-C-06", section_id="sec_c", permit_type=PermitType.WASSERRECHT, label="Wasserrechtliche Erlaubnis (Hessen)", status="open"),
        PermitStatus(id="P-C-07", section_id="sec_c", permit_type=PermitType.DENKMALSCHUTZ, label="Denkmalschutzrechtliche Genehmigung (Hessen)", status="open"),
    ]

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
        current_stage_index=0,
        created_at=datetime.now(),

        # Stages empty — stages now live in sections
        stages=[],

        # Sections with independent workflow progress
        sections=[section_a, section_b, section_c],

        # Permits
        permits=permits,

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
            GeoLayer(layer_id="GL-FFH-001", type="FFH", source="public", geometry_ref="geojson://ffh_demo_01", last_update="2026-01-10"),
            GeoLayer(layer_id="GL-WALD-014", type="Wald", source="public", geometry_ref="geojson://wald_demo_14", last_update="2025-12-15"),
            GeoLayer(layer_id="GL-WASSER-003", type="Wasserschutzgebiet", source="public", geometry_ref="geojson://wsg_demo_03", last_update="2025-11-02"),
        ],
        land_parcels=[
            LandParcel(parcel_id="BY-091-223-17", owner_type="private", rights_status="not_contacted", contact_ref="STK-OWN-101"),
            LandParcel(parcel_id="HE-044-887-03", owner_type="municipal", rights_status="negotiation_started", contact_ref="STK-OWN-204"),
        ],
        stakeholders=[
            Stakeholder(stakeholder_id="STK-OWN-101", type="land_owner", name="Eigentümergruppe A (Demo)", preferred_channel="letter"),
            Stakeholder(stakeholder_id="STK-AUTH-001", type="authority", name="Zuständige Planfeststellungsbehörde (Demo)", preferred_channel="official_portal"),
        ],
        historical_cases=[
            HistoricalCase(
                case_id="CASE-2019-047",
                title="380-kV Leitung Waldquerung Süd",
                similarity_features=SimilarityFeatures(routing_type="overhead", forest_crossing=True, ffh_overlap=False, state="BY"),
                outcome="granted_with_conditions",
                key_reasons=["Frühzeitige Abstimmung mit Forstbehörde", "Alternative Maststandorte belegt"],
                reusable_docs=["DOC-TPL-ARTENSCHUTZ-02", "DOC-TPL-WALD-ANTRAG-01"],
            ),
            HistoricalCase(
                case_id="CASE-2021-112",
                title="Erdkabelabschnitt nahe Siedlung",
                similarity_features=SimilarityFeatures(routing_type="underground", settlement_distance_m=220, wsg_overlap=True, state="HE"),
                outcome="delayed",
                key_reasons=["Hydrogeologisches Gutachten nachgefordert", "Unvollständige Trassenalternativen"],
                reusable_docs=["DOC-TPL-WSG-ANLAGE-03", "DOC-TPL-ALTERNATIVEN-01"],
            ),
        ],
        documents=[
            ProjectDocument(doc_id="DOC-001", doc_type="Projektsteckbrief", version="v1.3", status="approved_internal", source="internal", linked_stage="S1_SCOPE_RECHT"),
            ProjectDocument(doc_id="DOC-017", doc_type="Korridoralternativenbericht", version="v0.9", status="needs_revision", source="internal", linked_stage="S2_KORRIDOR"),
            ProjectDocument(doc_id="DOC-024", doc_type="Artenschutzbeitrag", version="v0.6", status="draft", source="internal", linked_stage="S3_UNTERSUCHUNGSRAHMEN"),
        ],
        project_tasks=[
            ProjectTask(task_id="TSK-3001", title="Kartierung Brutzeitfenster abschließen", owner_role="Umweltplanung", due_date="2026-02-20", dependencies=[], done_definition="Vollständige Artenliste + Kartenanhänge"),
            ProjectTask(task_id="TSK-3002", title="Flurstücksliste mit Korridor V2 synchronisieren", owner_role="GIS", due_date="2026-02-14", dependencies=["TSK-3001"], done_definition="Keine Geometrie-Konflikte > 5m"),
        ],
        risks=[
            Risk(risk_id="R-11", category="biodiversity", probability=0.7, impact=0.8, mitigation="Zusatzkartierung + Trassenmikroshift", owner="Umweltplanung"),
            Risk(risk_id="R-22", category="land_rights", probability=0.5, impact=0.9, mitigation="Frühzeitige Eigentümerdialoge + Alternativzufahrten", owner="Wegerechtsteam"),
        ],
        regulatory_requirements=[
            RegulatoryRequirement(requirement_id="REQ-NABEG-001", legal_basis="NABEG", trigger_condition="Länderübergreifende Höchstspannungsleitung", required_artifacts=["Antrag_Bundesfachplanung", "Korridoralternativenbericht"], authority="Bundesnetzagentur"),
            RegulatoryRequirement(requirement_id="REQ-ENWG-043", legal_basis="EnWG_43", trigger_condition="Nicht-NABEG-Fall", required_artifacts=["Planfeststellungsantrag", "Technische_Plansätze"], authority="Landesbehörde"),
        ],
        draft_templates=[
            DraftTemplate(template_id="TPL-ANFRAGE-FORST-001", output_type="authority_letter", applicable_stage="S3_UNTERSUCHUNGSRAHMEN", placeholders=["behoerde_name", "vorhaben_name", "flurstuecke", "anlagenverzeichnis"]),
            DraftTemplate(template_id="TPL-OWNER-CONTACT-002", output_type="land_owner_letter", applicable_stage="S5_BETEILIGUNG", placeholders=["owner_group", "trassenabschnitt", "kontakttermin", "faq_link"]),
        ],
    )

    projects[demo.id] = demo
