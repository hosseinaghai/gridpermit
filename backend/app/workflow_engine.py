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
                TaskTemplate(
                    id="s2_t4",
                    title="Kreuzungsvereinbarungen vorbereiten",
                    description=(
                        "Vorbereitung und Abschluss von Kreuzungsvereinbarungen mit Infrastrukturbetreibern "
                        "gem\u00e4\u00df EBKrG (\u00a7\u00a7 2, 3, 11), \u00a7 9 FStrG (Bauverbot/Zustimmungszonen an Bundesfernstra\u00dfen), "
                        "\u00a7 31 WaStrG (Bundeswasserstra\u00dfen) sowie SKR 2016/Ril 878 (Stromleitungskreuzungsrichtlinien DB)."
                    ),
                    form_fields=[
                        FormField(name="kreuzung_bahn", label="Kreuzung Bahnstrecken (DB InfraGO, SKR 2016/Ril 878)", type="textarea"),
                        FormField(name="kreuzung_strasse", label="Kreuzung Bundesfernstra\u00dfen (\u00a7 9 FStrG, Autobahn GmbH)", type="textarea"),
                        FormField(name="kreuzung_wasserstrasse", label="Kreuzung Bundeswasserstra\u00dfen (\u00a7 31 WaStrG)", type="textarea"),
                        FormField(name="kreuzung_sonstige", label="Sonstige Kreuzungen (Pipelines, Telekom, andere Leitungen)", type="textarea"),
                        FormField(name="profilplaene", label="Freileitungs-Profilpl\u00e4ne & L\u00e4ngsschnitte", type="textarea"),
                        FormField(name="schutzmassnahmen_kreuzung", label="Schutzma\u00dfnahmenkonzept (Sicherheitsnetze, Bauzeitr\u00e4ume)", type="textarea"),
                        FormField(name="kostenteilung", label="Kostenteilung (\u00a7 12 FStrG / \u00a7 11 EBKrG)", type="textarea"),
                        FormField(name="vereinbarungen_status", label="Status der Kreuzungsvereinbarungen", type="textarea"),
                    ],
                    checklist=[
                        "Kreuzungsstellen identifiziert und kartiert",
                        "DB InfraGO AG kontaktiert (Online-Portal Ril 878)",
                        "Kreuzungsantrag DB eingereicht (Formular 878.2202A07)",
                        "Autobahn GmbH kontaktiert (\u00a7 9 FStrG Zustimmung)",
                        "WSA-Genehmigung f\u00fcr Bundeswasserstra\u00dfen beantragt (\u00a7 31 WaStrG)",
                        "Profilpl\u00e4ne und Lageplaneerstellt",
                        "Technische Pr\u00fcfung durch Kreuzungspartner abgeschlossen",
                        "Schutzma\u00dfnahmenkonzept abgestimmt",
                        "Kreuzungsvereinbarungen unterzeichnet",
                        "Baufenster und Sperrpausen koordiniert",
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
                TaskTemplate(
                    id="s3_t4",
                    title="Wasserrechtliche Genehmigung beantragen",
                    description=(
                        "Beantragung der wasserrechtlichen Erlaubnis gem\u00e4\u00df WHG: "
                        "\u00a7 8 (Erlaubnis-/Bewilligungspflicht), \u00a7 36 (Anlagen an Gew\u00e4ssern), "
                        "\u00a7 38 (Gew\u00e4sserrandstreifen), \u00a7 52 (Wasserschutzgebiete), "
                        "\u00a7 78 (Hochwasser-/\u00dcberschwemmungsgebiete). "
                        "Konzentrationswirkung gem\u00e4\u00df \u00a7 24 NABEG i.V.m. \u00a7 70 WHG."
                    ),
                    form_fields=[
                        FormField(name="gewaesserquerungen", label="Gew\u00e4sserquerungen (Bezeichnung, Stationierung, Querungsmethode)", type="textarea"),
                        FormField(name="grundwasser", label="Grundwasserbeeinflussung (Flurabstand, Bauwasserh.)", type="textarea"),
                        FormField(name="schutzgebiete_wasser", label="Betr. Wasserschutzgebiete (\u00a7 52 WHG) & \u00dcberschwemmungsgebiete (\u00a7 78 WHG)", type="textarea"),
                        FormField(name="hydrogeologie", label="Hydrogeologisches Gutachten (Ergebnisse)", type="textarea"),
                        FormField(name="schutzmassnahmen_wasser", label="Gew\u00e4sserschutzma\u00dfnahmen & Bauwasserhaltungskonzept", type="textarea"),
                        FormField(name="antrag_status_wasser", label="Antragsstatus bei Wasserbeh\u00f6rde", type="textarea"),
                    ],
                    checklist=[
                        "Gew\u00e4sserquerungen identifiziert und kartiert",
                        "Hydrogeologisches Gutachten erstellt",
                        "Gew\u00e4sserkreuzungspl\u00e4ne erstellt (1:5.000)",
                        "\u00dcberschwemmungsgebiet-Vertr\u00e4glichkeit gepr\u00fcft (\u00a7 78 WHG)",
                        "Wasserschutzgebiet-Vertr\u00e4glichkeit gepr\u00fcft (\u00a7 52 WHG)",
                        "Bauwasserhaltungskonzept erstellt",
                        "Untere Wasserbeh\u00f6rde Stellungnahme eingeholt",
                        "WSA-Genehmigung f\u00fcr Bundeswasserstra\u00dfen beantragt (\u00a7 31 WaStrG)",
                        "\u00d6kologische Baubegleitung beauftragt",
                    ],
                ),
                TaskTemplate(
                    id="s3_t5",
                    title="Denkmalschutzpr\u00fcfung durchf\u00fchren",
                    description=(
                        "Pr\u00fcfung denkmalschutzrechtlicher Belange gem\u00e4\u00df Landes-DSchG und Europ\u00e4ischer "
                        "Konvention zum Schutz des arch\u00e4ologischen Erbes (Valletta-Konvention 1992). "
                        "Konzentrationswirkung \u00a7 24 NABEG. Verursacherprinzip: Vorhabentr\u00e4ger tr\u00e4gt "
                        "Kosten f\u00fcr Prospektion und Rettungsgrabungen."
                    ),
                    form_fields=[
                        FormField(name="bodendenkmale", label="Bekannte Bodendenkmale im Trassenbereich (Denkmalliste)", type="textarea"),
                        FormField(name="baudenkmale", label="Baudenkmale & Denkmalensembles im Umkreis", type="textarea"),
                        FormField(name="prospektion", label="Arch\u00e4ologische Prospektion (Feldbegehung, Geomagnetik, Georadar)", type="textarea"),
                        FormField(name="rettungsgrabung", label="Rettungsgrabungen (Ergebnisse & Dokumentation)", type="textarea"),
                        FormField(name="trassenoptimierung", label="Trassenverlagerung zur Denkmalvermeidung", type="textarea"),
                        FormField(name="auflagen_denkmal", label="Denkmalschutzrechtliche Auflagen & Nebenbestimmungen", type="textarea"),
                    ],
                    checklist=[
                        "Denkmallisten und Bodendenkmal-Kartierung abgeglichen",
                        "Landesamt f\u00fcr Denkmalpflege kontaktiert/Stellungnahme angefordert",
                        "Denkmalrechtlicher Fachbeitrag erstellt",
                        "Feldbegehungen durchgef\u00fchrt",
                        "Geomagnetische Prospektion durchgef\u00fchrt",
                        "Georadar-Untersuchung durchgef\u00fchrt (falls erforderlich)",
                        "Trassenoptimierung zur Denkmalvermeidung gepr\u00fcft",
                        "Rettungsgrabungen durchgef\u00fchrt (falls erforderlich)",
                        "Arch\u00e4ologische Baubegleitung vertraglich geregelt",
                        "Kosten nach Verursacherprinzip erfasst",
                    ],
                ),
                TaskTemplate(
                    id="s3_t6",
                    title="Immissionsschutznachweis erstellen",
                    description=(
                        "Nachweis der Einhaltung der Grenzwerte gem\u00e4\u00df 26. BImSchV: "
                        "\u00a7 3 (Grenzwerte Niederfrequenzanlagen: 5 kV/m E-Feld, 100 \u00b5T B-Feld bei 50 Hz; "
                        "500 \u00b5T f\u00fcr Gleichstromanlagen), "
                        "\u00a7 4 (Minimierungsgebot), "
                        "\u00a7 5 (Berechnung nach DIN EN 50413), "
                        "\u00a7 7 (Anzeigepflicht bei Immissionsschutzbeh\u00f6rde). "
                        "Zus\u00e4tzlich Schallimmissionsprognose gem\u00e4\u00df TA L\u00e4rm f\u00fcr Koronager\u00e4usche."
                    ),
                    form_fields=[
                        FormField(name="leitungstyp", label="Leitungstyp (AC/DC, Spannung, Freileitung/Erdkabel)", type="text"),
                        FormField(name="emf_berechnung", label="EMF-Berechnung nach DIN EN 50413 (E-Feld kV/m, B-Feld \u00b5T)", type="textarea"),
                        FormField(name="immissionsorte", label="Empfindliche Immissionsorte (Wohngeb\u00e4ude, Schulen, Abst\u00e4nde)", type="textarea"),
                        FormField(name="grenzwertvergleich", label="Grenzwertvergleich (\u00a7 3 Abs. 2: 100 \u00b5T bei 50 Hz / 500 \u00b5T DC)", type="textarea"),
                        FormField(name="minimierung", label="Minimierungsma\u00dfnahmen nach \u00a7 4 (Phasenlage, Masttyp, H\u00f6he)", type="textarea"),
                        FormField(name="schallprognose", label="Schallimmissionsprognose (Koronager\u00e4usche, dB(A) an Immissionsorten)", type="textarea"),
                        FormField(name="anzeige_behoerde", label="Anzeige nach \u00a7 7 an Immissionsschutzbeh\u00f6rde (Datum, Status)", type="textarea"),
                    ],
                    checklist=[
                        "Empfindliche Immissionsorte entlang der Trasse identifiziert",
                        "EMF-Berechnung nach DIN EN 50413 durchgef\u00fchrt",
                        "Elektrische Feldst\u00e4rke < 5 kV/m an allen Immissionsorten nachgewiesen",
                        "Magnetische Flussdichte < 100 \u00b5T (50 Hz) / < 500 \u00b5T (DC) nachgewiesen",
                        "Minimierungsma\u00dfnahmen nach \u00a7 4 dokumentiert",
                        "Freileitungstrasse f\u00fchrt nicht \u00fcber Wohngeb\u00e4ude (\u00a7 4 Abs. 3)",
                        "Schallimmissionsprognose erstellt (TA L\u00e4rm)",
                        "Anzeige nach \u00a7 7 an Immissionsschutzbeh\u00f6rde \u00fcbermittelt",
                        "Stellungnahme der Immissionsschutzbeh\u00f6rde eingeholt",
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
                TaskTemplate(
                    id="s2_t4",
                    title="Prepare Crossing Agreements",
                    description=(
                        "Preparation and conclusion of crossing agreements with infrastructure operators "
                        "pursuant to EBKrG (\u00a7\u00a7 2, 3, 11), \u00a7 9 FStrG (building restrictions near federal highways), "
                        "\u00a7 31 WaStrG (federal waterways), and SKR 2016/Ril 878 (DB power line crossing guidelines)."
                    ),
                    form_fields=[
                        FormField(name="kreuzung_bahn", label="Railway Crossings (DB InfraGO, SKR 2016/Ril 878)", type="textarea"),
                        FormField(name="kreuzung_strasse", label="Federal Highway Crossings (\u00a7 9 FStrG, Autobahn GmbH)", type="textarea"),
                        FormField(name="kreuzung_wasserstrasse", label="Federal Waterway Crossings (\u00a7 31 WaStrG)", type="textarea"),
                        FormField(name="kreuzung_sonstige", label="Other Crossings (Pipelines, Telecom, Other Lines)", type="textarea"),
                        FormField(name="profilplaene", label="Overhead Line Profile Plans & Cross-Sections", type="textarea"),
                        FormField(name="schutzmassnahmen_kreuzung", label="Protective Measures Concept (Safety Nets, Timing)", type="textarea"),
                        FormField(name="kostenteilung", label="Cost Allocation (\u00a7 12 FStrG / \u00a7 11 EBKrG)", type="textarea"),
                        FormField(name="vereinbarungen_status", label="Crossing Agreement Status", type="textarea"),
                    ],
                    checklist=[
                        "Crossing locations identified and mapped",
                        "DB InfraGO AG contacted (Online Portal Ril 878)",
                        "DB crossing application submitted (Form 878.2202A07)",
                        "Autobahn GmbH contacted (\u00a7 9 FStrG approval)",
                        "WSA permit for federal waterways applied (\u00a7 31 WaStrG)",
                        "Profile plans and site plans prepared",
                        "Technical review by crossing partner completed",
                        "Protective measures concept agreed",
                        "Crossing agreements signed",
                        "Construction windows and track closures coordinated",
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
                TaskTemplate(
                    id="s3_t4",
                    title="Apply for Water Law Permit",
                    description=(
                        "Application for water law permit pursuant to WHG: "
                        "\u00a7 8 (permit/authorization requirement), \u00a7 36 (facilities at water bodies), "
                        "\u00a7 38 (riparian buffer strips), \u00a7 52 (water protection areas), "
                        "\u00a7 78 (flood zones). Concentration effect per \u00a7 24 NABEG in conjunction with \u00a7 70 WHG."
                    ),
                    form_fields=[
                        FormField(name="gewaesserquerungen", label="Watercourse Crossings (Name, Station, Crossing Method)", type="textarea"),
                        FormField(name="grundwasser", label="Groundwater Impact (Depth, Construction Dewatering)", type="textarea"),
                        FormField(name="schutzgebiete_wasser", label="Water Protection Areas (\u00a7 52 WHG) & Flood Zones (\u00a7 78 WHG)", type="textarea"),
                        FormField(name="hydrogeologie", label="Hydrogeological Survey (Results)", type="textarea"),
                        FormField(name="schutzmassnahmen_wasser", label="Water Protection Measures & Dewatering Concept", type="textarea"),
                        FormField(name="antrag_status_wasser", label="Application Status at Water Authority", type="textarea"),
                    ],
                    checklist=[
                        "Watercourse crossings identified and mapped",
                        "Hydrogeological survey prepared",
                        "Watercourse crossing plans prepared (1:5,000)",
                        "Flood zone compatibility assessed (\u00a7 78 WHG)",
                        "Water protection area compatibility assessed (\u00a7 52 WHG)",
                        "Construction dewatering concept prepared",
                        "Lower water authority opinion obtained",
                        "WSA permit for federal waterways applied (\u00a7 31 WaStrG)",
                        "Ecological construction supervision commissioned",
                    ],
                ),
                TaskTemplate(
                    id="s3_t5",
                    title="Conduct Heritage Protection Assessment",
                    description=(
                        "Assessment of heritage protection concerns pursuant to state heritage protection law (DSchG) "
                        "and the European Convention for the Protection of Archaeological Heritage (Valletta Convention 1992). "
                        "Concentration effect per \u00a7 24 NABEG. Polluter-pays principle: project developer bears "
                        "costs for prospection and rescue excavations."
                    ),
                    form_fields=[
                        FormField(name="bodendenkmale", label="Known Ground Monuments in Route Area (Heritage Registry)", type="textarea"),
                        FormField(name="baudenkmale", label="Built Monuments & Heritage Ensembles in Vicinity", type="textarea"),
                        FormField(name="prospektion", label="Archaeological Prospection (Field Walking, Magnetometry, GPR)", type="textarea"),
                        FormField(name="rettungsgrabung", label="Rescue Excavations (Results & Documentation)", type="textarea"),
                        FormField(name="trassenoptimierung", label="Route Adjustment for Monument Avoidance", type="textarea"),
                        FormField(name="auflagen_denkmal", label="Heritage Protection Requirements & Conditions", type="textarea"),
                    ],
                    checklist=[
                        "Heritage registries and ground monument maps cross-referenced",
                        "State heritage office contacted/opinion requested",
                        "Heritage protection technical report prepared",
                        "Field walking surveys conducted",
                        "Geomagnetic prospection conducted",
                        "Ground-penetrating radar survey conducted (if required)",
                        "Route optimization for monument avoidance assessed",
                        "Rescue excavations conducted (if required)",
                        "Archaeological construction supervision contractually arranged",
                        "Costs under polluter-pays principle recorded",
                    ],
                ),
                TaskTemplate(
                    id="s3_t6",
                    title="Prepare Immission Protection Certificate",
                    description=(
                        "Proof of compliance with limits pursuant to 26. BImSchV: "
                        "\u00a7 3 (limits for low-frequency systems: 5 kV/m E-field, 100 \u00b5T B-field at 50 Hz; "
                        "500 \u00b5T for DC systems), "
                        "\u00a7 4 (minimization requirement), "
                        "\u00a7 5 (calculation per DIN EN 50413), "
                        "\u00a7 7 (notification to immission control authority). "
                        "Additionally noise immission forecast per TA L\u00e4rm for corona noise."
                    ),
                    form_fields=[
                        FormField(name="leitungstyp", label="Line Type (AC/DC, Voltage, Overhead/Underground)", type="text"),
                        FormField(name="emf_berechnung", label="EMF Calculation per DIN EN 50413 (E-field kV/m, B-field \u00b5T)", type="textarea"),
                        FormField(name="immissionsorte", label="Sensitive Receptor Locations (Residences, Schools, Distances)", type="textarea"),
                        FormField(name="grenzwertvergleich", label="Limit Comparison (\u00a7 3(2): 100 \u00b5T at 50 Hz / 500 \u00b5T DC)", type="textarea"),
                        FormField(name="minimierung", label="Minimization Measures per \u00a7 4 (Phase Arrangement, Tower Type, Height)", type="textarea"),
                        FormField(name="schallprognose", label="Noise Immission Forecast (Corona Noise, dB(A) at Receptors)", type="textarea"),
                        FormField(name="anzeige_behoerde", label="Notification per \u00a7 7 to Immission Control Authority (Date, Status)", type="textarea"),
                    ],
                    checklist=[
                        "Sensitive receptor locations along route identified",
                        "EMF calculation per DIN EN 50413 conducted",
                        "Electric field strength < 5 kV/m at all receptor locations verified",
                        "Magnetic flux density < 100 \u00b5T (50 Hz) / < 500 \u00b5T (DC) verified",
                        "Minimization measures per \u00a7 4 documented",
                        "Overhead line route does not cross residential buildings (\u00a7 4(3))",
                        "Noise immission forecast prepared (TA L\u00e4rm)",
                        "Notification per \u00a7 7 submitted to immission control authority",
                        "Opinion from immission control authority obtained",
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
    # Evaluate stages within each section
    for section in project.sections:
        for stage in section.stages:
            all_done = all(t.status == TaskStatus.DONE for t in stage.tasks)
            any_started = any(t.status != TaskStatus.PENDING for t in stage.tasks)
            if all_done and len(stage.tasks) > 0:
                stage.status = StageStatus.COMPLETED
            elif any_started:
                stage.status = StageStatus.ACTIVE

    # Legacy: evaluate project-level stages too
    for stage in project.stages:
        all_done = all(t.status == TaskStatus.DONE for t in stage.tasks)
        any_started = any(t.status != TaskStatus.PENDING for t in stage.tasks)
        if all_done and len(stage.tasks) > 0:
            stage.status = StageStatus.COMPLETED
        elif any_started:
            stage.status = StageStatus.ACTIVE

    # Update current_stage_index
    for i, stage in enumerate(project.stages):
        if stage.status != StageStatus.COMPLETED:
            project.current_stage_index = i
            break
    else:
        project.current_stage_index = len(project.stages) - 1

    return project


def find_task_in_project(project: Project, task_id: str) -> tuple[str, int, int] | None:
    """Search all sections for a task. Returns (section_id, stage_index, task_index) or None."""
    for section in project.sections:
        for si, stage in enumerate(section.stages):
            for ti, task in enumerate(stage.tasks):
                if task.id == task_id:
                    return section.id, si, ti
    # Fallback: search project.stages directly (backward compat)
    for si, stage in enumerate(project.stages):
        for ti, task in enumerate(stage.tasks):
            if task.id == task_id:
                return "", si, ti
    return None


def get_task_template_id(project: Project, task_instance_id: str) -> str | None:
    for section in project.sections:
        for stage in section.stages:
            for task in stage.tasks:
                if task.id == task_instance_id:
                    return task.template_id
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
    # Section names
    "Bayern Nord": "Bavaria North",
    "Grenzbereich BY-HE": "Border Area BY-HE",
    "Hessen Süd": "Hesse South",
    # Permit labels
    "Naturschutzgenehmigung": "Nature Conservation Permit",
    "FFH-Verträglichkeitsprüfung": "FFH Compatibility Assessment",
    "Waldumwandlungsgenehmigung": "Forest Conversion Permit",
    "Waldausgleichsnachweis": "Forest Compensation Certificate",
    "Wasserrechtliche Erlaubnis": "Water Law Permit",
    "Gewässerquerungsgenehmigung": "Watercourse Crossing Permit",
    "Denkmalschutzrechtliche Genehmigung": "Heritage Protection Permit",
    "Kreuzungsvereinbarung DB": "Railway Crossing Agreement",
    "Kreuzungsvereinbarung BAB": "Highway Crossing Agreement",
    "Immissionsschutznachweis": "Immission Protection Certificate",
    "Denkmalschutzrechtliche Genehmigung (Bodendenkmal)": "Heritage Protection Permit (Ground Monument)",
    "Waldumwandlungsgenehmigung (Grenzbereich)": "Forest Conversion Permit (Border Area)",
    "Immissionsschutznachweis (Grenzbereich)": "Immission Protection Certificate (Border Area)",
    "Wasserrechtliche Erlaubnis (Hessen)": "Water Law Permit (Hesse)",
    "Denkmalschutzrechtliche Genehmigung (Hessen)": "Heritage Protection Permit (Hesse)",
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

    # Sections
    for section in p.sections:
        section.name = _t(section.name)

    # Permits
    for permit in p.permits:
        permit.label = _t(permit.label)

    return p
