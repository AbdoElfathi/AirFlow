"""
Thèmes et styles supplémentaires pour l'interface moderne
"""
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Gestionnaire de thèmes pour l'interface"""
    
    def __init__(self):
        self.themes = {
            'default': {
                'primary': '#2C3E50',
                'secondary': '#3498DB', 
                'success': '#2ECC71',
                'warning': '#F39C12',
                'danger': '#E74C3C',
                'light': '#ECF0F1',
                'dark': '#34495E',
                'accent': '#9B59B6'
            },
            'dark': {
                'primary': '#1E1E1E',
                'secondary': '#007ACC', 
                'success': '#4EC9B0',
                'warning': '#FFCC00',
                'danger': '#F44747',
                'light': '#2D2D30',
                'dark': '#252526',
                'accent': '#C586C0'
            },
            'neon': {
                'primary': '#0D1117',
                'secondary': '#58A6FF', 
                'success': '#39D353',
                'warning': '#FFDF5D',
                'danger': '#FF6B6B',
                'light': '#161B22',
                'dark': '#21262D',
                'accent': '#D2A8FF'
            },
            'ocean': {
                'primary': '#003366',
                'secondary': '#0099CC', 
                'success': '#00CC99',
                'warning': '#FF9900',
                'danger': '#FF6666',
                'light': '#E6F3FF',
                'dark': '#004080',
                'accent': '#6600CC'
            }
        }
        
        self.current_theme = 'default'
    
    def get_theme(self, theme_name=None):
        """Retourne un thème spécifique ou le thème actuel"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes['default'])
    
    def set_theme(self, theme_name):
        """Change le thème actuel"""
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_available_themes(self):
        """Retourne la liste des thèmes disponibles"""
        return list(self.themes.keys())

class GradientFrame(tk.Canvas):
    """Frame avec fond en gradient"""
    
    def __init__(self, parent, color1, color2, direction='vertical', **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.direction = direction
        
        self.bind('<Configure>', self._on_configure)
        
    def _on_configure(self, event):
        """Redessine le gradient quand la taille change"""
        self.delete("gradient")
        self._draw_gradient()
        
    def _draw_gradient(self):
        """Dessine le gradient"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Convertir les couleurs hex en RGB
        r1, g1, b1 = self._hex_to_rgb(self.color1)
        r2, g2, b2 = self._hex_to_rgb(self.color2)
        
        if self.direction == 'vertical':
            steps = height
            for i in range(steps):
                ratio = i / steps
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.create_line(0, i, width, i, fill=color, tags="gradient")
        else:  # horizontal
            steps = width
            for i in range(steps):
                ratio = i / steps
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.create_line(i, 0, i, height, fill=color, tags="gradient")
    
    def _hex_to_rgb(self, hex_color):
        """Convertit une couleur hex en RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class AnimatedProgressBar(tk.Canvas):
    """Barre de progression animée"""
    
    def __init__(self, parent, width=300, height=20, bg_color="#E0E0E0", 
                 progress_color="#4CAF50", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        
        self.bg_color = bg_color
        self.progress_color = progress_color
        self.progress = 0
        self.animation_step = 0
        
        self.configure(bg=parent.cget('bg'))
        self.draw_progress()
        
    def set_progress(self, value):
        """Met à jour le progrès (0-100)"""
        self.progress = max(0, min(100, value))
        self.draw_progress()
        
    def start_animation(self):
        """Lance l'animation de la barre"""
        self.animate()
        
    def animate(self):
        """Animation de la barre de progression"""
        self.animation_step += 1
        self.draw_progress()
        self.after(50, self.animate)
        
    def draw_progress(self):
        """Dessine la barre de progression"""
        self.delete("all")
        
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        # Fond
        self.create_rectangle(0, 0, width, height, fill=self.bg_color, outline="")
        
        # Progression
        progress_width = (width * self.progress) // 100
        if progress_width > 0:
            self.create_rectangle(0, 0, progress_width, height, 
                                 fill=self.progress_color, outline="")
            
            # Effet de brillance animé
            shine_pos = (self.animation_step * 2) % (width + 50)
            if shine_pos < progress_width:
                self.create_rectangle(shine_pos, 0, shine_pos + 20, height, 
                                     fill="#FFFFFF40", outline="")

class ModernTooltip:
    """Tooltip moderne avec animation"""
    
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.after_id = None
        
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
        
    def on_enter(self, event):
        """Quand la souris entre dans le widget"""
        self.after_id = self.widget.after(self.delay, self.show_tooltip)
        
    def on_leave(self, event):
        """Quand la souris sort du widget"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self.hide_tooltip()
        
    def on_motion(self, event):
        """Mouvement de la souris"""
        if self.tooltip_window:
            self.update_position(event)
            
    def show_tooltip(self):
        """Affiche le tooltip"""
        if self.tooltip_window:
            return
            
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        # Style moderne
        frame = tk.Frame(self.tooltip_window, bg="#2C3E50", relief="solid", bd=1)
        frame.pack()
        
        label = tk.Label(frame, text=self.text, bg="#2C3E50", fg="white", 
                        font=("Segoe UI", 9), padx=10, pady=5)
        label.pack()
        
        # Animation d'apparition
        self.tooltip_window.attributes("-alpha", 0.0)
        self.fade_in()
        
    def fade_in(self, alpha=0.0):
        """Animation fade in"""
        if self.tooltip_window and alpha < 1.0:
            alpha += 0.1
            self.tooltip_window.attributes("-alpha", alpha)
            self.tooltip_window.after(20, lambda: self.fade_in(alpha))
            
    def hide_tooltip(self):
        """Cache le tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
            
    def update_position(self, event):
        """Met à jour la position du tooltip"""
        if self.tooltip_window:
            x = event.x_root + 25
            y = event.y_root + 25
            self.tooltip_window.wm_geometry(f"+{x}+{y}")

