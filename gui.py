import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
import math
from config import GestureConfig
from gesture_detector import GestureDetector
from presentation_controller import PresentationController

class ModernCard(tk.Frame):
    """Carte moderne avec ombre et effets"""
    
    def __init__(self, parent, bg_color="#FFFFFF", shadow_color="#E0E0E0", **kwargs):
        super().__init__(parent, bg=shadow_color, **kwargs)
        
        # Effet d'ombre
        self.shadow_frame = tk.Frame(self, bg=shadow_color, height=3)
        self.shadow_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Contenu principal
        self.content_frame = tk.Frame(self, bg=bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
    def get_content_frame(self):
        return self.content_frame

class ModernButton(tk.Button):
    """Bouton moderne simplifié et fiable"""
    
    def __init__(self, parent, text, command=None, bg_color="#4285F4", hover_color="#3367D6", 
                 text_color="white", icon="", **kwargs):
        
        # Configuration de base
        super().__init__(parent, 
                        text=f"{icon} {text}" if icon else text,
                        command=command,
                        bg=bg_color,
                        fg=text_color,
                        font=("Segoe UI", 11, "bold"),
                        relief="flat",
                        bd=0,
                        padx=20,
                        pady=12,
                        cursor="hand2",
                        **kwargs)
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        
        # Événements hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        self.configure(bg=self.hover_color)
        
    def on_leave(self, event):
        self.configure(bg=self.bg_color)

class GestureCard(tk.Frame):
    """Carte pour afficher un geste avec animation"""
    
    def __init__(self, parent, gesture_icon, gesture_name, action, color="#4285F4", **kwargs):
        super().__init__(parent, bg="#FFFFFF", relief="flat", bd=1, **kwargs)
        
        self.gesture_icon = gesture_icon
        self.gesture_name = gesture_name
        self.action = action
        self.color = color
        self.is_active = False
        
        self.setup_card()
        
    def setup_card(self):
        """Configure la carte"""
        # Barre colorée en haut
        color_bar = tk.Frame(self, bg=self.color, height=5)
        color_bar.pack(fill=tk.X)
        
        # Contenu
        content = tk.Frame(self, bg="#FFFFFF")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icône grande
        self.icon_label = tk.Label(content, text=self.gesture_icon, 
                                  bg="#FFFFFF", font=("Segoe UI Emoji", 32))
        self.icon_label.pack()
        
        # Nom du geste
        name_label = tk.Label(content, text=self.gesture_name, 
                             bg="#FFFFFF", fg="#333333",
                             font=("Segoe UI", 12, "bold"))
        name_label.pack(pady=(8, 0))
        
        # Action
        action_label = tk.Label(content, text=self.action, 
                               bg="#FFFFFF", fg="#666666",
                               font=("Segoe UI", 10), wraplength=150)
        action_label.pack(pady=(4, 0))
        
    def activate(self):
        """Active l'animation de la carte"""
        if not self.is_active:
            self.is_active = True
            self.configure(bg=self.color, relief="solid", bd=3)
            self.icon_label.configure(bg=self.color, font=("Segoe UI Emoji", 36))
            
    def deactivate(self):
        """Désactive l'animation"""
        self.is_active = False
        self.configure(bg="#FFFFFF", relief="flat", bd=1)
        self.icon_label.configure(bg="#FFFFFF", font=("Segoe UI Emoji", 32))

class StatusIndicator(tk.Frame):
    """Indicateur de statut simplifié"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#F8F9FA", relief="solid", bd=1, **kwargs)
        
        self.status = "Arrêté"
        self.is_active = False
        
        self.status_label = tk.Label(self, text="🔴 Arrêté", 
                                   bg="#F8F9FA", fg="#666666",
                                   font=("Segoe UI", 10, "bold"),
                                   padx=10, pady=8)
        self.status_label.pack()
        
    def set_status(self, status, is_active=False):
        self.status = status
        self.is_active = is_active
        
        if is_active:
            self.status_label.config(text=f"🟢 {status}", fg="#4CAF50")
            self.configure(bg="#E8F5E8")
            self.status_label.configure(bg="#E8F5E8")
        else:
            self.status_label.config(text=f"🔴 {status}", fg="#666666")
            self.configure(bg="#F8F9FA")
            self.status_label.configure(bg="#F8F9FA")

class ModernGestureControllerGUI:
    """Interface graphique moderne et responsive - 3 gestes uniquement"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Gesture Navigator Pro - Contrôle Simplifié")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        self.root.configure(bg="#F5F7FA")
        
        # Configuration avec précision améliorée
        self.config = GestureConfig()
        # Augmenter la précision pour les 3 gestes principaux
        self.config.min_detection_confidence = 0.8  # Plus strict
        self.config.min_tracking_confidence = 0.8   # Plus strict
        self.config.gesture_cooldown = 1.5          # Plus de temps entre gestes
        
        self.detector = GestureDetector(self.config)
        self.controller = PresentationController()
        
        # Variables
        self.cap = None
        self.is_running = False
        self.video_thread = None
        self.gesture_cards = {}
        self.current_gesture = "none"
        self.current_fps = 0
        self.gesture_confidence = 0.0
        
        self.setup_styles()
        self.create_interface()
        
        # Responsive design
        self.root.bind("<Configure>", self.on_window_resize)
        
    def setup_styles(self):
        """Configure les styles modernes"""
        self.colors = {
            'primary': '#4285F4',
            'secondary': '#34A853', 
            'accent': '#FBBC04',
            'danger': '#EA4335',
            'dark': '#202124',
            'light': '#F8F9FA',
            'card': '#FFFFFF',
            'text_primary': '#202124',
            'text_secondary': '#5F6368'
        }
        
    def create_interface(self):
        """Crée l'interface moderne et responsive"""
        # En-tête fixe
        self.create_header()
        
        # Container principal avec scrollbar si nécessaire
        self.main_canvas = tk.Canvas(self.root, bg="#F5F7FA", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame principal dans le canvas
        self.main_frame = tk.Frame(self.main_canvas, bg="#F5F7FA")
        self.canvas_frame = self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        self.main_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")
        
        # Contenu
        self.create_responsive_content()
        
        # Mise à jour du scroll
        self.main_frame.bind("<Configure>", self.update_scroll_region)
        
    def create_header(self):
        """En-tête moderne compact"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Container centré
        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(expand=True, fill=tk.BOTH)
        
        # Titre
        title = tk.Label(header_content, 
                        text="🎯 Gesture Navigator Pro - Contrôle Simplifié", 
                        bg=self.colors['primary'], fg="white",
                        font=("Segoe UI", 16, "bold"))
        title.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Badge "3 Gestes"
        badge = tk.Label(header_content, text="3 GESTES",
                        bg="#1A73E8", fg="white",
                        font=("Segoe UI", 9, "bold"),
                        padx=8, pady=4)
        badge.pack(side=tk.RIGHT, padx=20, pady=20)
        
    def create_responsive_content(self):
        """Crée le contenu responsive"""
        # Section contrôles (toujours en haut)
        self.create_control_section()
        
        # Section gestes - 3 gestes uniquement
        self.create_gestures_section()
        
        # Section instructions simplifiées
        self.create_instructions_section()
        
    def create_control_section(self):
        """Section contrôles responsive"""
        control_frame = tk.Frame(self.main_frame, bg="#F5F7FA")
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Card contrôles
        control_card = ModernCard(control_frame, bg_color="#FFFFFF")
        control_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        content = control_card.get_content_frame()
        
        # Titre
        tk.Label(content, text="🎮 Contrôles",
                bg="#FFFFFF", fg=self.colors['text_primary'],
                font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))
        
        # Boutons modernes
        button_frame = tk.Frame(content, bg="#FFFFFF")
        button_frame.pack(pady=10)
        
        self.start_btn = ModernButton(button_frame, "DÉMARRER", 
                                     command=self.start_detection,
                                     bg_color=self.colors['secondary'],
                                     hover_color="#2E8B47",
                                     icon="▶️", width=15)
        self.start_btn.pack(pady=5)
        
        self.stop_btn = ModernButton(button_frame, "ARRÊTER",
                                    command=self.stop_detection, 
                                    bg_color=self.colors['danger'],
                                    hover_color="#C53929",
                                    icon="⏹️", width=15)
        self.stop_btn.pack(pady=5)
        
        # Card statistiques avec précision
        stats_card = ModernCard(control_frame, bg_color="#FFFFFF")
        stats_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        stats_content = stats_card.get_content_frame()
        
        tk.Label(stats_content, text="📊 Précision",
                bg="#FFFFFF", fg=self.colors['text_primary'],
                font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))
        
        self.fps_label = tk.Label(stats_content, text="FPS: --",
                                 bg="#FFFFFF", fg=self.colors['text_secondary'],
                                 font=("Segoe UI", 11))
        self.fps_label.pack(pady=2)
        
        self.confidence_label = tk.Label(stats_content, text="Confiance: --%",
                                        bg="#FFFFFF", fg=self.colors['text_secondary'],
                                        font=("Segoe UI", 11))
        self.confidence_label.pack(pady=2)
        
        self.gesture_count_label = tk.Label(stats_content, text="Gestes: 0",
                                           bg="#FFFFFF", fg=self.colors['text_secondary'],
                                           font=("Segoe UI", 11))
        self.gesture_count_label.pack(pady=2)
        
        # Statut
        self.status_indicator = StatusIndicator(stats_content)
        self.status_indicator.pack(pady=10)
        
    def create_gestures_section(self):
        """Section gestes - 3 gestes uniquement"""
        gestures_card = ModernCard(self.main_frame, bg_color="#FFFFFF")
        gestures_card.pack(fill=tk.X, pady=(0, 15))
        
        content = gestures_card.get_content_frame()
        
        # Titre avec badge
        title_frame = tk.Frame(content, bg="#FFFFFF")
        title_frame.pack(fill=tk.X, pady=(15, 15))
        
        tk.Label(title_frame, text="✋ Gestes Simplifiés (3 uniquement)",
                bg="#FFFFFF", fg=self.colors['text_primary'],
                font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        
        self.current_gesture_badge = tk.Label(title_frame, text="Aucun",
                                             bg=self.colors['accent'], fg="white",
                                             font=("Segoe UI", 10, "bold"),
                                             padx=12, pady=6)
        self.current_gesture_badge.pack(side=tk.RIGHT)
        
        # Conteneur pour les 3 gestes
        self.gestures_container = tk.Frame(content, bg="#FFFFFF")
        self.gestures_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 3 gestes uniquement - Plus grands et centrés
        self.create_simplified_gesture_grid()
        
    def create_simplified_gesture_grid(self):
        """Crée une grille de 3 gestes uniquement"""
        gestures = [
            ("✊", "Poing", "Slide suivante", "#EA4335"),
            ("🖐", "Main ouverte", "Slide précédente", "#34A853"),
            ("👌", "Trois doigts", "Démarrer/Arrêter diaporama", "#FBBC04")
        ]
        
        # 3 colonnes pour les 3 gestes
        for i, (icon, name, action, color) in enumerate(gestures):
            card = GestureCard(self.gestures_container, icon, name, action, color)
            card.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            
            self.gesture_cards[name.lower().replace(" ", "_")] = card
            
        # Configurer les colonnes pour qu'elles s'étendent également
        for i in range(3):
            self.gestures_container.grid_columnconfigure(i, weight=1)
            
    def create_instructions_section(self):
        """Section instructions simplifiées pour 3 gestes"""
        instructions_card = ModernCard(self.main_frame, bg_color="#FFFFFF")
        instructions_card.pack(fill=tk.X, pady=(0, 15))
        
        content = instructions_card.get_content_frame()
        
        # Titre
        tk.Label(content, text="📖 Instructions Simplifiées",
                bg="#FFFFFF", fg=self.colors['text_primary'],
                font=("Segoe UI", 14, "bold")).pack(pady=(15, 10))
        
        # Instructions en 3 colonnes
        self.instructions_container = tk.Frame(content, bg="#FFFFFF")
        self.instructions_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Trois sections d'instructions simplifiées
        sections = [
            ("🔧 PRÉPARATION", "#E8F5E8", "#2E7D32", [
                "✓ Webcam fonctionnelle",
                "✓ Présentation ouverte", 
                "✓ Bon éclairage",
                "✓ Distance: 60cm"
            ]),
            ("🎯 3 GESTES SIMPLES", "#E3F2FD", "#1565C0", [
                "✊ Poing = Slide suivante",
                "🖐 Main ouverte = Slide précédente",
                "👌 Trois doigts = Démarrer/Arrêter",
                "⏱️ Attendez 1.5s entre gestes"
            ]),
            ("💡 CONSEILS", "#FFF3E0", "#E65100", [
                "• Gestes bien distincts",
                "• Main dans le cercle bleu",
                "• Mouvements lents et clairs", 
                "• 'Q' pour quitter la caméra"
            ])
        ]
        
        for i, (title, bg_color, fg_color, items) in enumerate(sections):
            section_frame = tk.Frame(self.instructions_container, bg=bg_color, relief="solid", bd=1)
            section_frame.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            tk.Label(section_frame, text=title, bg=bg_color, fg=fg_color,
                    font=("Segoe UI", 11, "bold")).pack(pady=10)
            
            for item in items:
                tk.Label(section_frame, text=item, bg=bg_color, fg=fg_color,
                        font=("Segoe UI", 9), anchor="w").pack(fill=tk.X, padx=10, pady=2)
        
        # Configurer les colonnes
        for i in range(3):
            self.instructions_container.grid_columnconfigure(i, weight=1)
            
    def on_window_resize(self, event):
        """Gère le redimensionnement de la fenêtre"""
        if event.widget == self.root:
            # Mise à jour de la largeur du canvas
            canvas_width = event.width - 30
            self.main_canvas.itemconfig(self.canvas_frame, width=canvas_width)
                
    def update_scroll_region(self, event):
        """Met à jour la région de scroll"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        
    def update_gesture_display(self, gesture, confidence=0.0):
        """Met à jour l'affichage du geste actuel avec confiance"""
        # Désactiver toutes les cartes
        for card in self.gesture_cards.values():
            card.deactivate()
        
        # Activer la carte correspondante (seulement pour les 3 gestes)
        gesture_map = {
            "fist": "poing",
            "open_hand": "main_ouverte", 
            "three": "trois_doigts"
        }
        
        mapped_gesture = gesture_map.get(gesture, "")
        if mapped_gesture in self.gesture_cards:
            self.gesture_cards[mapped_gesture].activate()
            
        # Mettre à jour le badge
        gesture_names = {
            "fist": "Poing",
            "open_hand": "Main ouverte",
            "three": "Trois doigts",
            "none": "Aucun"
        }
        
        display_name = gesture_names.get(gesture, "Aucun")
        self.current_gesture_badge.config(text=display_name)
        
        # Changer la couleur du badge selon le geste
        colors = {
            "Poing": "#EA4335",
            "Main ouverte": "#34A853",
            "Trois doigts": "#FBBC04",
            "Aucun": "#757575"
        }
        
        self.current_gesture_badge.config(bg=colors.get(display_name, "#757575"))
        
        # Mettre à jour la confiance
        self.gesture_confidence = confidence
        confidence_percent = confidence * 100
        if confidence > 0:
            confidence_color = "#4CAF50" if confidence > 0.7 else "#FF9800" if confidence > 0.5 else "#F44336"
            self.confidence_label.config(text=f"Confiance: {confidence_percent:.1f}%", fg=confidence_color)
        else:
            self.confidence_label.config(text="Confiance: --%", fg=self.colors['text_secondary'])
        
    def start_detection(self):
        """Démarre la détection avec précision améliorée"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Erreur", "Impossible d'accéder à la caméra")
                return
            
            # Configuration de la caméra pour une meilleure qualité
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            self.video_thread = Thread(target=self.video_loop, daemon=True)
            self.video_thread.start()
            
            self.status_indicator.set_status("Détection haute précision", True)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du démarrage: {str(e)}")
    
    def stop_detection(self):
        """Arrête la détection"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        self.status_indicator.set_status("Arrêté", False)
        self.update_gesture_display("none", 0.0)
        
    def video_loop(self):
        """Boucle vidéo avec détection améliorée pour 3 gestes"""
        gesture_count = 0
        fps_counter = 0
        last_fps_time = time.time()
        last_gesture_time = 0
        gesture_stability_count = 0
        required_stability = 5  # Nombre de frames consécutives pour valider un geste
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            fps_counter += 1
            current_time = time.time()
            
            # Calcul FPS
            if current_time - last_fps_time >= 1.0:
                fps = fps_counter / (current_time - last_fps_time)
                self.current_fps = fps
                self.fps_label.config(text=f"FPS: {fps:.1f}")
                fps_counter = 0
                last_fps_time = current_time
            
            # Traitement
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            landmarks = self.detector.get_landmarks(frame)
            
            if landmarks:
                detected_gesture = self.detector.detect_gesture(landmarks)
                
                # Filtrer pour ne garder que les 3 gestes autorisés
                if detected_gesture in ["fist", "open_hand", "three"]:
                    # Calculer une confiance basée sur la stabilité de détection
                    if detected_gesture == self.current_gesture:
                        gesture_stability_count += 1
                    else:
                        gesture_stability_count = 1
                        self.current_gesture = detected_gesture
                    
                    # Confiance basée sur la stabilité
                    confidence = min(gesture_stability_count / required_stability, 1.0)
                    
                    # Seulement exécuter si le geste est stable ET assez de temps s'est écoulé
                    if (gesture_stability_count >= required_stability and 
                        current_time - last_gesture_time > self.config.gesture_cooldown):
                        
                        gesture_count += 1
                        self.gesture_count_label.config(text=f"Gestes: {gesture_count}")
                        
                        # Exécution du geste
                        self.controller.execute_gesture_action(detected_gesture, self.config.gesture_cooldown)
                        last_gesture_time = current_time
                        
                    self.update_gesture_display(detected_gesture, confidence)
                else:
                    # Geste non reconnu ou non autorisé
                    self.update_gesture_display("none", 0.0)
                    gesture_stability_count = 0
                    self.current_gesture = "none"
                
                self.add_modern_overlay(frame, detected_gesture if detected_gesture in ["fist", "open_hand", "three"] else "none")
                self.detector.draw_landmarks(frame, landmarks, width, height)
            else:
                self.update_gesture_display("none", 0.0)
                self.add_modern_overlay(frame, "none")
                gesture_stability_count = 0
                self.current_gesture = "none"
            
            cv2.imshow('🎯 Gesture Navigator Pro - Caméra (3 Gestes)', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop_detection()
    
    def add_modern_overlay(self, frame, gesture):
        """Overlay moderne pour la caméra - 3 gestes uniquement"""
        height, width = frame.shape[:2]
        
        # Fond semi-transparent moderne
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 140), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Bordure moderne
        cv2.rectangle(frame, (10, 10), (400, 140), (66, 133, 244), 2)
        
        # Texte moderne
        cv2.putText(frame, "Gesture Navigator Pro - 3 Gestes", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (66, 133, 244), 2)
        
        # Geste actuel
        if gesture in ["fist", "open_hand", "three"]:
            gesture_names = {"fist": "Poing", "open_hand": "Main Ouverte", "three": "Trois Doigts"}
            gesture_text = f"Geste: {gesture_names[gesture]}"
            color = (0, 255, 0)  # Vert pour geste valide
        else:
            gesture_text = "Geste: Aucun reconnu"
            color = (200, 200, 200)  # Gris pour aucun geste
            
        cv2.putText(frame, gesture_text, (20, 65), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Confiance
        confidence_text = f"Confiance: {self.gesture_confidence*100:.1f}%"
        conf_color = (0, 255, 0) if self.gesture_confidence > 0.7 else (0, 165, 255) if self.gesture_confidence > 0.5 else (0, 0, 255)
        cv2.putText(frame, confidence_text, (20, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, conf_color, 2)
        
        # Statut
        cv2.putText(frame, "Status: Haute precision (3 gestes)", (20, 115), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (76, 175, 80), 2)
        
        cv2.putText(frame, "Appuyez sur 'Q' pour quitter", (20, 135), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Zone de détection améliorée - Plus précise
        center_x, center_y = width // 2, height // 2
        
        # Cercle principal plus visible
        cv2.circle(frame, (center_x, center_y), 120, (66, 133, 244), 3)
        
        # Cercle intérieur pour la zone optimale
        cv2.circle(frame, (center_x, center_y), 80, (0, 255, 0), 2)
        
        cv2.putText(frame, "Zone optimale", (center_x - 60, center_y + 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        cv2.putText(frame, "Zone de detection", (center_x - 80, center_y + 140), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (66, 133, 244), 1)
        
        # Indicateurs de coins pour guidance précise
        corner_size = 25
        corner_thickness = 2
        
        # Coins de la zone optimale (cercle intérieur)
        corner_offset = int(80 * 0.707)  # 80 * cos(45°) pour les coins du carré inscrit
        
        # Coin supérieur gauche
        cv2.line(frame, (center_x - corner_offset, center_y - corner_offset), 
                (center_x - corner_offset + corner_size, center_y - corner_offset), (0, 255, 0), corner_thickness)
        cv2.line(frame, (center_x - corner_offset, center_y - corner_offset), 
                (center_x - corner_offset, center_y - corner_offset + corner_size), (0, 255, 0), corner_thickness)
        
        # Coin supérieur droit
        cv2.line(frame, (center_x + corner_offset, center_y - corner_offset), 
                (center_x + corner_offset - corner_size, center_y - corner_offset), (0, 255, 0), corner_thickness)
        cv2.line(frame, (center_x + corner_offset, center_y - corner_offset), 
                (center_x + corner_offset, center_y - corner_offset + corner_size), (0, 255, 0), corner_thickness)
        
        # Coin inférieur gauche
        cv2.line(frame, (center_x - corner_offset, center_y + corner_offset), 
                (center_x - corner_offset + corner_size, center_y + corner_offset), (0, 255, 0), corner_thickness)
        cv2.line(frame, (center_x - corner_offset, center_y + corner_offset), 
                (center_x - corner_offset, center_y + corner_offset - corner_size), (0, 255, 0), corner_thickness)
        
        # Coin inférieur droit
        cv2.line(frame, (center_x + corner_offset, center_y + corner_offset), 
                (center_x + corner_offset - corner_size, center_y + corner_offset), (0, 255, 0), corner_thickness)
        cv2.line(frame, (center_x + corner_offset, center_y + corner_offset), 
                (center_x + corner_offset, center_y + corner_offset - corner_size), (0, 255, 0), corner_thickness)
        
        # Point central précis
        cv2.circle(frame, (center_x, center_y), 4, (255, 255, 255), -1)
        cv2.circle(frame, (center_x, center_y), 6, (0, 0, 0), 2)
        
        # Indicateur de performance et statistiques
        perf_text = f"FPS: {self.current_fps:.0f}"
        cv2.putText(frame, perf_text, (width - 120, height - 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Indicateur du geste actuel en bas
        if gesture in ["fist", "open_hand", "three"]:
            actions = {"fist": "SLIDE SUIVANTE", "open_hand": "SLIDE PRECEDENTE", "three": "DEMARRER/ARRETER"}
            action_text = actions[gesture]
            cv2.putText(frame, f"ACTION: {action_text}", (20, height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Indicateur de stabilité du geste
        if hasattr(self, 'gesture_confidence') and self.gesture_confidence > 0:
            # Barre de progression pour la confiance
            bar_width = 200
            bar_height = 10
            bar_x = width - bar_width - 20
            bar_y = height - 40
            
            # Fond de la barre
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
            
            # Barre de progression
            progress_width = int(bar_width * self.gesture_confidence)
            bar_color = (0, 255, 0) if self.gesture_confidence > 0.7 else (0, 165, 255) if self.gesture_confidence > 0.5 else (0, 0, 255)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), bar_color, -1)
            
            # Texte de la barre
            cv2.putText(frame, "Stabilite", (bar_x, bar_y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Instructions pour les 3 gestes spécifiques
        if gesture == "none":
            instruction_text = "Faites un geste: Poing, Main ouverte ou 3 doigts"
            cv2.putText(frame, instruction_text, (center_x - 200, center_y - 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
    def run(self):
        """Lance l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Gestion de la fermeture"""
        if self.is_running:
            self.stop_detection()
        self.root.destroy()

# Alias pour compatibilité
class GestureControllerGUI(ModernGestureControllerGUI):
    """Alias pour la compatibilité"""
    pass

# Classe principale pour l'export
ModernGestureControllerGUI = ModernGestureControllerGUI

if __name__ == "__main__":
    app = ModernGestureControllerGUI()
    app.run()