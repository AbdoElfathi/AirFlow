"""
Utilitaires et fonctions d'aide pour le contrôleur gestuel
"""
import cv2
import numpy as np
from typing import Tuple, List

class VideoUtils:
    """Utilitaires pour le traitement vidéo"""
    
    @staticmethod
    def add_text_with_background(frame, text: str, position: Tuple[int, int], 
                               font_scale: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255),
                               bg_color: Tuple[int, int, int] = (0, 0, 0), thickness: int = 2):
        """Ajoute du texte avec un arrière-plan"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Calculer la taille du texte
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Dessiner l'arrière-plan
        cv2.rectangle(frame, 
                     (position[0] - 5, position[1] - text_height - 5),
                     (position[0] + text_width + 5, position[1] + baseline + 5),
                     bg_color, -1)
        
        # Dessiner le texte
        cv2.putText(frame, text, position, font, font_scale, color, thickness)
    
    @staticmethod
    def draw_fps(frame, fps: float, position: Tuple[int, int] = (10, 30)):
        """Affiche le FPS sur l'image"""
        fps_text = f"FPS: {fps:.1f}"
        VideoUtils.add_text_with_background(frame, fps_text, position, 
                                          color=(0, 255, 0), bg_color=(0, 0, 0))
    
    @staticmethod
    def resize_frame(frame, max_width: int = 640, max_height: int = 480):
        """Redimensionne l'image en conservant le ratio"""
        height, width = frame.shape[:2]
        
        # Calculer le ratio
        ratio = min(max_width / width, max_height / height)
        
        if ratio < 1:
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            frame = cv2.resize(frame, (new_width, new_height))
        
        return frame

class MathUtils:
    """Utilitaires mathématiques"""
    
    @staticmethod
    def smooth_value(current_value: float, new_value: float, smoothing_factor: float = 0.8) -> float:
        """Lisse une valeur avec un facteur de lissage"""
        return current_value * smoothing_factor + new_value * (1 - smoothing_factor)
    
    @staticmethod
    def map_range(value: float, from_min: float, from_max: float, 
                  to_min: float, to_max: float) -> float:
        """Mappe une valeur d'un intervalle à un autre"""
        return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Limite une valeur entre min et max"""
        return max(min_val, min(value, max_val))

class PerformanceMonitor:
    """Moniteur de performance pour l'application"""
    
    def __init__(self, window_size: int = 30):
        self.window_size = window_size
        self.frame_times = []
        self.last_time = None
    
    def update(self) -> float:
        """Met à jour le moniteur et retourne le FPS actuel"""
        import time
        current_time = time.time()
        
        if self.last_time is not None:
            frame_time = current_time - self.last_time
            self.frame_times.append(frame_time)
            
            if len(self.frame_times) > self.window_size:
                self.frame_times.pop(0)
        
        self.last_time = current_time
        
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            return 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        
        return 0
    
    def get_stats(self) -> dict:
        """Retourne les statistiques de performance"""
        if not self.frame_times:
            return {"fps": 0, "avg_frame_time": 0, "min_frame_time": 0, "max_frame_time": 0}
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        
        return {
            "fps": fps,
            "avg_frame_time": avg_frame_time * 1000,  # en ms
            "min_frame_time": min(self.frame_times) * 1000,  # en ms
            "max_frame_time": max(self.frame_times) * 1000,  # en ms
        }

class ColorPalette:
    """Palette de couleurs pour l'interface"""
    
    # Couleurs principales
    PRIMARY = (66, 165, 245)      # Bleu
    SECONDARY = (156, 39, 176)    # Violet
    SUCCESS = (76, 175, 80)       # Vert
    WARNING = (255, 152, 0)       # Orange
    ERROR = (244, 67, 54)         # Rouge
    
    # Couleurs pour les landmarks
    HAND_LANDMARKS = (255, 0, 0)     # Bleu pour les points
    HAND_CONNECTIONS = (0, 255, 0)   # Vert pour les connexions
    
    # Couleurs pour les gestes
    GESTURE_COLORS = {
        "fist": (0, 0, 255),          # Rouge
        "open_hand": (0, 255, 0),     # Vert
        "point": (255, 0, 0),         # Bleu
        "ok": (0, 255, 255),          # Cyan
        "two": (255, 255, 0),         # Jaune
        "three": (255, 0, 255),       # Magenta
        "four": (128, 0, 128),        # Violet
        "unknown": (128, 128, 128),   # Gris
    }
    
    @staticmethod
    def get_gesture_color(gesture_name: str) -> Tuple[int, int, int]:
        """Retourne la couleur associée à un geste"""
        return ColorPalette.GESTURE_COLORS.get(gesture_name, ColorPalette.GESTURE_COLORS["unknown"])
