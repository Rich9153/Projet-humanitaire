import React, { useState } from "react";
import Recherche from "./components/Recherche";
import MapComponent from "./components/MapComponent";
import Timeline from "./components/Timeline";

export default function App() {
  const [searchResult, setSearchResult] = useState(null);
  const [coordinates, setCoordinates] = useState(null);

  const handleSearch = async (search, year) => {
    try {
      const response = await fetch(
        `http://localhost:5000/recherche?nom=${search}&annee=${year}`
      );
      const data = await response.json();
      setSearchResult(data);
  
      if (data && data.latitude && data.longitude) {
        setCoordinates({ lat: data.latitude, lng: data.longitude });
      }
    } catch (error) {
      console.error("Erreur lors de la requête API:", error);
    }
  };
  

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">Projet Humanitaire : Recherche de commune</h1>
      <Recherche onSearch={handleSearch} />
      <MapComponent coordinates={coordinates} />
      {searchResult && <Timeline history={searchResult.historique} />}
    </div>
  );
}
