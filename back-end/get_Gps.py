import sqlite3
import requests

# Connexion à la base de données SQLite
conn = sqlite3.connect('evenements_rhone.db')
cursor = conn.cursor()

# Récupérer toutes les communes
cursor.execute("SELECT id_commune, nom_commune FROM commune")
communes = cursor.fetchall()

# Fonction pour récupérer les coordonnées GPS à partir de l'API Geo
def get_gps_coordinates(commune_name):
    # URL de l'API de l'État français (Geo)
    url = f"https://api-adresse.data.gouv.fr/search/?q={commune_name}&limit=1"
    
    # Envoi de la requête GET
    response = requests.get(url)
    # On s'assure que la réponse est bien en JSON
    if response.status_code == 200:
        data = response.json()
        
        # Si des données sont renvoyées, on extrait les coordonnées
        if data['features']:
            lat = data['features'][0]['geometry']['coordinates'][1]  # Latitude
            lon = data['features'][0]['geometry']['coordinates'][0]  # Longitude
            return lat, lon
    return None, None

# Mise à jour des coordonnées pour chaque commune
for commune in communes:
    id_commune, nom_commune = commune
    latitude, longitude = get_gps_coordinates(nom_commune)

    if latitude and longitude:
        cursor.execute("""
            UPDATE commune
            SET latitude = ?, longitude = ?
            WHERE id_commune = ?
        """, (latitude, longitude, id_commune))

# Sauvegarder les modifications dans la base de données
conn.commit()
conn.close()

print("Coordonnées GPS mises à jour pour chaque commune.")
