"""
Interface graphique moderne avec mode laser intégré - Partie finale
"""
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
from config import GestureConfig
from gesture_detector import GestureDetector
from laser_mode import EnhancedPresentationController

# ... [Classes ModernButton, AnimatedStatusBar, GestureVisualizer, LaserControlPanel déjà définies] ...

class ModernGestureControllerGUI:
    """Interface graphique moderne pour le contrôleur gestuel avec laser"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contrôleur Gestuel Avancé - Mode Laser")
        self.root.geometry("1200x800")
        
        # Style moderne
        self.setup_style()
        
        self.config = GestureConfig()
        self.detector = GestureDetector(self.config)
        self.controller = EnhancedPresentationController()  # Utiliser la version améliorée
        
        self.cap = None
        self.is_running = False
        self.video_thread = None
        
        self.setup_modern_gui()
        
    # ... [Méthodes setup_style, setup_modern_gui, create_header, etc. déjà définies] ...
    
    def modern_video_loop(self):
        """Boucle vidéo moderne avec statistiques et laser"""
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
            
            # Traitement standard
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            landmarks = self.detector.get_landmarks(frame)
            
            if landmarks:
                gesture = self.detector.detect_gesture(landmarks)
                
                if gesture != "none":
                    gesture_count += 1
                    self.gesture_count_label.config(text=f"Gestes détectés: {gesture_count}")
                
                # Mise à jour du visualiseur
                self.gesture_visualizer.update_gesture(gesture)
                
                # Affichage moderne sur la frame
                self.add_modern_overlay(frame, gesture, landmarks, width, height)
                
                # Gestion du mode laser
                if self.controller.current_mode == "laser" and gesture == "point":
                    # Obtenir la position de l'index
                    index_tip = landmarks[8]
                    
                    # Mettre à jour la position du laser plein écran
                    self.controller.update_laser_position(index_tip.x, index_tip.y)
                    
                    # Afficher aussi le laser dans la fenêtre caméra
                    laser_x = int(index_tip.x * width)
                    laser_y = int(index_tip.y * height)
                    cv2.circle(frame, (laser_x, laser_y), 15, (0, 0, 255), -1)
                    cv2.circle(frame, (laser_x, laser_y), 25, (0, 0, 255), 2)
                    cv2.putText(frame, "LASER ACTIF", (laser_x + 30, laser_y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    # Exécuter les actions de gestes
                    self.controller.execute_gesture_action(gesture, self.config.gesture_cooldown)
                
                # Mettre à jour l'indicateur de mode
                mode = self.controller.current_mode
                self.mode_indicator.config(text=f"🎯 Mode: {mode.title()}")
                self.laser_control.update_laser_status()
                
                self.detector.draw_landmarks(frame, landmarks, width, height)
            
            cv2.imshow('🎯 Contrôleur Gestuel Avancé - Mode Laser', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.stop_detection()
    
    def add_modern_overlay(self, frame, gesture, landmarks, width, height):
        """Ajoute un overlay moderne à la frame"""
        # Fond semi-transparent pour les infos
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 140), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Informations stylées
        cv2.putText(frame, f"Geste: {gesture.replace('_', ' ').title()}", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.putText(frame, f"Mode: {self.controller.current_mode.title()}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Instructions spécifiques au mode
        if self.controller.current_mode == "laser":
            cv2.putText(frame, "MODE LASER - Pointez avec l'index", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "Poing ferme = Desactiver", (20, 105), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, "Geste OK = Changer couleur", (20, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "Index pointe = Activer laser", (20, 85), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Appuyez sur 'q' pour quitter", (20, 105), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
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
