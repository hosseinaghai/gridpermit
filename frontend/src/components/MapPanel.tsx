import "leaflet/dist/leaflet.css";
import { useEffect } from "react";
import {
  GeoJSON,
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import type { Project } from "../types";

// Fix default marker icons for Leaflet + bundlers
delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface Props {
  project: Project;
  showLayers?: {
    corridor?: boolean;
    ffh?: boolean;
    wald?: boolean;
    wsg?: boolean;
    parcels?: boolean;
    railway?: boolean;
    settlements?: boolean;
  };
}

// Mock GeoJSON data for the corridor route (BY/HE area ~50.1-50.9°N, 9.5-10.2°E)
const corridorB: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "Korridor B (Vorzugskorridor)", type: "corridor" },
      geometry: {
        type: "LineString",
        coordinates: [
          [9.68, 50.88],
          [9.72, 50.82],
          [9.78, 50.74],
          [9.82, 50.65],
          [9.88, 50.56],
          [9.93, 50.48],
          [9.98, 50.40],
          [10.03, 50.32],
          [10.08, 50.24],
          [10.12, 50.18],
        ],
      },
    },
  ],
};

const corridorA: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "Korridor A (Alternative)", type: "corridor_alt" },
      geometry: {
        type: "LineString",
        coordinates: [
          [9.68, 50.88],
          [9.60, 50.80],
          [9.55, 50.72],
          [9.52, 50.63],
          [9.55, 50.55],
          [9.60, 50.47],
          [9.68, 50.39],
          [9.78, 50.32],
          [9.90, 50.25],
          [10.12, 50.18],
        ],
      },
    },
  ],
};

const ffhArea: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "FFH-Gebiet 'Waldgebiet östlich Demo'", id: "GL-FFH-001" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [9.75, 50.70],
            [9.85, 50.70],
            [9.85, 50.76],
            [9.75, 50.76],
            [9.75, 50.70],
          ],
        ],
      },
    },
  ],
};

const waldArea: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "Waldgebiet (GL-WALD-014)", id: "GL-WALD-014" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [9.80, 50.58],
            [9.95, 50.58],
            [9.95, 50.66],
            [9.80, 50.66],
            [9.80, 50.58],
          ],
        ],
      },
    },
  ],
};

const wsgArea: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "Wasserschutzgebiet Zone III", id: "GL-WASSER-003" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [9.95, 50.36],
            [10.08, 50.36],
            [10.08, 50.42],
            [9.95, 50.42],
            [9.95, 50.36],
          ],
        ],
      },
    },
  ],
};

const railwayLine: GeoJSON.FeatureCollection = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { name: "DB-Strecke (Bündelung)", type: "railway" },
      geometry: {
        type: "LineString",
        coordinates: [
          [9.70, 50.88],
          [9.74, 50.80],
          [9.80, 50.72],
          [9.84, 50.63],
          [9.90, 50.54],
          [9.95, 50.46],
          [10.00, 50.38],
          [10.05, 50.30],
          [10.10, 50.22],
          [10.14, 50.18],
        ],
      },
    },
  ],
};

const parcels: { id: string; pos: [number, number]; label: string; owner: string }[] = [
  { id: "BY-091-223-17", pos: [50.62, 9.84], label: "Flurstück BY-091-223-17", owner: "Privat (nicht kontaktiert)" },
  { id: "HE-044-887-03", pos: [50.40, 10.00], label: "Flurstück HE-044-887-03", owner: "Kommune Demohausen" },
];

const settlements: { name: string; pos: [number, number]; distance: string }[] = [
  { name: "Musterstadt", pos: [50.75, 9.70], distance: "320 m" },
  { name: "Demohausen", pos: [50.42, 9.98], distance: "220 m (Erdkabel)" },
  { name: "Beispielhof", pos: [50.55, 9.90], distance: "580 m" },
];

// Fit map to corridor bounds
function FitBounds() {
  const map = useMap();
  useEffect(() => {
    const bounds = L.latLngBounds([
      [50.14, 9.45],
      [50.92, 10.20],
    ]);
    map.fitBounds(bounds, { padding: [20, 20] });
  }, [map]);
  return null;
}

const parcelIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const settlementIcon = new L.DivIcon({
  className: "",
  html: `<div style="background:#6366f1;color:white;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:bold;border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,.3)">S</div>`,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

export default function MapPanel({ showLayers = {} }: Props) {
  const {
    corridor = true,
    ffh = true,
    wald = true,
    wsg = true,
    parcels: showParcels = true,
    railway = true,
    settlements: showSettlements = true,
  } = showLayers;

  return (
    <div className="h-full w-full overflow-hidden rounded-lg border border-gray-200">
      <MapContainer
        center={[50.53, 9.85]}
        zoom={9}
        className="h-full w-full"
        style={{ minHeight: 200 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitBounds />

        {/* Corridor B (preferred) */}
        {corridor && (
          <GeoJSON
            data={corridorB}
            style={{ color: "#2563eb", weight: 4, opacity: 0.8, dashArray: "10 5" }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>72,8 km | Erdkabelanteil 35%`
              );
            }}
          />
        )}

        {/* Corridor A (alternative) */}
        {corridor && (
          <GeoJSON
            data={corridorA}
            style={{ color: "#9ca3af", weight: 2, opacity: 0.5, dashArray: "5 10" }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>76,3 km | überwiegend Freileitung`
              );
            }}
          />
        )}

        {/* FFH area */}
        {ffh && (
          <GeoJSON
            data={ffhArea}
            style={{ color: "#16a34a", fillColor: "#22c55e", fillOpacity: 0.2, weight: 2 }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>2,3 km Querung`
              );
            }}
          />
        )}

        {/* Wald */}
        {wald && (
          <GeoJSON
            data={waldArea}
            style={{ color: "#166534", fillColor: "#15803d", fillOpacity: 0.15, weight: 2, dashArray: "3 3" }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>8,7 km Waldquerung`
              );
            }}
          />
        )}

        {/* WSG */}
        {wsg && (
          <GeoJSON
            data={wsgArea}
            style={{ color: "#2563eb", fillColor: "#3b82f6", fillOpacity: 0.15, weight: 2, dashArray: "5 5" }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>1,1 km Randberührung`
              );
            }}
          />
        )}

        {/* Railway */}
        {railway && (
          <GeoJSON
            data={railwayLine}
            style={{ color: "#78716c", weight: 3, opacity: 0.6, dashArray: "2 6" }}
            onEachFeature={(feature, layer) => {
              layer.bindPopup(
                `<strong>${feature.properties?.name}</strong><br/>Bündelungspotenzial mit Trassenführung`
              );
            }}
          />
        )}

        {/* Parcels */}
        {showParcels &&
          parcels.map((p) => (
            <Marker key={p.id} position={p.pos} icon={parcelIcon}>
              <Popup>
                <strong>{p.label}</strong>
                <br />
                Eigentümer: {p.owner}
              </Popup>
            </Marker>
          ))}

        {/* Settlements */}
        {showSettlements &&
          settlements.map((s) => (
            <Marker key={s.name} position={s.pos} icon={settlementIcon}>
              <Popup>
                <strong>{s.name}</strong>
                <br />
                Siedlungsabstand: {s.distance}
              </Popup>
            </Marker>
          ))}
      </MapContainer>
    </div>
  );
}
