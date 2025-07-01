"""
Contrôleur simplifié pour les actions de présentation - Avec gestion intelligente du diaporama
"""
import pyautogui
import time

class PresentationController:
    """Contrôleur simplifié pour les actions de présentation uniquement"""
    
    def __init__(self):
        # Désactiver le fail-safe de pyautogui pour éviter les interruptions
        pyautogui.FAILSAFE = False
        self.last_gesture_time = 0
        self.is_in_slideshow = False  # Track slideshow state
        
    def execute_gesture_action(self, gesture: str, cooldown: float = 1.0):
        """Exécute l'action correspondant au geste détecté"""
        current_time = time.time()
        
        # Vérifier le cooldown
        if current_time - self.last_gesture_time < cooldown:
            return
        
        action_map = {
            "fist": self.next_slide,
            "open_hand": self.previous_slide,
            "three": self.smart_slideshow_toggle,  # Smart toggle instead of F5
            "two": lambda: self.go_to_slide(2),
            "four": lambda: self.go_to_slide(4),
        }
        
        if gesture in action_map:
            action_map[gesture]()
            self.last_gesture_time = current_time
            print(f"Geste exécuté: {gesture}")
    
    def next_slide(self):
        """Passer à la slide suivante"""
        pyautogui.press('right')
        print("→ Slide suivante")
    
    def previous_slide(self):
        """Revenir à la slide précédente"""
        pyautogui.press('left')
        print("← Slide précédente")
    
    def smart_slideshow_toggle(self):
        """Gestion intelligente du diaporama - démarre ou quitte selon le contexte"""
        if not self.is_in_slideshow:
            # Démarrer le diaporama
            pyautogui.press('f5')
            self.is_in_slideshow = True
            print("🎥 Démarrage du diaporama")
        else:
            # Quitter le diaporama
            pyautogui.press('escape')
            self.is_in_slideshow = False
            print("🚪 Sortie du diaporama")
    
    def force_start_slideshow(self):
        """Force le démarrage du diaporama"""
        pyautogui.press('f5')
        self.is_in_slideshow = True
        print("🎥 Diaporama forcé")
    
    def force_exit_slideshow(self):
        """Force la sortie du diaporama"""
        pyautogui.press('escape')
        self.is_in_slideshow = False
        print("🚪 Sortie forcée du diaporama")
    
    def go_to_slide(self, slide_number: int):
        """Aller à une slide spécifique"""
        if self.is_in_slideshow:
            # En mode diaporama, utiliser les numéros + Enter
            pyautogui.press(str(slide_number))
            pyautogui.press('enter')
        else:
            # En mode édition, utiliser Ctrl+G (PowerPoint "Go to slide")
            pyautogui.hotkey('ctrl', 'g')
            time.sleep(0.2)
            pyautogui.type(str(slide_number))
            pyautogui.press('enter')
        print(f"📄 Slide {slide_number}")
    
    def toggle_fullscreen_only(self):
        """Basculer uniquement le mode plein écran (F5 simple)"""
        pyautogui.press('f5')
        print("🖥️ Basculer plein écran")
    
    def end_slideshow(self):
        """Terminer le diaporama"""
        pyautogui.press('esc')
        self.is_in_slideshow = False
        print("⏹ Fin du diaporama")
    
    def black_screen(self):
        """Écran noir pendant la présentation"""
        if self.is_in_slideshow:
            pyautogui.press('b')
            print("⬛ Écran noir")
    
    def white_screen(self):
        """Écran blanc pendant la présentation"""
        if self.is_in_slideshow:
            pyautogui.press('w')
            print("⬜ Écran blanc")
    
    def reset_slideshow_state(self):
        """Remet à zéro l'état du diaporama (utile en cas de désynchronisation)"""
        self.is_in_slideshow = False
        print("🔄 État du diaporama réinitialisé")