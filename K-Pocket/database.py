import sqlite3
import random

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("photocards.db")
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        """Crea las tablas iniciales si no existen."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS photocards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo TEXT,
            idol TEXT,
            album TEXT,
            version TEXT,
            año INTEGER,
            rareza TEXT,
            imagen TEXT
        )''')
        self.conn.commit()
        # Insertar photocards de ejemplo
        self.populate_photocards()

    def populate_photocards(self):
        """Inserta photocards iniciales si no existen."""
        photocards = [
            ("Twice", "Chaeyoung", "Ready to Be", "Ver.1", 2023, "Común", "assets/images/chaeyoung.jpg"),
            ("Kep1er", "Yeseo", "Troubleshooter", "Daydream Ver.1", 2022, "Rara", "assets/images/yeseo.jpg"),
            ("G-Idle", "Yuqi", "I Never Die", "Chill Ver.", 2022, "Legendaria", "assets/images/yuqi.jpg"),
            ("Itzy", "Yuna", "Icy", "Ver.3", 2019, "Común", "assets/images/yuna.jpg"),
            ("StayC", "Seeun", "Poppy", "Limited Ver.1", 2022, "Épica", "assets/images/seeun.jpg"),
        ]
        try:
            for grupo, idol, album, version, año, rareza, imagen in photocards:  # Ajusta a 7 columnas
                self.cursor.execute('''
                INSERT OR IGNORE INTO photocards (grupo, idol, album, version, año, rareza, imagen)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (grupo, idol, album, version, año, rareza, imagen))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al insertar photocards: {e}")

    def generate_pack(self):
        """Genera un paquete de 5 photocards basado en rarezas."""
        RAREZA_PROBABILIDADES = {"Común": 0.6, "Rara": 0.25, "Épica": 0.1, "Legendaria": 0.05}

        paquete = []
        usados = set()
        while len(paquete) < 5:
            rareza = random.choices(
                list(RAREZA_PROBABILIDADES.keys()),
                weights=RAREZA_PROBABILIDADES.values(),
                k=1
            )[0]
            self.cursor.execute('''
            SELECT id, grupo, idol, album, version, año, rareza, imagen 
            FROM photocards 
            WHERE rareza = ?''', (rareza,))
            opciones = [opc for opc in self.cursor.fetchall() if opc[0] not in usados]
            if opciones:
                seleccion = random.choice(opciones)
                paquete.append(seleccion)
                usados.add(seleccion[0])
        return paquete


    def close(self):
        """Cierra la conexión con la base de datos."""
        self.conn.close()


# Uso de la clase
if __name__ == "__main__":
    db = Database()
    print("Generando paquete de prueba...")
    paquete = db.generate_pack()
    if isinstance(paquete, str):  # Si devuelve un mensaje de error
        print(paquete)
    else:
        for card in paquete:
            print(f"Grupo: {card[1]}, Idol: {card[2]}, Álbum: {card[3]}, Versión: {card[4]}, Año: {card[5]}, Rareza: {card[6]}")
    db.close()
