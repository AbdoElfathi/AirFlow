"""
Tests unitaires pour le contrôleur gestuel
"""
import unittest
import sys
import os

# Ajouter le dossier parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import GestureConfig
from gesture_detector import GestureDetector
from presentation_controller import PresentationController

class TestGestureConfig(unittest.TestCase):
    """Tests pour la configuration"""
    
    def test_default_values(self):
        """Test des valeurs par défaut"""
        config = GestureConfig()
        self.assertEqual(config.min_detection_confidence, 0.7)
        self.assertEqual(config.min_tracking_confidence, 0.5)
        self.assertEqual(config.gesture_cooldown, 1.0)
        self.assertEqual(config.laser_pointer_color, (0, 0, 255))
        self.assertEqual(config.laser_pointer_radius, 10)
    
    def test_custom_values(self):
        """Test avec des valeurs personnalisées"""
        config = GestureConfig(
            min_detection_confidence=0.8,
            gesture_cooldown=2.0,
            laser_pointer_color=(255, 0, 0)
        )
        self.assertEqual(config.min_detection_confidence, 0.8)
        self.assertEqual(config.gesture_cooldown, 2.0)
        self.assertEqual(config.laser_pointer_color, (255, 0, 0))

class TestGestureDetector(unittest.TestCase):
    """Tests pour le détecteur de gestes"""
    
    def setUp(self):
        """Configuration pour les tests"""
        self.config = GestureConfig()
        self.detector = GestureDetector(self.config)
    
    def test_detector_initialization(self):
        """Test de l'initialisation du détecteur"""
        self.assertIsNotNone(self.detector.mp_hands)
        self.assertIsNotNone(self.detector.hands)
        self.assertIsNotNone(self.detector.mp_drawing)
    
    def test_calculate_distance(self):
        """Test du calcul de distance"""
        class MockPoint:
            def __init__(self, x, y):
                self.x = x
                self.y = y
        
        point1 = MockPoint(0, 0)
        point2 = MockPoint(3, 4)
        distance = self.detector.calculate_distance(point1, point2)
        self.assertEqual(distance, 5.0)  # Triangle 3-4-5
    
    def test_detect_gesture_none(self):
        """Test de détection avec landmarks vides"""
        gesture = self.detector.detect_gesture(None)
        self.assertEqual(gesture, "none")

class TestPresentationController(unittest.TestCase):
    """Tests pour le contrôleur de présentation"""
    
    def setUp(self):
        """Configuration pour les tests"""
        self.controller = PresentationController()
    
    def test_controller_initialization(self):
        """Test de l'initialisation du contrôleur"""
        self.assertEqual(self.controller.current_mode, "navigation")
        self.assertEqual(self.controller.last_gesture_time, 0)
    
    def test_toggle_laser_mode(self):
        """Test du basculement du mode laser"""
        initial_mode = self.controller.current_mode
        self.controller.toggle_laser_mode()
        self.assertNotEqual(self.controller.current_mode, initial_mode)
        
        # Basculer à nouveau
        self.controller.toggle_laser_mode()
        self.assertEqual(self.controller.current_mode, initial_mode)

class TestIntegration(unittest.TestCase):
    """Tests d'intégration"""
    
    def test_full_workflow(self):
        """Test du workflow complet"""
        # Créer les composants
        config = GestureConfig()
        detector = GestureDetector(config)
        controller = PresentationController()
        
        # Vérifier que tout fonctionne ensemble
        self.assertIsNotNone(config)
        self.assertIsNotNone(detector)
        self.assertIsNotNone(controller)
        
        # Test du changement de mode
        initial_mode = controller.current_mode
        controller.toggle_laser_mode()
        self.assertNotEqual(controller.current_mode, initial_mode)

if __name__ == '__main__':
    # Lancer les tests
    unittest.main(verbosity=2)
