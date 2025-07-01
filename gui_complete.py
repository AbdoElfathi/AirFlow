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
    
    def video_loop(self):
        """Boucle vidéo avec détection améliorée pour 3 gestes"""
        gesture_count = 0
        fps_counter = 0
        last_fps_time = time.time()
        last_gesture_time = 0
        gesture_stability_count = 0
        required_stability = 5  # Nombre de frames consécutives pour valider un geste
        
        try:
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret or not self.is_running:
                    break
                
                fps_counter += 1
                current_time = time.time()
                
                # Calcul FPS
                if current_time - last_fps_time >= 1.0:
                    fps = fps_counter / (current_time - last_fps_time)
                    self.current_fps = fps
                    if self.is_running:  # Vérifier avant de mettre à jour l'interface
                        self.fps_label.config(text=f"FPS: {fps:.1f}")
                    fps_counter = 0
                    last_fps_time = current_time
                
                # Traitement
                frame = cv2.flip(frame, 1)
                height, width, _ = frame.shape
                
                landmarks = self.detector.get_landmarks(frame)
                
                if landmarks and self.is_running:
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
                            current_time - last_gesture_time > self.config.gesture_cooldown and
                            self.is_running):
                            
                            gesture_count += 1
                            if self.is_running:  # Vérifier avant de mettre à jour
                                self.gesture_count_label.config(text=f"Gestes: {gesture_count}")
                            
                            # Exécution du geste
                            self.controller.execute_gesture_action(detected_gesture, self.config.gesture_cooldown)
                            last_gesture_time = current_time
                            
                        if self.is_running:  # Vérifier avant de mettre à jour
                            self.update_gesture_display(detected_gesture, confidence)
                    else:
                        # Geste non reconnu ou non autorisé
                        if self.is_running:
                            self.update_gesture_display("none", 0.0)
                        gesture_stability_count = 0
                        self.current_gesture = "none"
                    
                    if self.is_running:
                        self.add_modern_overlay(frame, detected_gesture if detected_gesture in ["fist", "open_hand", "three"] else "none")
                        self.detector.draw_landmarks(frame, landmarks, width, height)
                else:
                    if self.is_running:
                        self.update_gesture_display("none", 0.0)
                        self.add_modern_overlay(frame, "none")
                    gesture_stability_count = 0
                    self.current_gesture = "none"
                
                # Afficher seulement si on est encore en cours d'exécution
                if self.is_running:
                    cv2.imshow('🎯 Gesture Navigator Pro - Caméra (3 Gestes)', frame)
                    
                    # Vérifier les touches
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q') or not self.is_running:
                        break
                else:
                    break
        
        except Exception as e:
            print(f"Erreur dans la boucle vidéo: {e}")
        
        finally:
            # Nettoyage final
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
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
        """Gestion de la fermeture améliorée"""
        if self.is_running:
            self.is_running = False
            
            # Attendre un peu pour que le thread se termine
            if self.video_thread and self.video_thread.is_alive():
                self.video_thread.join(timeout=1.0)
            
            # Libérer les ressources
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
        
        self.root.destroy()

# Classe de compatibilité pour ne pas casser les imports existants
class GestureControllerGUI(ModernGestureControllerGUI):
    """Alias pour la compatibilité"""
    pass

if __name__ == "__main__":
    app = ModernGestureControllerGUI()
    app.run()
