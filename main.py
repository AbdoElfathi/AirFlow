import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math
from threading import Thread
from dataclasses import dataclass
from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import ttk, messagebox

@dataclass
class GestureConfig:
    """Configuration des gestes et de leur sensibilité"""
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    gesture_cooldown: float = 1.0  # Délai entre gestes (secondes)
    distance_threshold: float = 0.15  # Distance minimum pour activer
    laser_pointer_color: Tuple[int, int, int] = (0, 0, 255)  # Rouge
    laser_pointer_radius: int = 10

class GestureDetector:
    """Détecteur de gestes basé sur MediaPipe"""
    
    def __init__(self, config: GestureConfig):
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=config.min_detection_confidence,
            min_tracking_confidence=config.min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def get_landmarks(self, image) -> Optional[List]:
        """Extrait les landmarks de la main depuis l'image"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)
        
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark
        return None
    
    def calculate_distance(self, point1, point2) -> float:
        """Calcule la distance euclidienne entre deux points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_finger_extended(self, landmarks, finger_tip_id: int, finger_pip_id: int) -> bool:
        """Vérifie si un doigt est étendu"""
        return landmarks[finger_tip_id].y < landmarks[finger_pip_id].y
    
    def count_extended_fingers(self, landmarks) -> int:
        """Compte le nombre de doigts étendus"""
        finger_tips = [4, 8, 12, 16, 20]  # Pouce, Index, Majeur, Annulaire, Auriculaire
        finger_pips = [3, 6, 10, 14, 18]
        
        extended_count = 0
        
        # Pouce (logique différente car il bouge latéralement)
        if landmarks[4].x > landmarks[3].x:  # Pouce étendu vers la droite
            extended_count += 1
            
        # Autres doigts
        for i in range(1, 5):
            if self.is_finger_extended(landmarks, finger_tips[i], finger_pips[i]):
                extended_count += 1
                
        return extended_count
    
    def detect_gesture(self, landmarks) -> str:
        """Détecte le type de geste basé sur les landmarks"""
        if not landmarks:
            return "none"
        
        extended_fingers = self.count_extended_fingers(landmarks)
        
        # Geste OK (pouce + index)
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        if self.calculate_distance(thumb_tip, index_tip) < 0.05 and extended_fingers <= 2:
            return "ok"
        
        # Classification basée sur le nombre de doigts
        if extended_fingers == 0:
            return "fist"
        elif extended_fingers == 1:
            # Vérifier si c'est l'index qui est étendu
            if self.is_finger_extended(landmarks, 8, 6):
                return "point"
            return "one"
        elif extended_fingers == 2:
            return "two"
        elif extended_fingers == 3:
            return "three"
        elif extended_fingers == 4:
            return "four"
        elif extended_fingers == 5:
            return "open_hand"
        
        return "unknown"

