import sqlite3
import os

class GestorSaludos:
    def __init__(self, db_name="saludos.db"):
        # Obtener el directorio actual del archivo Python
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        # Crear la ruta completa para la base de datos en la misma carpeta que el script
        db_path = os.path.join(ruta_actual, db_name)
        # Conectar a la base de datos o crearla si no existe
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        # Crear una tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS saludos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idioma TEXT NOT NULL,
                saludo TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def agregar_saludo(self, idioma, saludo):
        # Insertar un nuevo saludo en la base de datos
        self.cursor.execute('''
            INSERT INTO saludos (idioma, saludo)
            VALUES (?, ?)
        ''', (idioma, saludo))
        self.conn.commit()

    def obtener_saludos(self):
        # Obtener todos los saludos almacenados
        self.cursor.execute('SELECT * FROM saludos')
        return self.cursor.fetchall()

    def buscar_saludo_por_idioma(self, idioma):
        # Buscar saludos por idioma
        self.cursor.execute('SELECT * FROM saludos WHERE idioma = ?', (idioma,))
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        # Cerrar la conexión a la base de datos
        self.conn.close()

def mostrar_menu():
    print("\nGestor de Saludos Multilingües")
    print("1. Mostrar saludo por defecto")
    print("2. Personalizar saludo")
    print("3. Ver todos los saludos guardados")
    print("4. Buscar saludo por idioma")
    print("5. Salir")

def main():
    gestor = GestorSaludos()
    saludos_defecto = {
        "es": "Hola, mundo",
        "en": "Hello, world",
        "fr": "Bonjour, le monde",
        "de": "Hallo, Welt",
        "it": "Ciao, mondo"
    }

    while True:
        mostrar_menu()
        opcion = input("\nElige una opción (1-5): ")

        if opcion == "1":
            # Mostrar saludo por defecto en varios idiomas
            idioma = input("Elige un idioma (es, en, fr, de, it): ")
            print(saludos_defecto.get(idioma, "Idioma no soportado"))
        
        elif opcion == "2":
            # Personalizar un saludo y guardarlo en la base de datos
            idioma = input("Elige un idioma (es, en, fr, de, it): ")
            saludo_personalizado = input("Escribe tu saludo personalizado: ")
            gestor.agregar_saludo(idioma, saludo_personalizado)
            print("Saludo personalizado guardado correctamente.")
        
        elif opcion == "3":
            # Mostrar todos los saludos guardados
            saludos = gestor.obtener_saludos()
            if saludos:
                for saludo in saludos:
                    print(f"ID: {saludo[0]} | Idioma: {saludo[1]} | Saludo: {saludo[2]}")
            else:
                print("No hay saludos guardados.")
        
        elif opcion == "4":
            # Buscar saludos guardados por idioma
            idioma = input("Elige un idioma para buscar (es, en, fr, de, it): ")
            saludos = gestor.buscar_saludo_por_idioma(idioma)
            if saludos:
                for saludo in saludos:
                    print(f"ID: {saludo[0]} | Idioma: {saludo[1]} | Saludo: {saludo[2]}")
            else:
                print(f"No se encontraron saludos en {idioma}.")
        
        elif opcion == "5":
            # Salir del programa
            print("Saliendo del programa...")
            gestor.cerrar_conexion()
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
