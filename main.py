import serial
import threading
import customtkinter as ctk
import serial.tools.list_ports_windows
import time
import random


class MicrobitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Autiste 3000 | Logiciel ")
        self.root.geometry("600x450")
        
        # Amélioration de l'apparence
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Titre
        self.title_label = ctk.CTkLabel(root, text="Autiste 3000 | Logiciel", font=("Arial", 18), pady=20)
        self.title_label.pack()

        # Boîte de texte pour afficher les messages
        self.textbox = ctk.CTkTextbox(root, width=550, height=250, wrap="word", state="disabled")
        self.textbox.pack(pady=10)

        # Entrée pour les messages
        self.entry = ctk.CTkEntry(root, width=400, placeholder_text="Entrez un message", corner_radius=10)
        self.entry.pack(pady=5)
        
        # Bouton d'envoi
        self.send_button = ctk.CTkButton(root, text="Envoyer", command=self.send_message, width=200, height=40, corner_radius=10)
        self.send_button.pack(pady=10)
        
        # Connecter au port série
        self.serial_port = None
        self.start_serial()

    def detect_microbit(self):
        ports = serial.tools.list_ports_windows.comports()
        for port in ports:
            if "Microbit" in port.description or "mbed" in port.description:
                return port.device
        return None
    
    def start_serial(self):
        port = self.detect_microbit()
        if not port:
            port = ctk.CTkInputDialog(text="Aucune Micro:bit détectée. Entrez le port manuellement:", title="Port Série").get_input()
        
        baudrate = 115200
        
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.textbox.configure(state="normal")
            self.textbox.insert("end", "Connexion établie!\n")
            self.textbox.configure(state="disabled")
            threading.Thread(target=self.read_serial, daemon=True).start()
        except Exception as e:
            self.textbox.configure(state="normal")
            self.textbox.insert("end", f"Erreur: {e}\n")
            self.textbox.configure(state="disabled")
    
    def read_serial(self):
        while True:
            try:
                if self.serial_port:  # Mode réel
                    data = self.serial_port.readline().decode('utf-8').strip()
                else:  # Mode simulation
                    data = f"Simulé: Temp={random.randint(20, 30)}°C"
                    time.sleep(2)

                if data:
                    self.textbox.configure(state="normal")
                    self.textbox.insert("end", f"Reçu: {data}\n")
                    self.textbox.see("end")
                    self.textbox.configure(state="disabled")
            except Exception as e:
                self.textbox.configure(state="normal")
                self.textbox.insert("end", f"Erreur de lecture: {e}\n")
                self.textbox.configure(state="disabled")
                break
    
    def send_message(self):
        message = self.entry.get()
        if self.serial_port and message:
            self.serial_port.write((message + '\n').encode('utf-8'))
            self.textbox.configure(state="normal")
            self.textbox.insert("end", f"Envoyé: {message}\n")
            self.textbox.see("end")
            self.textbox.configure(state="disabled")
            self.entry.delete(0, "end")


if __name__ == "__main__":
    root = ctk.CTk()
    app = MicrobitGUI(root)
    root.mainloop()