class PresentationController:
    """Contrôleur pour les actions de présentation"""
    
    def __init__(self):
        # Désactiver le fail-safe de pyautogui pour éviter les interruptions
        pyautogui.FAILSAFE = False
        self.last_gesture_time = 0
        self.current_mode = "navigation"  # "navigation" ou "laser"
        
    def execute_gesture_action(self, gesture: str, cooldown: float = 1.0):
        """Exécute l'action correspondant au geste détecté"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < cooldown:
            return
        
        action_map = {
            "fist": self.next_slide,
            "open_hand": self.previous_slide,
            "point": self.toggle_laser_mode,
            "ok": self.toggle_fullscreen,
            "two": lambda: self.go_to_slide(2),
            "three": lambda: self.go_to_slide(3),
            "four": lambda: self.go_to_slide(4),
        }
        
        if gesture in action_map:
            action_map[gesture]()
            self.last_gesture_time = current_time
            print(f"Geste exécuté: {gesture}")
    
    def next_slide(self):
        """Passer à la slide suivante"""
        pyautogui.press('right')  # Ou 'space' pour PowerPoint
    
    def previous_slide(self):
        """Revenir à la slide précédente"""
        pyautogui.press('left')   # Ou 'backspace' pour PowerPoint
    
    def toggle_fullscreen(self):
        """Basculer le mode plein écran"""
        pyautogui.press('f5')     # Démarre le diaporama PowerPoint
    
    def go_to_slide(self, slide_number: int):
        """Aller à une slide spécifique"""
        pyautogui.press(str(slide_number))
        pyautogui.press('enter')
    
    def end_slideshow(self):
        """Terminer le diaporama"""
        pyautogui.press('esc')    # Quitte le mode diaporama
    
    def black_screen(self):
        """Écran noir pendant la présentation"""
        pyautogui.press('b')      # PowerPoint : écran noir
    
    def white_screen(self):
        """Écran blanc pendant la présentation"""
        pyautogui.press('w')      # PowerPoint : écran blanc
    
    def toggle_laser_mode(self):
        """Basculer le mode pointeur laser"""
        self.current_mode = "laser" if self.current_mode == "navigation" else "navigation"
        print(f"Mode: {self.current_mode}")

class GestureControllerGUI:
    """Interface graphique pour le contrôleur gestuel"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contrôleur Gestuel pour Présentations")
        self.root.geometry("600x400")
        
        self.config = GestureConfig()
        self.detector = GestureDetector(self.config)
        self.controller = PresentationController()
        
        self.cap = None
        self.is_running = False
        self.video_thread = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configure l'interface graphique"""
        # Titre
        title_label = tk.Label(self.root, text="Contrôleur Gestuel pour Présentations", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les contrôles
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Boutons de contrôle
        self.start_button = ttk.Button(control_frame, text="Démarrer", 
                                      command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Arrêter", 
                                     command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="Statut: Arrêté", 
                                    font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Liste des gestes
        gesture_frame = ttk.LabelFrame(self.root, text="Gestes Disponibles")
        gesture_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        gestures_text = """
        • Poing fermé → Slide suivante
        • Main ouverte → Slide précédente  
        • Index pointé → Mode pointeur laser
        • Geste OK (pouce+index) → Plein écran
        • 2 doigts → Aller à la slide 2
        • 3 doigts → Aller à la slide 3
        • 4 doigts → Aller à la slide 4
        """
        
        gestures_label = tk.Label(gesture_frame, text=gestures_text, 
                                 justify=tk.LEFT, font=("Arial", 10))
        gestures_label.pack(pady=10)
        
        # Configuration
        config_frame = ttk.LabelFrame(self.root, text="Configuration")
        config_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Cooldown
        cooldown_frame = ttk.Frame(config_frame)
        cooldown_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(cooldown_frame, text="Délai entre gestes (s):").pack(side=tk.LEFT)
        self.cooldown_var = tk.DoubleVar(value=self.config.gesture_cooldown)
        cooldown_scale = ttk.Scale(cooldown_frame, from_=0.5, to=3.0, 
                                  variable=self.cooldown_var, orient=tk.HORIZONTAL)
        cooldown_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
    def start_detection(self):
        """Démarre la détection de gestes"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Erreur", "Impossible d'accéder à la caméra")
                return
            
            self.is_running = True
            self.video_thread = Thread(target=self.video_loop, daemon=True)
            self.video_thread.start()
            
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Statut: Actif - Détection en cours")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du démarrage: {str(e)}")
    
    def stop_detection(self):
        """Arrête la détection de gestes"""
        self.is_running = False
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Statut: Arrêté")
    
    def video_loop(self):
        """Boucle principale de traitement vidéo"""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Miroir horizontal pour une utilisation plus naturelle
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            # Détection des landmarks
            landmarks = self.detector.get_landmarks(frame)
            
            if landmarks:
                # Détection du geste
                gesture = self.detector.detect_gesture(landmarks)
                
                # Affichage du geste détecté
                cv2.putText(frame, f"Geste: {gesture}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Mode pointeur laser
                if self.controller.current_mode == "laser" and gesture == "point":
                    # Afficher le pointeur laser à la position de l'index
                    index_tip = landmarks[8]
                    laser_x = int(index_tip.x * width)
                    laser_y = int(index_tip.y * height)
                    
                    cv2.circle(frame, (laser_x, laser_y), 
                             self.config.laser_pointer_radius, 
                             self.config.laser_pointer_color, -1)
                    
                    cv2.putText(frame, "MODE LASER", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    # Exécuter l'action du geste
                    self.controller.execute_gesture_action(gesture, self.cooldown_var.get())
                
                # Dessiner les landmarks de la main
                self.draw_landmarks(frame, landmarks, width, height)
            
            # Afficher le mode actuel
            mode_color = (0, 0, 255) if self.controller.current_mode == "laser" else (0, 255, 0)
            cv2.putText(frame, f"Mode: {self.controller.current_mode}", (10, height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, mode_color, 2)
            
            # Afficher la fenêtre
            cv2.imshow('Contrôleur Gestuel', frame)
            
            # Sortir avec 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop_detection()
    
    def draw_landmarks(self, frame, landmarks, width, height):
        """Dessine les landmarks de la main sur l'image"""
        # Dessiner les points des articulations
        for landmark in landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
        
        # Dessiner les connexions entre les doigts
        connections = [
            # Pouce
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Index
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Majeur
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Annulaire
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Auriculaire
            (0, 17), (17, 18), (18, 19), (19, 20),
            # Connexions de la paume
            (5, 9), (9, 13), (13, 17)
        ]
        
        for connection in connections:
            start_point = landmarks[connection[0]]
            end_point = landmarks[connection[1]]
            
            start_x = int(start_point.x * width)
            start_y = int(start_point.y * height)
            end_x = int(end_point.x * width)
            end_y = int(end_point.y * height)
            
            cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    
    def run(self):
        """Lance l'application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Gère la fermeture de l'application"""
        if self.is_running:
            self.stop_detection()
        self.root.destroy()

def main():
    """Fonction principale"""
    print("=== Contrôleur Gestuel pour Présentations ===")
    print("Prérequis:")
    print("- Une webcam fonctionnelle")
    print("- Une présentation ouverte (PowerPoint, PDF, etc.)")
    print("\nInstructions:")
    print("1. Lancez votre présentation")
    print("2. Cliquez sur 'Démarrer' dans l'interface")
    print("3. Utilisez les gestes devant la caméra")
    print("4. Appuyez sur 'q' dans la fenêtre vidéo pour quitter")
    print("\n" + "="*50)
    
    try:
        app = GestureControllerGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
    except Exception as e:
        print(f"Erreur: {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")

if __name__ == "__main__":
    main()