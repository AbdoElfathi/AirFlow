"""
Contrôleur simplifié pour les actions de présentation - Sans pointeur laser
"""
import pyautogui
import time

class PresentationController:
    """Contrôleur simplifié pour les actions de présentation uniquement"""
    
    def __init__(self):
        # Désactiver le fail-safe de pyautogui pour éviter les interruptions
        pyautogui.FAILSAFE = False
        self.last_gesture_time = 0
        
    def execute_gesture_action(self, gesture: str, cooldown: float = 1.0):
        """Exécute l'action correspondant au geste détecté"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < cooldown:
            return
        
        action_map = {
            "fist": self.next_slide,
            "open_hand": self.previous_slide,
            "point": self.next_slide,  # Index pointer now goes to next slide
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