class NotificationManager:
    """Gestionnaire de notifications modernes"""
    
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        
    def show_notification(self, message, type="info", duration=3000):
        """Affiche une notification"""
        colors = {
            "info": "#3498DB",
            "success": "#2ECC71", 
            "warning": "#F39C12",
            "error": "#E74C3C"
        }
        
        notification = NotificationWindow(
            self.parent, message, colors.get(type, "#3498DB"), duration
        )
        
        # Positionner la notification
        y_offset = len(self.notifications) * 80
        notification.show(y_offset)
        
        self.notifications.append(notification)
        
        # Retirer après la durée spécifiée
        self.parent.after(duration, lambda: self.remove_notification(notification))
        
    def remove_notification(self, notification):
        """Retire une notification"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.hide()
            
            # Repositionner les autres notifications
            for i, notif in enumerate(self.notifications):
                notif.update_position(i * 80)

class NotificationWindow:
    """Fenêtre de notification individuelle"""
    
    def __init__(self, parent, message, color, duration):
        self.parent = parent
        self.message = message
        self.color = color
        self.duration = duration
        self.window = None
        
    def show(self, y_offset=0):
        """Affiche la notification"""
        self.window = tk.Toplevel(self.parent)
        self.window.wm_overrideredirect(True)
        
        # Position en haut à droite
        x = self.parent.winfo_rootx() + self.parent.winfo_width() - 320
        y = self.parent.winfo_rooty() + 50 + y_offset
        
        self.window.wm_geometry(f"300x60+{x}+{y}")
        
        # Style de la notification
        frame = tk.Frame(self.window, bg=self.color, padx=15, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        label = tk.Label(frame, text=self.message, bg=self.color, fg="white",
                        font=("Segoe UI", 10), wraplength=250)
        label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bouton fermer
        close_btn = tk.Button(frame, text="×", bg=self.color, fg="white",
                             font=("Segoe UI", 12, "bold"), border=0,
                             command=self.hide)
        close_btn.pack(side=tk.RIGHT)
        
        # Animation d'entrée
        self.window.attributes("-alpha", 0.0)
        self.slide_in()
        
    def slide_in(self, alpha=0.0):
        """Animation d'entrée"""
        if self.window and alpha < 0.9:
            alpha += 0.1
            self.window.attributes("-alpha", alpha)
            self.window.after(30, lambda: self.slide_in(alpha))
            
    def hide(self):
        """Cache la notification"""
        if self.window:
            self.slide_out()
            
    def slide_out(self, alpha=0.9):
        """Animation de sortie"""
        if self.window and alpha > 0.0:
            alpha -= 0.1
            self.window.attributes("-alpha", alpha)
            self.window.after(30, lambda: self.slide_out(alpha))
        elif self.window:
            self.window.destroy()
            self.window = None
            
    def update_position(self, y_offset):
        """Met à jour la position"""
        if self.window:
            x = self.parent.winfo_rootx() + self.parent.winfo_width() - 320
            y = self.parent.winfo_rooty() + 50 + y_offset
            self.window.wm_geometry(f"300x60+{x}+{y}")

class ModernIconButton(tk.Canvas):
    """Bouton avec icône moderne"""
    
    def __init__(self, parent, icon, text="", command=None, size=40, **kwargs):
        super().__init__(parent, width=size, height=size, highlightthickness=0, **kwargs)
        
        self.icon = icon
        self.text = text
        self.command = command
        self.size = size
        self.is_hovered = False
        
        self.configure(bg=parent.cget('bg'))
        self.draw_button()
        
        # Événements
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        # Tooltip si du texte est fourni
        if self.text:
            ModernTooltip(self, self.text)
            
    def draw_button(self):
        """Dessine le bouton icône"""
        self.delete("all")
        
        center = self.size // 2
        radius = (self.size - 10) // 2
        
        # Cercle de fond
        if self.is_hovered:
            self.create_oval(center-radius-2, center-radius-2, 
                           center+radius+2, center+radius+2,
                           fill="#E0E0E0", outline="")
        
        # Icône
        self.create_text(center, center, text=self.icon, 
                        font=("Segoe UI Emoji", self.size//3), fill="#2C3E50")
        
    def on_enter(self, event):
        """Effet hover"""
        self.is_hovered = True
        self.draw_button()
        
    def on_leave(self, event):
        """Fin effet hover"""
        self.is_hovered = False
        self.draw_button()
        
    def on_click(self, event):
        """Gestion du clic"""
        if self.command:
            self.command()
