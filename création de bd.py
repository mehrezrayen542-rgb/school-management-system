import sqlite3

con = sqlite3.connect("school.db")
cur = con.cursor()

# lire le SQL depuis le fichier
with open("school.sql", "r") as f:
    sql = f.read()

# exécuter toutes les commandes
cur.executescript(sql)

con.commit()
con.close()

print("SQLite DB created successfully!")
