import React, { useState } from "react";

export default function Recherche({ onSearch }) {
  const [search, setSearch] = useState("");
  const [year, setYear] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(search, year);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <div>
        <label className="block">Nom de la commune :</label>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border rounded p-2 w-full"
        />
      </div>
      <div>
        <label className="block">Année :</label>
        <input
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          className="border rounded p-2 w-full"
        />
      </div>
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Rechercher
      </button>
    </form>
  );
}
