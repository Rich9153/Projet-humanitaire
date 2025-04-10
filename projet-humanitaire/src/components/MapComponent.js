import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function MapComponent({ coordinates }) {
  const defaultPosition = [46.603354, 1.888334]; // Centre de la France

  return (
    <MapContainer
      center={coordinates ? [coordinates.lat, coordinates.lng] : defaultPosition}
      zoom={coordinates ? 10 : 6}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {coordinates && (
        <Marker position={[coordinates.lat, coordinates.lng]}>
          <Popup>Commune trouvée</Popup>
        </Marker>
      )}
    </MapContainer>
  );
}
