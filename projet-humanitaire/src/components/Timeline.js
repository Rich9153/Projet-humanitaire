import React from "react";

export default function Timeline({ history }) {
  if (!history || history.length === 0) return <p>Aucune donnée historique disponible.</p>;

  return (
    <div className="border-l-4 border-blue-500 pl-4 space-y-4">
      <h2 className="text-xl font-semibold mb-2">Historique</h2>
      {history.map((event, index) => (
        <div key={index} className="relative">
          <div className="absolute w-3 h-3 bg-blue-500 rounded-full -left-5 top-1.5"></div>
          <p><strong>{event.date}</strong> : {event.description}</p>
        </div>
      ))}
    </div>
  );
}
