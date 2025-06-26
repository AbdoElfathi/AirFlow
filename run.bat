@echo off
echo ===========================================
echo    Contrôleur Gestuel pour Présentations
echo ===========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo Python détecté...

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
python -c "import cv2, mediapipe, pyautogui, numpy, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dépendances
        pause
        exit /b 1
    )
)

echo Toutes les dépendances sont installées.
echo.

REM Lancer l'application
echo Lancement de l'application...
python main_new.py

pause
