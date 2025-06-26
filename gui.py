"""
Interface graphique moderne épurée - Version finale sans distractions
"""
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
from config import GestureConfig
from gesture_detector import GestureDetector
from laser_mode import DualModeController

class ModernButton(tk.Canvas):
    """Bouton moderne avec effets hover et animations"""
    
    def __init__(self, parent, text, command=None, bg_color="#4A90E2", hover_color="#357ABD", 
                 text_color="white", width=120, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.is_hovered = False
        
        self.configure(bg=parent.cget('bg'))
        self.draw_button()
        
        # Événements
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw_button(self):
        """Dessine le bouton avec bordures arrondies"""
        self.delete("all")
        
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Ombre (sans transparence)
        self.create_rectangle(2, 2, self.winfo_reqwidth()-2, self.winfo_reqheight()-2, 
                            fill="#D0D0D0", outline="", width=0)
        
        # Bouton principal avec coins arrondis simulés
        margin = 4
        self.create_rectangle(margin, margin, self.winfo_reqwidth()-margin, 
                            self.winfo_reqheight()-margin, fill=color, outline="", width=0)
        
        # Texte
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, 
                        text=self.text, fill=self.text_color, font=("Segoe UI", 10, "bold"))
        
    def on_enter(self, event):
        """Effet hover"""
        self.is_hovered = True
        self.draw_button()
        
    def on_leave(self, event):
        """Fin effet hover"""
        self.is_hovered = False
        self.draw_button()
        
    def on_click(self, event):
        """Gestion du clic"""
        if self.command:
            self.command()

class AnimatedStatusBar(tk.Canvas):
    """Barre de statut animée"""
    
    def __init__(self, parent, width=400, height=30, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.status = "Arrêté"
        self.animation_step = 0
        self.is_active = False
        
        self.configure(bg=parent.cget('bg'))
        self.update_status()
        
    def set_status(self, status, is_active=False):
        """Met à jour le statut"""
        self.status = status
        self.is_active = is_active
        self.update_status()
        
        if is_active:
            self.animate()
            
    def update_status(self):
        """Met à jour l'affichage du statut"""
        self.delete("all")
        
        # Fond
        bg_color = "#2ECC71" if self.is_active else "#95A5A6"
        self.create_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(), 
                             fill=bg_color, outline="")
        
        # Texte
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, 
                        text=f"Statut: {self.status}", fill="white", 
                        font=("Segoe UI", 10, "bold"))
        
        # Animation pour le mode actif (sans transparence)
        if self.is_active:
            x = (self.animation_step % 100) * (self.winfo_reqwidth() / 100)
            self.create_rectangle(x, 0, x+20, self.winfo_reqheight(), 
                                 fill="#A8E6CF", outline="")
            
    def animate(self):
        """Animation de la barre"""
        if self.is_active:
            self.animation_step += 2
            self.update_status()
            self.after(50, self.animate)

class GestureVisualizer(tk.Canvas):
    """Visualiseur de gestes en temps réel"""
    
    def __init__(self, parent, width=300, height=200, **kwargs):
        super().__init__(parent, width=width, height=height, bg="#2C3E50", highlightthickness=0, **kwargs)
        
        self.current_gesture = "none"
        self.gesture_colors = {
            "fist": "#E74C3C",
            "open_hand": "#2ECC71", 
            "point": "#3498DB",
            "ok": "#F39C12",
            "two": "#9B59B6",
            "three": "#1ABC9C",
            "four": "#E67E22",
            "none": "#95A5A6"
        }
        
        self.draw_background()
        
    def draw_background(self):
        """Dessine le fond avec grille"""
        self.delete("all")
        
        # Grille
        for i in range(0, self.winfo_reqwidth(), 20):
            self.create_line(i, 0, i, self.winfo_reqheight(), fill="#34495E", width=1)
        for i in range(0, self.winfo_reqheight(), 20):
            self.create_line(0, i, self.winfo_reqwidth(), i, fill="#34495E", width=1)
            
        # Titre
        self.create_text(self.winfo_reqwidth()//2, 20, text="Geste Détecté", 
                        fill="white", font=("Segoe UI", 12, "bold"))
        
    def update_gesture(self, gesture):
        """Met à jour le geste affiché"""
        self.current_gesture = gesture
        self.draw_gesture()
        
    def draw_gesture(self):
        """Dessine la représentation du geste"""
        self.draw_background()
        
        center_x = self.winfo_reqwidth() // 2
        center_y = self.winfo_reqheight() // 2
        
        color = self.gesture_colors.get(self.current_gesture, "#95A5A6")
        
        # Cercle principal
        radius = 50
        self.create_oval(center_x-radius, center_y-radius, 
                        center_x+radius, center_y+radius, 
                        fill=color, outline="white", width=3)
        
        # Texte du geste
        self.create_text(center_x, center_y, text=self.current_gesture.replace("_", " ").title(), 
                        fill="white", font=("Segoe UI", 14, "bold"))
        
        # Effet de pulsation
        if self.current_gesture != "none":
            pulse_radius = radius + 10
            self.create_oval(center_x-pulse_radius, center_y-pulse_radius,
                           center_x+pulse_radius, center_y+pulse_radius,
                           outline=color, width=2)

