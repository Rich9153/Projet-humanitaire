from flask import Flask, jsonify, request, Response
import sqlite3
import json

app = Flask(__name__)

# Connexion à la base
def get_db_connection():
    conn = sqlite3.connect("evenements_rhone.db")
    conn.row_factory = sqlite3.Row
    return conn

# Route pour afficher toutes les communes
@app.route('/communes')
def get_communes():
    conn = get_db_connection()
    communes = conn.execute("SELECT * FROM commune").fetchall()
    conn.close()

    resultats = []
    for commune in communes:
        resultats.append({
            "id_commune": commune["id_commune"],
            "nom_commune": commune["nom_commune"],
            "latitude": commune["latitude"],
            "longitude": commune["longitude"]
        })

    return jsonify(resultats)

# Route avec filtres date pour les événements d'une commune
@app.route("/evenements/<int:id_commune>")
def get_evenements_par_commune(id_commune):
    avant = request.args.get("avant")
    apres = request.args.get("apres")
    exact = request.args.get("date")

    query = """
    SELECT e.id_evenement, e.type_evenement, e.date, e.date_normale, e.source,
           e.commentaire, l.role, c.nom_commune
    FROM evenement e
    JOIN lien_commune_evenement l ON e.id_evenement = l.id_evenement
    JOIN commune c ON l.id_commune = c.id_commune
    WHERE l.id_commune = ?
    """
    params = [id_commune]

    if exact:
        query += " AND e.date_normale = ?"
        params.append(exact)
    else:
        if avant:
            query += " AND e.date_normale < ?"
            params.append(avant)
        if apres:
            query += " AND e.date_normale > ?"
            params.append(apres)

    query += " ORDER BY e.date_normale"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id_evenement": row["id_evenement"],
            "type": row["type_evenement"],
            "date_originale": row["date"],
            "date_normale": row["date_normale"],
            "source": row["source"],
            "commentaire": row["commentaire"],
            "role": row["role"],
            "nom_commune": row["nom_commune"]
        })

    response_json = json.dumps(result, ensure_ascii=False, indent=2)
    return Response(response_json, content_type="application/json; charset=utf-8")

# Route recherche intelligente : par nom et/ou année
@app.route("/recherche")
def rechercher_evenements():
    nom = request.args.get("nom")
    annee = request.args.get("annee")

    if not nom:
        erreur = {"erreur": "Le paramètre 'nom' est requis."}
        response_json = json.dumps(erreur, ensure_ascii=False, indent=2)
        return Response(response_json, content_type="application/json; charset=utf-8"), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifie si la commune existe
    cursor.execute("SELECT id_commune, latitude, longitude FROM commune WHERE lower(nom_commune) = lower(?)", (nom,))
    commune = cursor.fetchone()

    if not commune:
        conn.close()
        return jsonify({"erreur": f"La commune '{nom}' n'existe pas dans la base."}), 404

    id_commune = commune["id_commune"]
    latitude = commune["latitude"]
    longitude = commune["longitude"]

    # Requête événements
    query = """
    SELECT e.id_evenement, e.type_evenement, e.date, e.date_normale, e.source,
           e.commentaire, l.role, c.nom_commune
    FROM evenement e
    JOIN lien_commune_evenement l ON e.id_evenement = l.id_evenement
    JOIN commune c ON l.id_commune = c.id_commune
    WHERE l.id_commune = ?
    """
    params = [id_commune]

    if annee:
        query += " AND strftime('%Y', e.date_normale) = ?"
        params.append(str(annee))

    query += " ORDER BY e.date_normale"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        result = {
            "message": f"Aucun événement trouvé pour '{nom}' en {annee if annee else 'toute année'}",
            "nom_commune": nom,
            "latitude": latitude,
            "longitude": longitude
        }
        response_json = json.dumps(result, ensure_ascii=False, indent=2)
        return Response(response_json, content_type="application/json; charset=utf-8")

    result = []
    for row in rows:
        result.append({
            "id_evenement": row["id_evenement"],
            "type": row["type_evenement"],
            "date_originale": row["date"],
            "date_normale": row["date_normale"],
            "source": row["source"],
            "commentaire": row["commentaire"],
            "role": row["role"],
            "nom_commune": row["nom_commune"],
            "latitude": latitude,
            "longitude": longitude
        })

    return Response(json.dumps(result, ensure_ascii=False, indent=2), content_type="application/json; charset=utf-8")

# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True)
