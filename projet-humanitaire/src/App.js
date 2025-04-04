import React, { useState } from 'react';
import './App.css';
import Recherche from './components/Recherche';
import Carte from './components/Carte';

export default function App() {
  const [donneerecherche, setDonneerecherche] = useState(null);
  const [coordinates, setCoordinates] = useState([48.8566, 2.3522]); // Paris par défaut

  // Simuler une API qui retourne des coordonnées pour une commune donnée
  const fetchCoordinates = async (commune) => {
    const fakeDatabase = {
      "Paris": [48.8566, 2.3522],
      "Marseille": [43.2965, 5.3698],
      "Lyon": [45.764, 4.8357],
    };

    return fakeDatabase[commune] || null; // Retourne null si la commune n'existe pas
  };

  const handlesearch = async (data) => {
    console.log("Données reçues : ", data);
    setDonneerecherche(data);

    // Simuler un appel à une API pour récupérer les coordonnées
    const fetchedCoordinates = await fetchCoordinates(data.search);
    if (fetchedCoordinates) {
      setCoordinates(fetchedCoordinates); // Met à jour les coordonnées de la carte
    } else {
      console.log("Commune non trouvée.");
      setCoordinates([48.8566, 2.3522]); // Si aucune coordonnée n'est trouvée, afficher Paris par défaut
    }
  };

  return (
    <div className="App">
      <h1>Carte interactive</h1>
      <Recherche onSearch={handlesearch} />
      <Carte coordinates={coordinates} />
    </div>
  );
}
