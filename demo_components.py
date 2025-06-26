"""
Démonstration des composants modernes de l'interface
"""
import tkinter as tk
from tkinter import ttk
from themes import (ThemeManager, GradientFrame, AnimatedProgressBar, 
                   ModernTooltip, NotificationManager, ModernIconButton)

class DemoWindow:
    """Fenêtre de démonstration des composants modernes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Démonstration - Composants Modernes")
        self.root.geometry("800x600")
        self.root.configure(bg="#ECF0F1")
        
        self.theme_manager = ThemeManager()
        self.notification_manager = NotificationManager(self.root)
        
        self.create_demo_interface()
        
    def create_demo_interface(self):
        """Crée l'interface de démonstration"""
        # Titre
        title_frame = GradientFrame(self.root, "#2C3E50", "#3498DB", height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(title_frame, text="🎨 Démonstration des Composants Modernes", 
                              font=("Segoe UI", 20, "bold"), fg="white", bg="#2C3E50")
        title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Container principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Démonstration des thèmes
        self.create_theme_demo(main_frame)
        
        # Démonstration des boutons icônes
        self.create_icon_demo(main_frame)
        
        # Démonstration de la barre de progression
        self.create_progress_demo(main_frame)
        
        # Démonstration des notifications
        self.create_notification_demo(main_frame)
        
    def create_theme_demo(self, parent):
        """Démonstration des thèmes"""
        theme_frame = ttk.LabelFrame(parent, text="Sélecteur de Thèmes")
        theme_frame.pack(fill=tk.X, pady=10)
        
        themes = self.theme_manager.get_available_themes()
        
        for theme in themes:
            colors = self.theme_manager.get_theme(theme)
            
            # Frame pour chaque thème
            theme_item = tk.Frame(theme_frame, bg="white", relief="raised", bd=1)
            theme_item.pack(fill=tk.X, padx=10, pady=5)
            
            # Barre de couleur
            color_bar = tk.Frame(theme_item, bg=colors['primary'], height=30)
            color_bar.pack(fill=tk.X)
            
            # Nom du thème
            name_label = tk.Label(color_bar, text=theme.title(), 
                                 bg=colors['primary'], fg="white", 
                                 font=("Segoe UI", 12, "bold"))
            name_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            # Palette de couleurs
            palette_frame = tk.Frame(theme_item, bg="white")
            palette_frame.pack(fill=tk.X, padx=10, pady=5)
            
            color_keys = ['secondary', 'success', 'warning', 'danger', 'accent']
            for color_key in color_keys:
                color_square = tk.Frame(palette_frame, bg=colors[color_key], 
                                       width=30, height=20)
                color_square.pack(side=tk.LEFT, padx=2)
                
                # Tooltip avec le nom de la couleur
                ModernTooltip(color_square, f"{color_key}: {colors[color_key]}")
            
            # Bouton d'application
            apply_btn = tk.Button(palette_frame, text="Appliquer", 
                                 command=lambda t=theme: self.apply_theme(t),
                                 bg=colors['secondary'], fg="white",
                                 font=("Segoe UI", 9), border=0, padx=10)
            apply_btn.pack(side=tk.RIGHT, padx=10)
            
    def create_icon_demo(self, parent):
        """Démonstration des boutons icônes"""
        icon_frame = ttk.LabelFrame(parent, text="Boutons Icônes Modernes")
        icon_frame.pack(fill=tk.X, pady=10)
        
        button_container = tk.Frame(icon_frame, bg="#ECF0F1")
        button_container.pack(pady=20)
        
        icons = [
            ("🎮", "Contrôles", lambda: self.show_demo_notification("Contrôles activés!")),
            ("⚙️", "Paramètres", lambda: self.show_demo_notification("Paramètres ouverts!")),
            ("📊", "Statistiques", lambda: self.show_demo_notification("Statistiques affichées!")),
            ("🎨", "Thèmes", lambda: self.show_demo_notification("Thème changé!")),
            ("💾", "Sauvegarder", lambda: self.show_demo_notification("Configuration sauvegardée!")),
            ("🔄", "Actualiser", lambda: self.show_demo_notification("Interface actualisée!"))
        ]
        
        for icon, text, command in icons:
            btn = ModernIconButton(button_container, icon, text, command, size=50)
            btn.pack(side=tk.LEFT, padx=10)
            
    def create_progress_demo(self, parent):
        """Démonstration de la barre de progression"""
        progress_frame = ttk.LabelFrame(parent, text="Barre de Progression Animée")
        progress_frame.pack(fill=tk.X, pady=10)
        
        container = tk.Frame(progress_frame, bg="#ECF0F1")
        container.pack(pady=20)
        
        self.progress_bar = AnimatedProgressBar(container, width=400, height=25)
        self.progress_bar.pack(pady=10)
        
        # Contrôles
        controls = tk.Frame(container, bg="#ECF0F1")
        controls.pack()
        
        tk.Button(controls, text="0%", command=lambda: self.progress_bar.set_progress(0),
                 bg="#3498DB", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="25%", command=lambda: self.progress_bar.set_progress(25),
                 bg="#3498DB", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="50%", command=lambda: self.progress_bar.set_progress(50),
                 bg="#3498DB", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="75%", command=lambda: self.progress_bar.set_progress(75),
                 bg="#3498DB", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="100%", command=lambda: self.progress_bar.set_progress(100),
                 bg="#2ECC71", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        
        # Animation
        tk.Button(controls, text="Animer", command=self.progress_bar.start_animation,
                 bg="#9B59B6", fg="white", font=("Segoe UI", 9), border=0, padx=10).pack(side=tk.LEFT, padx=5)
        
    def create_notification_demo(self, parent):
        """Démonstration des notifications"""
        notif_frame = ttk.LabelFrame(parent, text="Système de Notifications")
        notif_frame.pack(fill=tk.X, pady=10)
        
        container = tk.Frame(notif_frame, bg="#ECF0F1")
        container.pack(pady=20)
        
        notifications = [
            ("Info", "info", "📘 Voici une notification d'information"),
            ("Succès", "success", "✅ Opération réussie avec succès!"),
            ("Attention", "warning", "⚠️ Attention: vérifiez vos paramètres"),
            ("Erreur", "error", "❌ Une erreur s'est produite")
        ]
        
        for text, type_notif, message in notifications:
            btn = tk.Button(container, text=text, 
                           command=lambda m=message, t=type_notif: self.notification_manager.show_notification(m, t),
                           bg=self.get_color_for_type(type_notif), fg="white", 
                           font=("Segoe UI", 10), border=0, padx=15, pady=5)
            btn.pack(side=tk.LEFT, padx=10)
            
    def get_color_for_type(self, notif_type):
        """Retourne la couleur selon le type de notification"""
        colors = {
            "info": "#3498DB",
            "success": "#2ECC71", 
            "warning": "#F39C12",
            "error": "#E74C3C"
        }
        return colors.get(notif_type, "#3498DB")
            
    def apply_theme(self, theme_name):
        """Applique un thème"""
        self.theme_manager.set_theme(theme_name)
        self.notification_manager.show_notification(
            f"🎨 Thème '{theme_name}' appliqué!", "success"
        )
        
    def show_demo_notification(self, message):
        """Affiche une notification de démonstration"""
        self.notification_manager.show_notification(message, "info")
        
    def run(self):
        """Lance la démonstration"""
        self.root.mainloop()

def main():
    """Lance la démonstration"""
    print("🎨 Lancement de la démonstration des composants modernes...")
    demo = DemoWindow()
    demo.run()

if __name__ == "__main__":
    main()
