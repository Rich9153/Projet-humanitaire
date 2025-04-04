import React, { useState } from "react";

const Recherche = ({ onSearch }) => {
  const [search, setSearch] = useState("");
  const [year, setYear] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ search, year }); // Transmettre les données au parent (ex: App.js)
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <div>
        <label>Recherche :</label>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Entrez un lieu..."
        />
      </div>
      <div>
        <label>Année :</label>
        <input
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          placeholder="Ex: 2024"
        />
      </div>
      <button type="submit">Rechercher</button>
    </form>
  );
};

export default Recherche;
