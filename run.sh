#!/bin/bash

echo "==========================================="
echo "   Contrôleur Gestuel pour Présentations"
echo "==========================================="
echo

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python3 n'est pas installé"
    echo "Veuillez installer Python depuis https://python.org"
    exit 1
fi

echo "Python détecté..."

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
python3 -c "import cv2, mediapipe, pyautogui, numpy, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERREUR: Impossible d'installer les dépendances"
        exit 1
    fi
fi

echo "Toutes les dépendances sont installées."
echo

# Lancer l'application
echo "Lancement de l'application..."
python3 main_new.py
