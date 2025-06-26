"""
Script de test pour vérifier l'installation et la nouvelle interface
"""
import sys
import os

def test_imports():
    """Teste tous les imports nécessaires"""
    print("🔍 Test des imports...")
    
    modules_to_test = [
        ('cv2', 'OpenCV'),
        ('mediapipe', 'MediaPipe'),
        ('pyautogui', 'PyAutoGUI'),
        ('numpy', 'NumPy'),
        ('tkinter', 'Tkinter'),
    ]
    
    all_good = True
    
    for module, name in modules_to_test:
        try:
            __import__(module)
            print(f"  ✅ {name} - OK")
        except ImportError:
            print(f"  ❌ {name} - MANQUANT")
            all_good = False
    
    return all_good

def test_local_modules():
    """Teste les modules locaux"""
    print("\n🔍 Test des modules locaux...")
    
    local_modules = [
        ('config', 'Configuration'),
        ('gesture_detector', 'Détecteur de gestes'),
        ('presentation_controller', 'Contrôleur de présentation'),
        ('gui', 'Interface graphique'),
        ('themes', 'Gestionnaire de thèmes'),
        ('utils', 'Utilitaires')
    ]
    
    all_good = True
    
    for module, name in local_modules:
        try:
            __import__(module)
            print(f"  ✅ {name} - OK")
        except ImportError as e:
            print(f"  ❌ {name} - ERREUR: {e}")
            all_good = False
    
    return all_good

def test_camera():
    """Teste l'accès à la caméra"""
    print("\n📹 Test de la caméra...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("  ✅ Caméra accessible et fonctionnelle")
                cap.release()
                return True
            else:
                print("  ❌ Caméra accessible mais ne retourne pas d'images")
                cap.release()
                return False
        else:
            print("  ❌ Impossible d'accéder à la caméra")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur lors du test caméra: {e}")
        return False

def test_gui_components():
    """Teste les composants de l'interface"""
    print("\n🖥️ Test des composants GUI...")
    
    try:
        from gui import ModernGestureControllerGUI, ModernButton, GestureVisualizer
        from themes import ThemeManager, NotificationManager
        
        print("  ✅ Classes principales - OK")
        
        # Test basique de création des objets
        theme_manager = ThemeManager()
        themes = theme_manager.get_available_themes()
        print(f"  ✅ Thèmes disponibles: {', '.join(themes)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur composants GUI: {e}")
        return False

def run_quick_demo():
    """Lance une démonstration rapide"""
    print("\n🚀 Lancement de la démonstration rapide...")
    
    try:
        from demo_components import DemoWindow
        
        print("  📝 Instructions:")
        print("  - Une fenêtre de démonstration va s'ouvrir")
        print("  - Testez les différents composants")
        print("  - Fermez la fenêtre pour continuer")
        
        input("  Appuyez sur Entrée pour lancer la démo...")
        
        demo = DemoWindow()
        demo.run()
        
        print("  ✅ Démonstration terminée")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur démonstration: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 SCRIPT DE TEST - CONTRÔLEUR GESTUEL MODERNE")
    print("=" * 60)
    
    # Tests séquentiels
    tests = [
        ("Imports des dépendances", test_imports),
        ("Modules locaux", test_local_modules),
        ("Accès caméra", test_camera),
        ("Composants GUI", test_gui_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 30)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("\n🚀 Votre installation est prête!")
        print("Vous pouvez maintenant lancer:")
        print("  python main_new.py")
        
        # Proposer la démonstration
        response = input("\n❓ Voulez-vous voir la démonstration des composants? (o/n): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            run_quick_demo()
            
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n🔧 Actions recommandées:")
        print("1. Vérifiez l'installation des dépendances:")
        print("   pip install -r requirements.txt")
        print("2. Vérifiez que votre caméra fonctionne")
        print("3. Relancez ce script de test")
    
    print("\n📖 Pour plus d'aide, consultez le README.md")

if __name__ == "__main__":
    main()
