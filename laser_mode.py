"""
Mode laser épuré sans distractions - Interface professionnelle
"""
import tkinter as tk
import cv2
import numpy as np
from threading import Thread
import time
import pyautogui

class LaserPointer:
    """Pointeur laser professionnel sans distractions"""
    
    def __init__(self, config):
        self.config = config
        self.is_active = False
        self.laser_window = None
        self.laser_x = 0
        self.laser_y = 0
        self.trail_points = []
        self.current_color = "#FF0000"  # Rouge par défaut
        self.pointer_size = "normal"  # normal, large, small
        self.is_drawing = False  # Mode dessin temporaire
        self.draw_points = []  # Points pour le mode dessin
        self.show_instructions = True  # Affichage des instructions (toggle)
        
        # Couleurs disponibles
        self.colors = [
            "#FF0000",  # Rouge
            "#00FF00",  # Vert  
            "#0000FF",  # Bleu
            "#FFFF00",  # Jaune
            "#FF00FF",  # Magenta
            "#00FFFF",  # Cyan
            "#FFFFFF"   # Blanc
        ]
        
        # Tailles de pointeur
        self.sizes = {
            "small": 8,
            "normal": 15,
            "large": 25
        }
        
    def activate(self):
        """Active le mode laser plein écran"""
        if not self.is_active:
            self.is_active = True
            self.create_laser_window()
            
    def deactivate(self):
        """Désactive le mode laser"""
        if self.is_active:
            self.is_active = False
            self.is_drawing = False
            self.draw_points = []
            if self.laser_window:
                self.laser_window.destroy()
                self.laser_window = None
                
    def create_laser_window(self):
        """Crée la fenêtre laser transparente et épurée"""
        self.laser_window = tk.Toplevel()
        
        # Configuration plein écran
        self.laser_window.attributes('-fullscreen', True)
        self.laser_window.attributes('-topmost', True)
        self.laser_window.attributes('-alpha', 0.9)
        self.laser_window.configure(bg='black')
        
        # Rendre la fenêtre transparente aux clics
        try:
            self.laser_window.wm_attributes('-transparentcolor', 'black')
        except:
            pass
        
        # Canvas pour dessiner le laser
        self.laser_canvas = tk.Canvas(
            self.laser_window,
            bg='black',
            highlightthickness=0,
            width=self.laser_window.winfo_screenwidth(),
            height=self.laser_window.winfo_screenheight()
        )
        self.laser_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Instructions minimalistes (masquables)
        self.create_minimal_instructions()
        
        # Raccourcis clavier
        self.laser_window.bind('<Escape>', lambda e: self.deactivate())
        self.laser_window.bind('<c>', lambda e: self.change_color())
        self.laser_window.bind('<s>', lambda e: self.change_size())
        self.laser_window.bind('<d>', lambda e: self.toggle_drawing())
        self.laser_window.bind('<x>', lambda e: self.clear_drawings())
        self.laser_window.bind('<h>', lambda e: self.toggle_instructions())  # Toggle help
        self.laser_window.bind('<i>', lambda e: self.toggle_instructions())  # Toggle instructions
        self.laser_window.focus_set()
        
        # Démarrer l'animation
        self.animate_laser()
        
        # Auto-masquer les instructions après 3 secondes
        self.laser_window.after(3000, self.auto_hide_instructions)
        
    def create_minimal_instructions(self):
        """Instructions minimalistes et discrètes"""
        self.instructions_frame = tk.Frame(self.laser_window, bg='#000020')
        self.instructions_frame.place(x=10, y=10)
        
        # Titre discret
        self.title_label = tk.Label(
            self.instructions_frame,
            text="🔴 POINTEUR LASER",
            fg="#ffffff",
            bg="#000020",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=5
        )
        self.title_label.pack()
        
        # Statut compact
        self.status_frame = tk.Frame(self.instructions_frame, bg="#001122")
        self.status_frame.pack(fill=tk.X)
        
        self.color_info = tk.Label(
            self.status_frame,
            text="Rouge",
            fg="white",
            bg="#001122",
            font=("Arial", 9),
            padx=10,
            pady=3
        )
        self.color_info.pack(side=tk.LEFT)
        
        self.size_info = tk.Label(
            self.status_frame,
            text="Normal",
            fg="white",
            bg="#001122", 
            font=("Arial", 9),
            padx=10,
            pady=3
        )
        self.size_info.pack(side=tk.LEFT)
        
        # Note discrète
        self.help_note = tk.Label(
            self.instructions_frame,
            text="H = Aide",
            fg="#666666",
            bg="#000020",
            font=("Arial", 8),
            padx=10,
            pady=2
        )
        self.help_note.pack()
        
    def toggle_instructions(self):
        """Affiche/masque les instructions"""
        self.show_instructions = not self.show_instructions
        if self.show_instructions:
            self.instructions_frame.place(x=10, y=10)
        else:
            self.instructions_frame.place_forget()
            
    def auto_hide_instructions(self):
        """Masque automatiquement les instructions après 3 secondes"""
        if self.show_instructions:
            self.show_instructions = False
            self.instructions_frame.place_forget()
        
    def change_color(self):
        """Change la couleur du laser"""
        current_index = self.colors.index(self.current_color) if self.current_color in self.colors else 0
        self.current_color = self.colors[(current_index + 1) % len(self.colors)]
        
        # Mettre à jour l'affichage
        color_names = {
            "#FF0000": "Rouge", "#00FF00": "Vert", "#0000FF": "Bleu",
            "#FFFF00": "Jaune", "#FF00FF": "Magenta", "#00FFFF": "Cyan", "#FFFFFF": "Blanc"
        }
        color_name = color_names.get(self.current_color, "Rouge")
        if hasattr(self, 'color_info'):
            self.color_info.config(text=color_name)
            
        # Affichage temporaire de la couleur
        self.show_color_feedback()
            
    def change_size(self):
        """Change la taille du pointeur"""
        sizes = ["small", "normal", "large"]
        current_index = sizes.index(self.pointer_size) if self.pointer_size in sizes else 1
        self.pointer_size = sizes[(current_index + 1) % len(sizes)]
        
        # Mettre à jour l'affichage
        size_names = {"small": "Petit", "normal": "Normal", "large": "Grand"}
        size_name = size_names.get(self.pointer_size, "Normal")
        if hasattr(self, 'size_info'):
            self.size_info.config(text=size_name)
            
        # Affichage temporaire de la taille
        self.show_size_feedback()
            
    def toggle_drawing(self):
        """Active/désactive le mode dessin"""
        self.is_drawing = not self.is_drawing
        # Feedback visuel temporaire sans texte permanent
        self.show_mode_feedback()
                
    def clear_drawings(self):
        """Efface tous les dessins"""
        self.draw_points = []
        self.is_drawing = False
        # Feedback visuel temporaire
        self.show_clear_feedback()
        
    def show_color_feedback(self):
        """Affichage temporaire du changement de couleur"""
        if hasattr(self, 'laser_canvas'):
            # Créer un indicateur temporaire
            color_names = {
                "#FF0000": "Rouge", "#00FF00": "Vert", "#0000FF": "Bleu",
                "#FFFF00": "Jaune", "#FF00FF": "Magenta", "#00FFFF": "Cyan", "#FFFFFF": "Blanc"
            }
            color_name = color_names.get(self.current_color, "Rouge")
            
            feedback_id = self.laser_canvas.create_text(
                self.laser_canvas.winfo_reqwidth() // 2,
                50,
                text=f"🎨 {color_name}",
                fill=self.current_color,
                font=("Arial", 16, "bold"),
                tags="feedback"
            )
            
            # Supprimer après 1.5 secondes
            self.laser_window.after(1500, lambda: self.laser_canvas.delete("feedback"))
            
    def show_size_feedback(self):
        """Affichage temporaire du changement de taille"""
        if hasattr(self, 'laser_canvas'):
            size_names = {"small": "Petit", "normal": "Normal", "large": "Grand"}
            size_name = size_names.get(self.pointer_size, "Normal")
            
            feedback_id = self.laser_canvas.create_text(
                self.laser_canvas.winfo_reqwidth() // 2,
                100,
                text=f"📏 {size_name}",
                fill="white",
                font=("Arial", 16, "bold"),
                tags="feedback"
            )
            
            # Supprimer après 1.5 secondes
            self.laser_window.after(1500, lambda: self.laser_canvas.delete("feedback"))
            
    def show_mode_feedback(self):
        """Affichage temporaire du changement de mode"""
        if hasattr(self, 'laser_canvas'):
            mode_text = "Mode Dessin" if self.is_drawing else "Mode Pointage"
            
            feedback_id = self.laser_canvas.create_text(
                self.laser_canvas.winfo_reqwidth() // 2,
                150,
                text=f"✏️ {mode_text}",
                fill="#FFD700",
                font=("Arial", 16, "bold"),
                tags="feedback"
            )
            
            # Supprimer après 1.5 secondes
            self.laser_window.after(1500, lambda: self.laser_canvas.delete("feedback"))
            
    def show_clear_feedback(self):
        """Affichage temporaire de l'effacement"""
        if hasattr(self, 'laser_canvas'):
            feedback_id = self.laser_canvas.create_text(
                self.laser_canvas.winfo_reqwidth() // 2,
                200,
                text="🧹 Dessins effacés",
                fill="#00FF00",
                font=("Arial", 16, "bold"),
                tags="feedback"
            )
            
            # Supprimer après 1.5 secondes
            self.laser_window.after(1500, lambda: self.laser_canvas.delete("feedback"))
        
    def update_position(self, x, y):
        """Met à jour la position du laser"""
        if self.is_active and self.laser_canvas:
            # Convertir les coordonnées de la caméra vers l'écran
            screen_width = self.laser_window.winfo_screenwidth()
            screen_height = self.laser_window.winfo_screenheight()
            
            # Inversion horizontale pour un contrôle naturel
            screen_x = screen_width - int(x * screen_width)
            screen_y = int(y * screen_height)
            
            self.laser_x = screen_x
            self.laser_y = screen_y
            
            # Gestion du mode dessin
            if self.is_drawing:
                self.draw_points.append((screen_x, screen_y, time.time()))
                # Limiter le nombre de points de dessin
                if len(self.draw_points) > 2000:
                    self.draw_points = self.draw_points[-1000:]
            else:
                # Ajouter à la traînée normale
                self.trail_points.append((screen_x, screen_y, time.time()))
                
                # Nettoyer les anciens points de traînée
                current_time = time.time()
                self.trail_points = [(x, y, t) for x, y, t in self.trail_points 
                                   if current_time - t < 1.2]
            
    def animate_laser(self):
        """Animation continue du laser"""
        if self.is_active and self.laser_canvas:
            self.draw_laser()
            self.laser_window.after(20, self.animate_laser)  # 50 FPS pour fluidité
        
    def draw_laser(self):
        """Dessine le pointeur laser épuré"""
        if not (self.is_active and self.laser_canvas):
            return
            
        self.laser_canvas.delete("laser")
        
        # Dessiner les dessins permanents
        self.draw_permanent_drawings()
        
        # Dessiner la traînée ou le dessin en cours
        if self.is_drawing:
            self.draw_current_drawing()
        else:
            self.draw_trail()
        
        # Pointeur principal
        self.draw_main_pointer()
        
    def draw_permanent_drawings(self):
        """Dessine les dessins permanents"""
        if not self.draw_points:
            return
            
        # Grouper les points par proximité temporelle pour créer des lignes
        for i in range(1, len(self.draw_points)):
            x1, y1, t1 = self.draw_points[i-1]
            x2, y2, t2 = self.draw_points[i]
            
            # Si les points sont proches dans le temps, les connecter
            if t2 - t1 < 0.15:  # 150ms
                try:
                    self.laser_canvas.create_line(
                        x1, y1, x2, y2,
                        fill=self.current_color, width=4, tags="laser"
                    )
                except:
                    pass
                    
    def draw_current_drawing(self):
        """Dessine le trait en cours de création"""
        if len(self.trail_points) > 1:
            for i in range(1, len(self.trail_points)):
                x1, y1, t1 = self.trail_points[i-1]
                x2, y2, t2 = self.trail_points[i]
                
                try:
                    self.laser_canvas.create_line(
                        x1, y1, x2, y2,
                        fill=self.current_color, width=5, tags="laser"
                    )
                except:
                    pass
                    
    def draw_trail(self):
        """Dessine la traînée normale du pointeur"""
        current_time = time.time()
        
        for i, (x, y, t) in enumerate(self.trail_points):
            age = current_time - t
            alpha = max(0, 1 - (age / 1.2))
            size = int(3 + alpha * 8)
            
            try:
                self.laser_canvas.create_oval(
                    x - size//2, y - size//2,
                    x + size//2, y + size//2,
                    fill=self.current_color, outline="", tags="laser"
                )
            except:
                pass
                
    def draw_main_pointer(self):
        """Dessine le pointeur principal épuré"""
        if not (hasattr(self, 'laser_x') and hasattr(self, 'laser_y')):
            return
            
        radius = self.sizes[self.pointer_size]
        
        # Effet de pulsation subtil
        pulse_factor = (1 + 0.2 * abs(np.sin(time.time() * 4)))
        pulse_size = int(radius * pulse_factor)
        
        try:
            # Halo externe subtil
            self.laser_canvas.create_oval(
                self.laser_x - pulse_size * 2, self.laser_y - pulse_size * 2,
                self.laser_x + pulse_size * 2, self.laser_y + pulse_size * 2,
                outline=self.current_color, width=1, tags="laser"
            )
            
            # Cercle principal
            self.laser_canvas.create_oval(
                self.laser_x - pulse_size, self.laser_y - pulse_size,
                self.laser_x + pulse_size, self.laser_y + pulse_size,
                fill=self.current_color, outline="#FFFFFF", width=2, tags="laser"
            )
            
            # Point central brillant
            center_size = max(3, pulse_size // 2)
            self.laser_canvas.create_oval(
                self.laser_x - center_size, self.laser_y - center_size,
                self.laser_x + center_size, self.laser_y + center_size,
                fill="#FFFFFF", outline="", tags="laser"
            )
            
            # Indicateur de mode dessin minimal (seulement si actif)
            if self.is_drawing:
                # Petit indicateur discret
                self.laser_canvas.create_oval(
                    self.laser_x + pulse_size * 2, self.laser_y - pulse_size * 2,
                    self.laser_x + pulse_size * 2 + 8, self.laser_y - pulse_size * 2 + 8,
                    fill="#FFD700", outline="", tags="laser"
                )
        except:
            pass

class SimplePresentationController:
    """Contrôleur de présentation simplifié - Navigation uniquement"""
    
    def __init__(self):
        # Désactiver le fail-safe de pyautogui
        pyautogui.FAILSAFE = False
        self.last_gesture_time = 0
        
    def execute_gesture_action(self, gesture: str, cooldown: float = 1.0):
        """Actions de navigation uniquement - simplifiées"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < cooldown:
            return
        
        # Actions de navigation simplifiées
        action_map = {
            "fist": self.next_slide,
            "open_hand": self.previous_slide,
            "ok": self.toggle_fullscreen,
        }
        
        if gesture in action_map:
            action_map[gesture]()
            self.last_gesture_time = current_time
            print(f"Action de navigation: {gesture}")
    
    def next_slide(self):
        """Slide suivante"""
        pyautogui.press('right')
        print("→ Slide suivante")
    
    def previous_slide(self):
        """Slide précédente"""
        pyautogui.press('left')
        print("← Slide précédente")
    
    def toggle_fullscreen(self):
        """Basculer plein écran / démarrer diaporama"""
        pyautogui.press('f5')
        print("🖥️ Basculer plein écran")

class DualModeController:
    """Contrôleur dual épuré avec interface professionnelle"""
    
    def __init__(self):
        from config import GestureConfig
        
        # Deux contrôleurs séparés
        self.laser_pointer = LaserPointer(GestureConfig())
        self.presentation_controller = SimplePresentationController()
        
        # État actuel
        self.current_mode = "navigation"  # "navigation" ou "laser"
        
    def toggle_mode(self):
        """Basculer entre navigation et laser"""
        if self.current_mode == "navigation":
            self.current_mode = "laser"
            self.laser_pointer.activate()
            print("🔴 MODE POINTEUR LASER - Interface épurée")
        else:
            self.current_mode = "navigation"
            self.laser_pointer.deactivate()
            print("🎯 MODE NAVIGATION")
            
    def update_laser_position(self, normalized_x, normalized_y):
        """Met à jour la position du laser (mode laser uniquement)"""
        if self.current_mode == "laser":
            self.laser_pointer.update_position(normalized_x, normalized_y)
            
    def execute_gesture_action(self, gesture: str, cooldown: float = 1.0):
        """Exécution des gestes selon le mode actuel"""
        
        if self.current_mode == "navigation":
            # Mode navigation - gestes simplifiés
            if gesture == "point":
                # Index = passer en mode laser
                self.toggle_mode()
            else:
                # Autres gestes = navigation
                self.presentation_controller.execute_gesture_action(gesture, cooldown)
                
        elif self.current_mode == "laser":
            # Mode laser - gestes spécialisés
            current_time = time.time()
            last_time = getattr(self, 'last_laser_gesture_time', 0)
            
            if current_time - last_time < cooldown:
                return
                
            if gesture == "point":
                # Index = contrôler le laser (pas d'action spéciale)
                pass
            elif gesture == "fist":
                # Poing = quitter le mode laser
                self.toggle_mode()
                self.last_laser_gesture_time = current_time
            elif gesture == "two":
                # Deux doigts = changer taille
                self.laser_pointer.change_size()
                self.last_laser_gesture_time = current_time
            elif gesture == "three":
                # Trois doigts = changer couleur
                self.laser_pointer.change_color()
                self.last_laser_gesture_time = current_time
            elif gesture == "ok":
                # OK = mode dessin
                self.laser_pointer.toggle_drawing()
                self.last_laser_gesture_time = current_time
            elif gesture == "open_hand":
                # Main ouverte = effacer dessins
                self.laser_pointer.clear_drawings()
                self.last_laser_gesture_time = current_time

# Alias pour compatibilité
EnhancedPresentationController = DualModeController
