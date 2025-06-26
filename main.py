"""
Point d'entrée principal pour le contrôleur gestuel moderne
Avec support des thèmes et interface avancée
"""
import sys
import os
from tkinter import messagebox

# Ajouter le dossier imagerie au path si nécessaire
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from gui import ModernGestureControllerGUI
    from themes import ThemeManager, NotificationManager
except ImportError:
    # Si l'import échoue, essayer depuis le dossier imagerie
    imagerie_path = os.path.join(os.path.dirname(__file__), '.')
    sys.path.insert(0, imagerie_path)
    from gui import ModernGestureControllerGUI
    from themes import ThemeManager, NotificationManager

def print_banner():
    """Affiche une bannière stylée"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🎯  CONTRÔLEUR GESTUEL AVANCÉ  🎯                         ║
    ║                                                              ║
    ║    ✨ Intelligence Artificielle                              ║
    ║    🎮 Vision par Ordinateur                                  ║
    ║    🚀 Interface Moderne                                      ║
    ║    🎨 Thèmes Personnalisables                                ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    required_modules = [
        'cv2', 'mediapipe', 'pyautogui', 'numpy', 'tkinter'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Modules manquants: {', '.join(missing_modules)}")
        print("📦 Installez-les avec: pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def main():
    """Fonction principale améliorée"""
    print_banner()
    
    # Vérification des dépendances
    if not check_dependencies():
        input("Appuyez sur Entrée pour quitter...")
        return
    
    print("\n🔧 Configuration:")
    print("- Webcam requise et fonctionnelle")
    print("- Présentation ouverte (PowerPoint, PDF, etc.)")
    print("- Éclairage suffisant pour la détection")
    
    print("\n📋 Instructions:")
    print("1. Cliquez sur '▶ Démarrer' dans l'interface")
    print("2. Utilisez les gestes devant la caméra")
    print("3. Consultez le guide des gestes dans l'interface")
    print("4. Appuyez sur 'q' dans la fenêtre vidéo pour quitter")
    
    print("\n🎨 Fonctionnalités modernes:")
    print("- Interface graphique redesignée")
    print("- Visualisation des gestes en temps réel")
    print("- Statistiques de performance")
    print("- Configuration avancée")
    print("- Thèmes personnalisables")
    
    print("\n" + "="*60)
    print("🚀 Lancement de l'application...")
    
    try:
        # Initialisation du gestionnaire de thèmes
        theme_manager = ThemeManager()
        
        # Lancement de l'application
        app = ModernGestureControllerGUI()
        
        # Notification de bienvenue
        notification_manager = NotificationManager(app.root)
        app.root.after(1000, lambda: notification_manager.show_notification(
            "🎯 Contrôleur Gestuel Prêt!\nUtilisez les gestes pour contrôler vos présentations.", 
            "success", 4000
        ))
        
        app.run()
        
    except KeyboardInterrupt:
        print("\n⚠️  Arrêt du programme par l'utilisateur...")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite: {str(e)}")
        print("\n🔍 Vérifiez:")
        print("- Que votre caméra fonctionne")
        print("- Que toutes les dépendances sont installées")
        print("- Que vous avez les permissions nécessaires")

if __name__ == "__main__":
    main()
