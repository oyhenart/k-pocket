import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from database import Database

# Conexión con la base de datos
conn = sqlite3.connect("photocards.db")
conn = conn.cursor()
db = Database()

class LoginScreen(Screen):
    """Pantalla inicial para navegar hacia la apertura de paquetes."""
    pass

class ClickableImage(ButtonBehavior, Image):
    """Combina ButtonBehavior con Image para hacerla clickeable."""
    pass

class OpenPackScreen(Screen):
    pack_message = StringProperty("¡Haz clic en el paquete para abrirlo!")

    def open_pack(self):
        """Genera un paquete y muestra las photocards."""
        self.pack_message = "Abriendo paquete..."
        paquete = db.generate_pack()  # Obtener photocards de la base de datos
        grid = self.ids.pack_grid
        grid.clear_widgets()  # Limpia widgets existentes

        # Agregar imágenes de photocards al grid
        for card in paquete:
            if len(card) > 7:  # Asegurarse de que la columna imagen existe
                grid.add_widget(Image(source=card[7]))
            else:
                print(f"Error: La photocard {card} no tiene una imagen asociada.")
        self.pack_message = "¡Paquete abierto con éxito!"



class PhotocardApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(OpenPackScreen(name="open_pack"))
        return sm

if __name__ == "__main__":
    PhotocardApp().run()
