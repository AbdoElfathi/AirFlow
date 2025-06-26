"""
Configuration pour le contrôleur gestuel
"""
from dataclasses import dataclass
from typing import Tuple

@dataclass
class GestureConfig:
    """Configuration des gestes et de leur sensibilité"""
    min_detection_confidence: float = 0.7
    min_tracking_confidence: float = 0.5
    gesture_cooldown: float = 1.0  # Délai entre gestes (secondes)
    distance_threshold: float = 0.15  # Distance minimum pour activer
    laser_pointer_color: Tuple[int, int, int] = (0, 0, 255)  # Rouge
    laser_pointer_radius: int = 10
