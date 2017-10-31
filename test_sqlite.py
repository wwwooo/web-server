import sqlite3

conn = sqlite3.connect('contacts_db.sqlite')
c = conn.cursor()

with open("data.txt", "w") as file:
    for row in c.execute("SELECT * FROM contacts"):
        file.write(" ".join(row) + "\n")

conn.commit()
conn.close()