class LaserControlPanel(tk.Frame):
    """Panel de contrôle spécifique au mode laser épuré"""
    
    def __init__(self, parent, controller, colors, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.colors = colors
        
        self.configure(bg=colors['light'])
        self.create_laser_controls()
        
    def create_laser_controls(self):
        """Crée les contrôles du mode laser épuré"""
        # Titre
        title = tk.Label(self, text="🔴 Pointeur Laser Épuré", 
                        font=("Segoe UI", 12, "bold"), 
                        bg=self.colors['light'], fg=self.colors['danger'])
        title.pack(pady=(10, 5))
        
        # Instructions simplifiées
        instructions = [
            "👆 Index pointé → Basculer vers mode laser",
            "Interface épurée sans distractions", 
            "Raccourcis clavier disponibles",
            "H = Afficher/masquer aide",
            "Feedback temporaire uniquement",
            "✊ Poing fermé → Quitter mode laser"
        ]
        
        for instruction in instructions:
            label = tk.Label(self, text=instruction, font=("Segoe UI", 9),
                           bg=self.colors['light'], fg=self.colors['dark'],
                           anchor="w")
            label.pack(fill=tk.X, padx=10, pady=2)
            
        # Statut laser
        self.laser_status = tk.Label(self, text="🎯 Mode: Navigation Simple", 
                                   font=("Segoe UI", 10, "bold"),
                                   bg=self.colors['light'], fg=self.colors['secondary'])
        self.laser_status.pack(pady=(10, 5))
        
        # Couleur actuelle
        self.color_status = tk.Label(self, text="🎨 Prêt pour le laser", 
                                   font=("Segoe UI", 9),
                                   bg=self.colors['light'], fg=self.colors['dark'])
        self.color_status.pack(pady=2)
        
        # Taille actuelle
        self.size_status = tk.Label(self, text="📏 Pointeur disponible", 
                                   font=("Segoe UI", 9),
                                   bg=self.colors['light'], fg=self.colors['dark'])
        self.size_status.pack(pady=2)
        
        # Bouton de test laser
        test_btn = ModernButton(self, "🔴 Test Laser", 
                               command=self.test_laser,
                               bg_color=self.colors['warning'],
                               hover_color="#E67E22", width=100, height=30)
        test_btn.pack(pady=5)
        
    def test_laser(self):
        """Test du mode laser"""
        self.controller.toggle_mode()
        self.update_laser_status()
        
    def update_laser_status(self):
        """Met à jour le statut du laser"""
        mode = self.controller.current_mode
        if mode == "laser":
            self.laser_status.config(text="🔴 Mode: Pointeur Laser ACTIF", fg=self.colors['danger'])
            # Afficher les infos du laser
            color_names = {
                "#FF0000": "Rouge", "#00FF00": "Vert", "#0000FF": "Bleu",
                "#FFFF00": "Jaune", "#FF00FF": "Magenta", "#00FFFF": "Cyan", "#FFFFFF": "Blanc"
            }
            size_names = {"small": "Petite", "normal": "Normale", "large": "Grande"}
            
            current_color = getattr(self.controller.laser_pointer, 'current_color', '#FF0000')
            current_size = getattr(self.controller.laser_pointer, 'pointer_size', 'normal')
            
            color_name = color_names.get(current_color, "Rouge")
            size_name = size_names.get(current_size, "Normale")
            
            self.color_status.config(text=f"🎨 Couleur: {color_name}")
            self.size_status.config(text=f"📏 Taille: {size_name}")
        else:
            self.laser_status.config(text="🎯 Mode: Navigation Simple", fg=self.colors['secondary'])
            self.color_status.config(text="🎨 Prêt pour le laser")
            self.size_status.config(text="📏 Pointeur disponible")

class ModernGestureControllerGUI:
    """Interface graphique moderne épurée pour le contrôleur gestuel"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Contrôleur Gestuel Épuré - Navigation | Pointeur Laser")
        self.root.geometry("1200x800")
        
        # Style moderne
        self.setup_style()
        
        self.config = GestureConfig()
        self.detector = GestureDetector(self.config)
        self.controller = DualModeController()
        
        self.cap = None
        self.is_running = False
        self.video_thread = None
        
        self.setup_modern_gui()
        
    def setup_style(self):
        """Configure le style moderne"""
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#3498DB', 
            'success': '#2ECC71',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'light': '#ECF0F1',
            'dark': '#34495E',
            'accent': '#9B59B6'
        }
        
        self.root.configure(bg=self.colors['light'])
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TFrame', background=self.colors['light'])
        
    def setup_modern_gui(self):
        """Configure l'interface moderne"""
        # En-tête
        self.create_header()
        
        # Container principal
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Layout en grille 3x2
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # Panels
        self.create_control_panel(main_container)
        self.create_visualization_panel(main_container)
        self.create_laser_panel(main_container)
        self.create_config_panel(main_container)
        self.create_gesture_panel(main_container)
        self.create_modern_status_bar()
        
    def create_header(self):
        """Crée l'en-tête"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="🎯 Contrôleur Gestuel Épuré - Navigation | Pointeur Laser", 
                              bg=self.colors['primary'], fg="white", 
                              font=("Segoe UI", 18, "bold"))
        title_label.place(relx=0.5, rely=0.3, anchor="center")
        
        subtitle_label = tk.Label(header, text="Interface Épurée • Sans Distractions • Pointeur Professionnel", 
                                 bg=self.colors['primary'], fg="#ECF0F1", 
                                 font=("Segoe UI", 10))
        subtitle_label.place(relx=0.5, rely=0.7, anchor="center")
        
    def create_control_panel(self, parent):
        """Panel de contrôle principal"""
        control_frame = ttk.LabelFrame(parent, text=" 🎮 Contrôles Principaux ", style='Modern.TFrame')
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        button_frame = tk.Frame(control_frame, bg=self.colors['light'])
        button_frame.pack(pady=20)
        
        self.start_button = ModernButton(button_frame, "▶ Démarrer", 
                                        command=self.start_detection,
                                        bg_color=self.colors['success'], 
                                        hover_color="#27AE60")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ModernButton(button_frame, "⏹ Arrêter", 
                                       command=self.stop_detection,
                                       bg_color=self.colors['danger'],
                                       hover_color="#C0392B")
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
    def create_visualization_panel(self, parent):
        """Panel de visualisation"""
        viz_frame = ttk.LabelFrame(parent, text=" 📊 Visualisation en Temps Réel ", style='Modern.TFrame')
        viz_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        self.gesture_visualizer = GestureVisualizer(viz_frame)
        self.gesture_visualizer.pack(pady=20)
        
    def create_laser_panel(self, parent):
        """Panel de contrôle laser"""
        laser_frame = ttk.LabelFrame(parent, text=" 🔴 Mode Pointeur Épuré ", style='Modern.TFrame')
        laser_frame.grid(row=0, column=2, sticky="ew", padx=10, pady=5)
        
        self.laser_control = LaserControlPanel(laser_frame, self.controller, self.colors)
        self.laser_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_config_panel(self, parent):
        """Panel de configuration"""
        config_frame = ttk.LabelFrame(parent, text=" ⚙️ Configuration Avancée ", style='Modern.TFrame')
        config_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Sliders
        self.cooldown_var = self.create_modern_slider(config_frame, "Délai entre gestes (s)", 
                                                     0.5, 3.0, 1.0, self.update_cooldown)
        
        self.detection_var = self.create_modern_slider(config_frame, "Seuil de détection", 
                                                      0.3, 0.9, 0.7, self.update_detection_threshold)
        
        # Statistiques
        stats_frame = tk.Frame(config_frame, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.fps_label = tk.Label(stats_frame, text="FPS: 0", bg=self.colors['light'], 
                                 font=("Segoe UI", 10), fg=self.colors['secondary'])
        self.fps_label.pack()
        
        self.gesture_count_label = tk.Label(stats_frame, text="Gestes détectés: 0", 
                                           bg=self.colors['light'], font=("Segoe UI", 10), 
                                           fg=self.colors['secondary'])
        self.gesture_count_label.pack()
        
    def create_gesture_panel(self, parent):
        """Panel des gestes avec séparation claire"""
        gesture_frame = ttk.LabelFrame(parent, text=" 🎮 Deux Modes Séparés ", style='Modern.TFrame')
        gesture_frame.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=5)
        
        # Conteneur avec onglets pour séparer les modes
        notebook = ttk.Notebook(gesture_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet Navigation Simplifié
        nav_frame = tk.Frame(notebook, bg=self.colors['light'])
        notebook.add(nav_frame, text="🎯 Navigation Simple")
        
        # En-tête navigation
        nav_header = tk.Label(nav_frame, text="CONTRÔLES DE NAVIGATION", 
                             font=("Segoe UI", 14, "bold"), bg=self.colors['light'], 
                             fg=self.colors['primary'])
        nav_header.pack(pady=(10, 5))
        
        nav_subtitle = tk.Label(nav_frame, text="Gestes essentiels pour contrôler vos présentations", 
                               font=("Segoe UI", 10), bg=self.colors['light'], 
                               fg=self.colors['dark'])
        nav_subtitle.pack(pady=(0, 15))
        
        nav_gestures = [
            ("✊", "Poing fermé", "Slide suivante", self.colors['danger']),
            ("🖐", "Main ouverte", "Slide précédente", self.colors['success']),
            ("👌", "Geste OK", "Démarrer/Arrêter diaporama (F5)", self.colors['warning']),
            ("👆", "Index pointé", "PASSER EN MODE POINTEUR LASER", self.colors['secondary']),
        ]
        
        for icon, gesture, action, color in nav_gestures:
            self.create_navigation_card(nav_frame, icon, gesture, action, color)
        
        # Note navigation
        nav_note = tk.Label(nav_frame, 
                           text="💡 Mode Navigation : Simple et efficace, seulement 4 gestes essentiels !",
                           bg=self.colors['success'], fg="white", font=("Segoe UI", 10, "bold"),
                           padx=10, pady=8)
        nav_note.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        # Onglet Pointeur Laser Épuré
        laser_frame = tk.Frame(notebook, bg=self.colors['light'])
        notebook.add(laser_frame, text="🔴 Pointeur Laser Épuré")
        
        # En-tête laser
        laser_header = tk.Label(laser_frame, text="POINTEUR LASER ÉPURÉ", 
                               font=("Segoe UI", 14, "bold"), bg=self.colors['light'], 
                               fg=self.colors['danger'])
        laser_header.pack(pady=(10, 5))
        
        laser_subtitle = tk.Label(laser_frame, text="Interface sans distractions avec feedback temporaire uniquement", 
                                 font=("Segoe UI", 10), bg=self.colors['light'], 
                                 fg=self.colors['dark'])
        laser_subtitle.pack(pady=(0, 15))
        
        laser_gestures = [
            ("👆", "Index pointé", "Contrôler la position du pointeur", self.colors['secondary']),
            ("✌️", "Deux doigts", "Changer taille (feedback temporaire)", self.colors['accent']),
            ("🤟", "Trois doigts", "Changer couleur (feedback temporaire)", self.colors['accent']),
            ("👌", "Geste OK", "Mode dessin ON/OFF (indicateur discret)", self.colors['warning']),
            ("🖐", "Main ouverte", "Effacer tous les dessins", self.colors['success']),
            ("✊", "Poing fermé", "RETOUR AU MODE NAVIGATION", self.colors['danger']),
        ]
        
        for icon, gesture, action, color in laser_gestures:
            self.create_laser_card(laser_frame, icon, gesture, action, color)
            
        # Raccourcis clavier laser
        keyboard_frame = tk.Frame(laser_frame, bg=self.colors['dark'])
        keyboard_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        keyboard_title = tk.Label(keyboard_frame, text="⌨️ RACCOURCIS CLAVIER (Mode Laser)", 
                                 bg=self.colors['dark'], fg="white", 
                                 font=("Segoe UI", 11, "bold"), pady=5)
        keyboard_title.pack()
        
        shortcuts = ["C = Couleur", "S = Taille", "D = Dessin", "X = Effacer", "H = Aide ON/OFF", "ESC = Quitter"]
        shortcuts_text = " • ".join(shortcuts)
        
        keyboard_shortcuts = tk.Label(keyboard_frame, text=shortcuts_text,
                                      bg=self.colors['dark'], fg="#cccccc", 
                                      font=("Segoe UI", 9), pady=5)
        keyboard_shortcuts.pack()
        
        # Note importante
        note_frame = tk.Frame(gesture_frame, bg=self.colors['warning'], height=50)
        note_frame.pack(fill=tk.X, side=tk.BOTTOM)
        note_frame.pack_propagate(False)
        
        note_label = tk.Label(note_frame, 
                             text="💡 MODE LASER : Interface épurée sans distractions - Appuyez sur H pour l'aide",
                             bg=self.colors['warning'], fg="white", font=("Segoe UI", 10, "bold"))
        note_label.place(relx=0.5, rely=0.5, anchor="center")
        
    def create_navigation_card(self, parent, icon, gesture, action, color):
        """Carte pour les gestes de navigation"""
        card = tk.Frame(parent, bg="white", relief="solid", bd=2)
        card.pack(fill=tk.X, padx=15, pady=4)
        
        # Barre colorée plus épaisse
        color_bar = tk.Frame(card, bg=color, height=5)
        color_bar.pack(fill=tk.X)
        
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Layout horizontal
        icon_label = tk.Label(content_frame, text=icon, font=("Segoe UI Emoji", 22), bg="white")
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        text_frame = tk.Frame(content_frame, bg="white")
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        gesture_label = tk.Label(text_frame, text=gesture, font=("Segoe UI", 13, "bold"), 
                                bg="white", fg=self.colors['primary'])
        gesture_label.pack(anchor="w")
        
        action_label = tk.Label(text_frame, text=f"→ {action}", font=("Segoe UI", 11), 
                               bg="white", fg=self.colors['dark'])
        action_label.pack(anchor="w")
        
    def create_laser_card(self, parent, icon, gesture, action, color):
        """Carte pour les gestes du laser"""
        card = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
        card.pack(fill=tk.X, padx=15, pady=3)
        
        # Barre colorée
        color_bar = tk.Frame(card, bg=color, height=3)
        color_bar.pack(fill=tk.X)
        
        content_frame = tk.Frame(card, bg="#f8f9fa")
        content_frame.pack(fill=tk.X, padx=12, pady=8)
        
        # Layout horizontal
        icon_label = tk.Label(content_frame, text=icon, font=("Segoe UI Emoji", 16), bg="#f8f9fa")
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        text_frame = tk.Frame(content_frame, bg="#f8f9fa")
        text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        gesture_label = tk.Label(text_frame, text=gesture, font=("Segoe UI", 10, "bold"), 
                                bg="#f8f9fa", fg=self.colors['primary'])
        gesture_label.pack(anchor="w")
        
        action_label = tk.Label(text_frame, text=f"→ {action}", font=("Segoe UI", 9), 
                               bg="#f8f9fa", fg=self.colors['dark'])
        action_label.pack(anchor="w")
        
    def create_modern_slider(self, parent, label, min_val, max_val, initial, callback):
        """Crée un slider moderne"""
        frame = tk.Frame(parent, bg=self.colors['light'])
        frame.pack(fill=tk.X, padx=20, pady=10)
        
        label_widget = tk.Label(frame, text=label, bg=self.colors['light'], 
                               font=("Segoe UI", 10), fg=self.colors['primary'])
        label_widget.pack(anchor="w")
        
        var = tk.DoubleVar(value=initial)
        scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=var, 
                         orient=tk.HORIZONTAL, command=lambda v: callback(var.get()))
        scale.pack(fill=tk.X, pady=(5, 0))
        
        return var
        
    def create_modern_status_bar(self):
        """Crée une barre de statut moderne"""
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_bar = AnimatedStatusBar(status_frame, width=400, height=30)
        self.status_bar.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Indicateurs
        indicators_frame = tk.Frame(status_frame, bg=self.colors['primary'])
        indicators_frame.pack(side=tk.RIGHT, padx=20, pady=5)
        
        self.camera_indicator = tk.Label(indicators_frame, text="📹 Caméra: OFF", 
                                        bg=self.colors['primary'], fg="white", 
                                        font=("Segoe UI", 9))
        self.camera_indicator.pack(side=tk.LEFT, padx=10)
        
        self.mode_indicator = tk.Label(indicators_frame, text="🎯 Mode: Navigation", 
                                      bg=self.colors['primary'], fg="white", 
                                      font=("Segoe UI", 9))
        self.mode_indicator.pack(side=tk.LEFT, padx=10)
        
    def update_cooldown(self, value):
        """Met à jour le délai"""
        self.config.gesture_cooldown = value
        
    def update_detection_threshold(self, value):
        """Met à jour le seuil de détection"""
        self.config.min_detection_confidence = value
        
    def start_detection(self):
        """Démarre la détection"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Erreur", "Impossible d'accéder à la caméra")
                return
            
            self.is_running = True
            self.video_thread = Thread(target=self.modern_video_loop, daemon=True)
            self.video_thread.start()
            
            self.status_bar.set_status("Actif - Détection en cours", True)
            self.camera_indicator.config(text="📹 Caméra: ON", fg=self.colors['success'])
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du démarrage: {str(e)}")
    
    def stop_detection(self):
        """Arrête la détection"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        # Désactiver le laser si actif
        if self.controller.current_mode == "laser":
            self.controller.toggle_mode()
        
        self.status_bar.set_status("Arrêté", False)
        self.camera_indicator.config(text="📹 Caméra: OFF", fg="white")
        self.gesture_visualizer.update_gesture("none")
        self.laser_control.update_laser_status()
        
    def modern_video_loop(self):
        """Boucle vidéo avec laser épuré"""
        gesture_count = 0
        fps_counter = 0
        last_fps_time = time.time()
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            fps_counter += 1
            current_time = time.time()
            
            # Calcul FPS
            if current_time - last_fps_time >= 1.0:
                fps = fps_counter / (current_time - last_fps_time)
                self.fps_label.config(text=f"FPS: {fps:.1f}")
                fps_counter = 0
                last_fps_time = current_time
            
            # Traitement
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            landmarks = self.detector.get_landmarks(frame)
            
            if landmarks:
                gesture = self.detector.detect_gesture(landmarks)
                
                if gesture != "none":
                    gesture_count += 1
                    self.gesture_count_label.config(text=f"Gestes détectés: {gesture_count}")
                
                self.gesture_visualizer.update_gesture(gesture)
                self.add_minimal_overlay(frame, gesture, landmarks, width, height)
                
                # Gestion du laser
                if self.controller.current_mode == "laser" and gesture == "point":
                    index_tip = landmarks[8]
                    
                    # Mettre à jour le laser plein écran
                    self.controller.update_laser_position(index_tip.x, index_tip.y)
                    
                    # Indicateur minimal dans la caméra
                    laser_x = int(index_tip.x * width)
                    laser_y = int(index_tip.y * height)
                    cv2.circle(frame, (laser_x, laser_y), 8, (0, 0, 255), -1)
                    cv2.circle(frame, (laser_x, laser_y), 15, (0, 0, 255), 1)
                else:
                    self.controller.execute_gesture_action(gesture, self.config.gesture_cooldown)
                
                # Mettre à jour l'interface
                mode = self.controller.current_mode
                if mode == "laser":
                    self.mode_indicator.config(text=f"🔴 Mode: Pointeur Laser")
                else:
                    self.mode_indicator.config(text=f"🎯 Mode: Navigation")
                self.laser_control.update_laser_status()
                
                self.detector.draw_landmarks(frame, landmarks, width, height)
            
            cv2.imshow('🎯 Contrôleur Gestuel Épuré', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop_detection()
    
    def add_minimal_overlay(self, frame, gesture, landmarks, width, height):
        """Ajoute un overlay minimal sans distractions"""
        # Fond semi-transparent réduit
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (350, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Informations essentielles uniquement
        cv2.putText(frame, f"Geste: {gesture.replace('_', ' ').title()}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.putText(frame, f"Mode: {self.controller.current_mode.title()}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Instructions contextuelles minimales
        if self.controller.current_mode == "laser":
            cv2.putText(frame, "MODE POINTEUR - Interface epuree", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "MODE NAVIGATION", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    def run(self):
        """Lance l'application moderne"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Gestion de la fermeture"""
        if self.is_running:
            self.stop_detection()
        self.root.destroy()

# Classe de compatibilité pour ne pas casser les imports existants
class GestureControllerGUI(ModernGestureControllerGUI):
    """Alias pour la compatibilité"""
    pass

if __name__ == "__main__":
    app = ModernGestureControllerGUI()
    app.run()