import sqlite3

conn = sqlite3.connect("evenements_rhone.db")
cursor = conn.cursor()

# Vérifie si la colonne existe déjà
cursor.execute("PRAGMA table_info(evenement)")
colonnes = [col[1] for col in cursor.fetchall()]

if "date_normale" not in colonnes:
    cursor.execute("ALTER TABLE evenement ADD COLUMN date_normale TEXT")
    print("✅ Colonne 'date_normale' ajoutée avec succès.")
else:
    print("ℹ️ La colonne 'date_normale' existe déjà.")

conn.commit()
conn.close()
