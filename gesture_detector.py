"""
Détecteur de gestes basé sur MediaPipe
"""
import cv2
import mediapipe as mp
import math
from typing import List, Optional
from config import GestureConfig

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
