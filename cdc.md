\# Cahier des Charges - Watermark Tool



\## 📋 Vue d'ensemble



\*\*Nom du projet\*\* : Watermark Tool  

\*\*Version\*\* : 1.0.0  

\*\*Type\*\* : Application desktop multi-plateforme (Windows, Linux, macOS)  

\*\*Licence\*\* : Open Source (MIT)  

\*\*Auteur\*\* : Damien Marill



\### Description



Application desktop multi-plateforme permettant de sécuriser des documents administratifs en ajoutant rapidement des filigranes (watermarks) textuels sur des fichiers images et PDF. L'outil est conçu pour protéger les documents sensibles, identifier les copies, et assurer la traçabilité des fichiers partagés. L'application propose deux modes d'utilisation distincts pour s'adapter aux différents contextes professionnels.



---



\## 🎯 Objectifs



\### Objectifs principaux



1\. \*\*Sécurisation documentaire\*\* : Protéger les documents sensibles contre la copie non autorisée

2\. \*\*Traçabilité\*\* : Identifier l'origine et le destinataire des documents partagés

3\. \*\*Conformité\*\* : Marquer les documents selon leur statut (CONFIDENTIEL, BROUILLON, COPIE, etc.)

4\. \*\*Simplicité d'utilisation\*\* : Permettre l'ajout de filigranes en quelques clics

5\. \*\*Intégration système native\*\* : S'intégrer au menu contextuel sur toutes les plateformes



\### Objectifs secondaires



1\. Multi-plateforme dès la v1.0 (Windows, Linux, macOS)

2\. Open-source et documenté pour la communauté

3\. Architecture modulaire facilitant l'évolution

4\. Support multiformat (images de documents scannés et PDF)

5\. Installation simple via installateurs natifs

6\. CI/CD complet avec builds automatisés



\### Cas d'usage typiques



\#### Entreprise

\- Marquer des documents confidentiels avant envoi externe

\- Identifier les versions BROUILLON vs FINAL

\- Tracer les documents partagés avec nom/date/service



\#### Administration publique

\- Marquer les documents officiels (ORIGINAL, COPIE, etc.)

\- Ajouter des mentions légales sur les documents

\- Protéger les documents sensibles



\#### Enseignement

\- Marquer les sujets d'examens (CONFIDENTIEL)

\- Identifier les versions corrigées

\- Protéger les supports de cours



\#### Usage personnel

\- Protéger des documents personnels (contrats, factures)

\- Marquer des copies pour archivage



---



\## 🛠️ Stack Technique



\### Langage principal

\- \*\*Python 3.11+\*\* : Langage de développement principal



\### Bibliothèques Python



\#### Interface utilisateur

\- \*\*Tkinter\*\* : Interface native Windows pour le mode rapide (simple dialog)

\- \*\*Eel\*\* : Bridge Python-HTML/CSS/JS pour l'application complète



\#### Traitement d'images

\- \*\*Pillow (PIL)\*\* : Manipulation d'images (lecture, écriture, dessin)

\- Support des formats : PNG, JPEG, JPG, BMP, GIF



\#### Traitement PDF (futur)

\- \*\*ReportLab\*\* ou \*\*PyPDF2\*\* : Manipulation de fichiers PDF

\- Ajout de filigranes textuels sur documents PDF



\#### Système

\- \*\*winreg\*\* : Modification du registre Windows (menu contextuel)

\- \*\*os / pathlib\*\* : Gestion des fichiers et chemins



\### Frontend (Application complète)



\#### Technologies web

\- \*\*HTML5\*\* : Structure de l'interface

\- \*\*CSS3\*\* : Stylisation

\- \*\*JavaScript (Vanilla)\*\* : Logique frontend et interactions



\#### Framework CSS (optionnel)

\- \*\*Tailwind CSS\*\* : Framework utility-first pour le styling rapide

\- \*\*DaisyUI\*\* (alternative) : Components pré-stylisés au-dessus de Tailwind



\### Packaging et distribution



\#### Compilation multi-plateforme

\- \*\*PyInstaller\*\* : Compilation Python → Executable natif

&nbsp; - Windows : `.exe`

&nbsp; - Linux : Binaire ELF

&nbsp; - macOS : `.app` bundle

\- Configuration : Mode `--onefile --windowed`

\- Inclusion des ressources (icons, assets web)



\#### Installation par plateforme



\##### Windows

\- \*\*Inno Setup\*\* : Création d'installateur Windows professionnel

\- Gestion automatique du registre

\- Création de raccourcis

\- Désinstallateur intégré



\##### Linux

\- \*\*AppImage\*\* : Format portable universel

\- \*\*DEB package\*\* : Pour Debian/Ubuntu

\- \*\*RPM package\*\* (optionnel) : Pour Fedora/RHEL

\- Scripts d'installation du menu contextuel (Nautilus, Dolphin)



\##### macOS

\- \*\*DMG\*\* : Image disque pour distribution

\- \*\*PKG\*\* (optionnel) : Installateur macOS

\- Signature du code (si certificat disponible)

\- Intégration Finder (Services ou Quick Actions)



\#### CI/CD avec GitHub Actions



\##### Workflow automatisé

\- \*\*Déclenchement\*\* : Push sur tags `v\*` (ex: v1.0.0)

\- \*\*Builds parallèles\*\* : Windows, Linux, macOS simultanément

\- \*\*Runners\*\* : 

&nbsp; - `windows-latest` pour Windows

&nbsp; - `ubuntu-latest` pour Linux

&nbsp; - `macos-latest` pour macOS

\- \*\*Artefacts\*\* : Upload automatique des binaires compilés

\- \*\*Release GitHub\*\* : Création automatique avec notes de version

\- \*\*Assets\*\* : Attachement des installateurs à la release



\##### Matrice de build

```yaml

strategy:

&nbsp; matrix:

&nbsp;   os: \[windows-latest, ubuntu-latest, macos-latest]

&nbsp;   python-version: \['3.11']

```



\##### Tests automatisés

\- Exécution des tests unitaires avant build

\- Validation de la compilation

\- Tests d'intégration post-build (optionnel)



\##### Versioning sémantique

\- Extraction de la version depuis le tag Git

\- Injection dans les métadonnées de l'application

\- Génération automatique du changelog



\### Environnement de développement



\#### Outils

\- \*\*Git\*\* : Gestion de versions

\- \*\*GitHub\*\* : Hébergement du code et releases

\- \*\*GitHub Actions\*\* : CI/CD pour builds multi-plateformes automatiques

&nbsp; - Workflow : `.github/workflows/build-release.yml`

&nbsp; - Runners : Windows, Linux, macOS

&nbsp; - Déclenchement automatique sur tags



\#### IDE recommandé

\- \*\*PyCharm\*\* ou \*\*VS Code\*\* : Développement Python

\- Extensions Python, HTML, CSS



\#### Environnement de test

\- \*\*Virtualenv\*\* ou \*\*venv\*\* : Isolation des dépendances

\- \*\*pytest\*\* : Framework de tests

\- Machines virtuelles ou containers pour tests multi-OS



---



\## 🏗️ Architecture Générale



\### Structure du projet



```

watermark-tool/

├── .github/

│   └── workflows/

│       ├── build-release.yml      # CI/CD multi-plateforme

│       ├── tests.yml              # Tests automatisés

│       └── lint.yml               # Qualité du code

│

├── src/                          # Code source Python

│   ├── watermark\_quick.py        # Mode rapide (clic droit)

│   ├── watermark\_app.py          # Application complète (Eel)

│   ├── watermark\_logic.py        # Logique métier partagée

│   └── installer/

│       ├── windows\_installer.py  # Installation registre Windows

│       ├── linux\_installer.py    # Installation menu Nautilus/Dolphin

│       └── macos\_installer.py    # Installation Finder Services

│

├── web/                          # Interface HTML/CSS/JS

│   ├── index.html                # Page principale

│   ├── css/

│   │   └── style.css

│   ├── js/

│   │   └── app.js

│   └── assets/

│       ├── icons/

│       └── images/

│

├── resources/                    # Ressources statiques

│   ├── windows/

│   │   └── icon.ico

│   ├── linux/

│   │   └── icon.png

│   └── macos/

│       └── icon.icns

│

├── tests/                        # Tests unitaires

│   ├── test\_watermark\_logic.py

│   ├── test\_integration.py

│   └── test\_multiplatform.py

│

├── build/                        # Scripts de build

│   ├── build\_windows.py          # Build Windows

│   ├── build\_linux.py            # Build Linux

│   ├── build\_macos.py            # Build macOS

│   ├── build\_all.py              # Build toutes plateformes

│   └── installers/

│       ├── windows.iss           # Config Inno Setup

│       ├── linux\_appimage.sh     # Script AppImage

│       ├── linux\_deb.sh          # Script DEB

│       └── macos\_dmg.sh          # Script DMG

│

├── dist/                         # Fichiers compilés (ignoré git)

│   ├── windows/

│   ├── linux/

│   └── macos/

│

├── docs/                         # Documentation

│   ├── user-guide.md

│   ├── developer-guide.md

│   └── platform-specific/

│       ├── windows.md

│       ├── linux.md

│       └── macos.md

│

├── requirements.txt              # Dépendances Python

├── README.md

├── LICENSE

├── CHANGELOG.md

└── .gitignore

```



\### Modules principaux



\#### 1. watermark\_logic.py (Cœur métier)

\- Gestion du filigranage d'images

\- Gestion du filigranage de PDF

\- Génération de previews

\- Utilitaires de traitement de fichiers



\#### 2. watermark\_quick.py (Mode rapide)

\- Interface Tkinter minimaliste

\- Récupération du fichier via argv

\- Dialog de saisie du texte

\- Appel de la logique métier

\- Notification de succès/erreur



\#### 3. watermark\_app.py (Application complète)

\- Serveur Eel (bridge Python-JS)

\- API exposée au frontend

\- Gestion multi-fichiers

\- Gestion des previews

\- Sélection de dossiers



\#### 4. installer.py

\- Modification du registre Windows

\- Installation du menu contextuel

\- Désinstallation propre



---



\## 🎨 Fonctionnalités Détaillées



\### Mode 1 : Quick Watermark (Clic droit)



\#### Déclenchement

\- Clic droit sur un fichier (image ou PDF) dans l'Explorateur Windows

\- Option "Ajouter un filigrane" dans le menu contextuel



\#### Comportement



1\. \*\*Ouverture de la fenêtre\*\*

&nbsp;  - Petite fenêtre modale (400x150px)

&nbsp;  - Style natif Windows 11

&nbsp;  - Titre : "Ajouter un filigrane"



2\. \*\*Interface\*\*

&nbsp;  - Label : "Texte du filigrane :"

&nbsp;  - Input text : Pré-rempli avec "CONFIDENTIEL"

&nbsp;  - Bouton "Annuler" : Ferme la fenêtre sans action

&nbsp;  - Bouton "Valider" : Lance le traitement

&nbsp;  - Raccourcis clavier :

&nbsp;    - `Enter` : Valider

&nbsp;    - `Escape` : Annuler



3\. \*\*Traitement\*\*

&nbsp;  - Validation du texte (non vide)

&nbsp;  - Appel de la logique métier

&nbsp;  - Création du fichier avec suffixe `\_watermarked`

&nbsp;  - Même dossier que le fichier source



4\. \*\*Retour utilisateur\*\*

&nbsp;  - Message de succès (optionnel : notification Windows)

&nbsp;  - Message d'erreur en cas de problème

&nbsp;  - Fermeture automatique en cas de succès



\#### Limitations volontaires

\- Un seul fichier à la fois

\- Pas de preview

\- Pas de personnalisation avancée

\- Position et style de filigrane par défaut



---



\### Mode 2 : Watermark Tool (Application complète)



\#### Déclenchement

\- Lancement direct de l'exécutable

\- Raccourci bureau (optionnel)

\- Menu démarrer



\#### Interface principale



\##### Zone de drag \& drop

\- \*\*Position\*\* : Haut de la fenêtre

\- \*\*Apparence\*\* : 

&nbsp; - Bordure pointillée

&nbsp; - Icône de fichier/upload

&nbsp; - Texte : "Glissez-déposez vos fichiers ici ou cliquez pour parcourir"

\- \*\*Interactions\*\* :

&nbsp; - Hover : Changement de couleur

&nbsp; - Click : Ouvre le sélecteur de fichiers natif

&nbsp; - Drag over : Highlight visuel

&nbsp; - Drop : Ajout des fichiers à la liste



\##### Liste des fichiers sélectionnés

\- \*\*Affichage\*\* : Card/Panel avec liste

\- \*\*Informations par fichier\*\* :

&nbsp; - Icône selon le type

&nbsp; - Nom du fichier complet (chemin)

&nbsp; - Possibilité de retirer individuellement (futur)

\- \*\*Compteur\*\* : "X fichier(s) sélectionné(s)"



\##### Configuration du filigrane



\###### Texte du filigrane

\- \*\*Type\*\* : Input text

\- \*\*Label\*\* : "Texte du filigrane"

\- \*\*Valeur par défaut\*\* : "CONFIDENTIEL"

\- \*\*Validation\*\* : Non vide

\- \*\*Update\*\* : Preview en temps réel



\###### Dossier de sortie

\- \*\*Type\*\* : Input readonly + bouton "Parcourir"

\- \*\*Label\*\* : "Dossier de sortie"

\- \*\*Placeholder\*\* : "Même dossier que les fichiers source"

\- \*\*Comportement\*\* :

&nbsp; - Si vide : Fichiers créés à côté des originaux

&nbsp; - Si spécifié : Tous les fichiers dans ce dossier

&nbsp; - Bouton "Parcourir" : Ouvre dialog natif de sélection



\##### Zone de preview

\- \*\*Affichage\*\* : Masquée par défaut

\- \*\*Déclenchement\*\* : Dès qu'un fichier est sélectionné

\- \*\*Contenu\*\* :

&nbsp; - Preview du premier fichier avec filigrane appliqué

&nbsp; - Image redimensionnée (max 800x600)

&nbsp; - Mise à jour en temps réel si texte modifié

\- \*\*Format\*\* : Image base64 affichée dans un `<img>`



\##### Bouton de traitement

\- \*\*Texte\*\* : "Traiter les fichiers"

\- \*\*État désactivé\*\* : Aucun fichier sélectionné

\- \*\*État actif\*\* : Au moins un fichier

\- \*\*Comportement au clic\*\* :

&nbsp; - Désactivation du bouton

&nbsp; - Texte : "Traitement en cours..."

&nbsp; - Appel de l'API Python

&nbsp; - Affichage des résultats

&nbsp; - Réactivation du bouton



\##### Zone de résultats

\- \*\*Affichage\*\* : Masquée par défaut

\- \*\*Déclenchement\*\* : Après traitement

\- \*\*Contenu\*\* :

&nbsp; - Titre : "Résultats : X/Y réussi(s)"

&nbsp; - Liste des fichiers traités :

&nbsp;   - ✓ Succès : Chemin du fichier créé

&nbsp;   - ✗ Échec : Nom du fichier + message d'erreur

&nbsp; - Codes couleur (vert/rouge)



\#### Fonctionnalités avancées (futures)



\##### Personnalisation du filigrane

\- Position : Centre, coins, personnalisée

\- Opacité : Slider 0-100%

\- Taille : Petite, Moyenne, Grande, Personnalisée

\- Police : Liste de polices système

\- Couleur : Color picker

\- Rotation : Angle en degrés



\##### Preview multi-fichiers

\- Carrousel de previews

\- Zoom sur preview

\- Comparaison avant/après



\##### Traitement par lot avancé

\- File d'attente avec progression

\- Barre de progression globale

\- Possibilité d'annuler

\- Logs détaillés



---



\## 💼 Logique Métier



\### Traitement d'images



\#### Lecture du fichier

1\. Ouverture du fichier avec Pillow

2\. Conversion en mode RGBA (transparence)

3\. Récupération des dimensions



\#### Création du filigrane



\##### Calcul de la taille

\- Taille de police = 10% de la plus petite dimension de l'image

\- Minimum : 20px

\- Maximum : 200px



\##### Création du layer de texte

1\. Création d'un layer transparent (même taille que l'image)

2\. Initialisation du contexte de dessin

3\. Chargement de la police (Arial par défaut, fallback sur police système)

4\. Calcul des dimensions du texte (bounding box)



\##### Positionnement (mode par défaut : centré)

\- Position X = (Largeur image - Largeur texte) / 2

\- Position Y = (Hauteur image - Hauteur texte) / 2



\##### Rendu du texte

\- Couleur : Blanc (255, 255, 255)

\- Opacité : 50% (128 sur 255)

\- Style : Remplissage simple (pas de contour)



\#### Composition finale

1\. Fusion du layer de texte avec l'image originale (alpha compositing)

2\. Conversion en RGB (suppression du canal alpha pour JPG)

3\. Génération du nom de fichier de sortie



\#### Sauvegarde

\- \*\*Nom de fichier\*\* :

&nbsp; - Mode quick : `{nom\_original}\_watermarked{extension}`

&nbsp; - Mode app : Selon configuration utilisateur

\- \*\*Dossier\*\* :

&nbsp; - Par défaut : Même que l'original

&nbsp; - Optionnel : Dossier spécifié par l'utilisateur

\- \*\*Format\*\* : Conservation du format original



\#### Gestion d'erreurs

\- Fichier non lisible → Exception avec message clair

\- Format non supporté → Exception avec liste des formats supportés

\- Erreur d'écriture → Exception (permissions, espace disque)

\- Police non trouvée → Fallback sur police par défaut



---



\### Traitement de PDF (spécification future)



\#### Approche

\- Utilisation de ReportLab ou PyPDF2

\- Ajout d'un layer de texte sur chaque page

\- Conservation de la structure du document



\#### Spécificités PDF

\- Filigrane sur toutes les pages

\- Respect de l'orientation des pages

\- Conservation des métadonnées

\- Gestion des PDF protégés (lecture seule)



---



\### Génération de preview



\#### Objectif

Afficher un aperçu du résultat sans créer le fichier



\#### Processus

1\. Copie de l'image originale en mémoire

2\. Redimensionnement à 800x600 (thumbnail)

3\. Application du filigrane sur la miniature

4\. Conversion en base64

5\. Retour de la chaîne base64 au frontend



\#### Optimisations

\- Mise en cache de la preview si le texte ne change pas

\- Traitement asynchrone pour ne pas bloquer l'UI

\- Compression de la preview (qualité 85%)



---



\### Intégration multi-plateforme



\#### Windows



\##### Menu contextuel

\- \*\*Clé\*\* : `HKEY\_CLASSES\_ROOT\\\*\\shell\\WatermarkTool`

\- \*\*Valeur par défaut\*\* : "Ajouter un filigrane"

\- \*\*Icône\*\* : Chemin vers l'exécutable

\- \*\*Commande\*\* : `HKEY\_CLASSES\_ROOT\\\*\\shell\\WatermarkTool\\command`

&nbsp; - Valeur : `"{chemin\_exe}" "%1"`



\##### Installation

\- Script Python utilisant `winreg`

\- Exécution au premier lancement (ou via installateur)

\- Vérification des permissions admin



\##### Désinstallation

\- Suppression propre des clés de registre

\- Inclus dans le désinstallateur



\#### Linux



\##### Menu contextuel Nautilus (GNOME)

\- \*\*Emplacement\*\* : `~/.local/share/nautilus/scripts/`

\- \*\*Fichier\*\* : `watermark-tool.sh`

\- \*\*Permissions\*\* : Exécutable (`chmod +x`)

\- \*\*Comportement\*\* : 

&nbsp; - Récupère les fichiers sélectionnés via `NAUTILUS\_SCRIPT\_SELECTED\_FILE\_PATHS`

&nbsp; - Lance l'application avec les fichiers en paramètres



\##### Menu contextuel Dolphin (KDE)

\- \*\*Emplacement\*\* : `~/.local/share/kservices5/ServiceMenus/`

\- \*\*Fichier\*\* : `watermark-tool.desktop`

\- \*\*Format\*\* : Desktop Entry

\- \*\*Actions\*\* : Quick et App modes



\##### Installation

\- Script shell d'installation

\- Détection automatique de l'environnement (GNOME/KDE/autre)

\- Copie des scripts dans les bons emplacements



\##### Désinstallation

\- Suppression des scripts

\- Nettoyage des fichiers de service



\#### macOS



\##### Finder Services (Quick Actions)

\- \*\*Emplacement\*\* : `~/Library/Services/`

\- \*\*Fichier\*\* : `WatermarkTool.workflow`

\- \*\*Type\*\* : Automator workflow

\- \*\*Comportement\*\* :

&nbsp; - Service disponible dans le menu contextuel Finder

&nbsp; - Récupère les fichiers sélectionnés

&nbsp; - Lance l'application



\##### Alternative : Applescript

\- Script AppleScript pour intégration native

\- Ajout au menu contextuel via Automator



\##### Installation

\- Script d'installation automatique

\- Création du workflow Automator

\- Configuration des permissions



\##### Désinstallation

\- Suppression du workflow

\- Nettoyage des préférences



---



\## 📦 Packaging et Distribution



\### Compilation avec PyInstaller



\#### Configuration Windows

\- \*\*Nom\*\* : 

&nbsp; - `WatermarkQuick.exe` (mode rapide)

&nbsp; - `WatermarkTool.exe` (application complète)

\- \*\*Options\*\* :

&nbsp; - `--onefile` : Exécutable unique

&nbsp; - `--windowed` : Sans console

&nbsp; - `--icon=resources/windows/icon.ico`

&nbsp; - `--add-data=web;web` (app complète uniquement)

\- \*\*Taille approximative\*\* : 

&nbsp; - Quick : 15-20 MB

&nbsp; - App : 25-30 MB



\#### Configuration Linux

\- \*\*Nom\*\* : 

&nbsp; - `watermark-quick` (mode rapide)

&nbsp; - `watermark-tool` (application complète)

\- \*\*Options\*\* :

&nbsp; - `--onefile`

&nbsp; - `--windowed`

&nbsp; - `--icon=resources/linux/icon.png`

&nbsp; - `--add-data=web:web` (notation Linux)

\- \*\*Formats de distribution\*\* :

&nbsp; - \*\*AppImage\*\* : Portable, fonctionne sur toutes distributions

&nbsp; - \*\*DEB\*\* : Pour Debian, Ubuntu, Mint, etc.

&nbsp; - \*\*RPM\*\* (optionnel) : Pour Fedora, RHEL, CentOS

\- \*\*Taille approximative\*\* : 

&nbsp; - Quick : 20-25 MB

&nbsp; - App : 30-35 MB



\#### Configuration macOS

\- \*\*Nom\*\* : 

&nbsp; - `WatermarkQuick.app` (mode rapide)

&nbsp; - `WatermarkTool.app` (application complète)

\- \*\*Options\*\* :

&nbsp; - `--onefile`

&nbsp; - `--windowed`

&nbsp; - `--icon=resources/macos/icon.icns`

&nbsp; - `--add-data=web:web`

&nbsp; - `--osx-bundle-identifier=com.damienmarill.watermarktool`

\- \*\*Formats de distribution\*\* :

&nbsp; - \*\*DMG\*\* : Image disque standard macOS

&nbsp; - \*\*PKG\*\* (optionnel) : Installateur macOS

\- \*\*Taille approximative\*\* : 

&nbsp; - Quick : 25-30 MB

&nbsp; - App : 35-40 MB

\- \*\*Signature\*\* : Code signing si certificat Apple Developer disponible



\### Installateurs par plateforme



\#### Windows : Inno Setup



\*\*Fonctionnalités\*\* :

1\. \*\*Installation\*\*

&nbsp;  - Sélection du répertoire (`Program Files`)

&nbsp;  - Copie des fichiers

&nbsp;  - Modification du registre (menu contextuel)

&nbsp;  - Création des raccourcis (bureau, menu démarrer)

&nbsp;  - Vérification des droits admin



2\. \*\*Configuration\*\*

&nbsp;  - Sélection des composants :

&nbsp;    - Application complète (obligatoire)

&nbsp;    - Intégration menu contextuel (recommandé)

&nbsp;    - Mode rapide (optionnel)

&nbsp;    - Raccourci bureau (optionnel)



3\. \*\*Désinstallation\*\*

&nbsp;  - Suppression des fichiers

&nbsp;  - Nettoyage du registre

&nbsp;  - Suppression des raccourcis

&nbsp;  - Conservation des fichiers utilisateur



\*\*Fichier de sortie\*\* :

\- \*\*Nom\*\* : `WatermarkTool-Setup-v1.0.0-windows.exe`

\- \*\*Taille\*\* : ~30-35 MB

\- \*\*Architecture\*\* : x64



\#### Linux : Multiples formats



\##### AppImage

\*\*Avantages\*\* :

\- Portable (aucune installation)

\- Fonctionne sur toutes distributions

\- Pas de droits admin requis



\*\*Fichier de sortie\*\* :

\- \*\*Nom\*\* : `WatermarkTool-v1.0.0-x86\_64.AppImage`

\- \*\*Taille\*\* : ~35-40 MB

\- \*\*Exécution\*\* : `chmod +x` puis double-clic



\##### Package DEB

\*\*Avantages\*\* :

\- Installation système standard

\- Gestion des dépendances

\- Intégration native Ubuntu/Debian



\*\*Fichier de sortie\*\* :

\- \*\*Nom\*\* : `watermark-tool\_1.0.0\_amd64.deb`

\- \*\*Taille\*\* : ~30-35 MB

\- \*\*Installation\*\* : `sudo dpkg -i` ou double-clic



\##### Package RPM (optionnel)

\*\*Fichier de sortie\*\* :

\- \*\*Nom\*\* : `watermark-tool-1.0.0-1.x86\_64.rpm`

\- \*\*Installation\*\* : `sudo rpm -i` ou gestionnaire de paquets



\#### macOS : DMG



\*\*Fonctionnalités\*\* :

\- Image disque avec application

\- Interface drag-and-drop (glisser vers Applications)

\- README/License inclus

\- Background personnalisé (optionnel)



\*\*Fichier de sortie\*\* :

\- \*\*Nom\*\* : `WatermarkTool-v1.0.0-macos.dmg`

\- \*\*Taille\*\* : ~40-45 MB

\- \*\*Architecture\*\* : x86\_64 (Intel) ou arm64 (Apple Silicon) ou Universal



\*\*Installation\*\* :

1\. Monter le DMG (double-clic)

2\. Glisser l'app vers Applications

3\. Premier lancement : autoriser dans Préférences Système



\### Automatisation CI/CD avec GitHub Actions



\#### Workflow principal : `.github/workflows/build-release.yml`



\##### Déclenchement

```yaml

on:

&nbsp; push:

&nbsp;   tags:

&nbsp;     - 'v\*.\*.\*'  # Ex: v1.0.0, v1.2.3

```



\##### Jobs parallèles



\*\*Job 1 : Build Windows\*\*

\- Runner : `windows-latest`

\- Python : 3.11

\- Steps :

&nbsp; 1. Checkout du code

&nbsp; 2. Installation de Python et dépendances

&nbsp; 3. Exécution des tests

&nbsp; 4. Build avec PyInstaller

&nbsp; 5. Création de l'installateur Inno Setup

&nbsp; 6. Upload des artefacts



\*\*Job 2 : Build Linux\*\*

\- Runner : `ubuntu-latest`

\- Python : 3.11

\- Steps :

&nbsp; 1. Checkout du code

&nbsp; 2. Installation de Python et dépendances

&nbsp; 3. Exécution des tests

&nbsp; 4. Build avec PyInstaller

&nbsp; 5. Création AppImage, DEB (et RPM optionnel)

&nbsp; 6. Upload des artefacts



\*\*Job 3 : Build macOS\*\*

\- Runner : `macos-latest`

\- Python : 3.11

\- Steps :

&nbsp; 1. Checkout du code

&nbsp; 2. Installation de Python et dépendances

&nbsp; 3. Exécution des tests

&nbsp; 4. Build avec PyInstaller

&nbsp; 5. Création DMG

&nbsp; 6. Code signing (si certificat configuré dans secrets)

&nbsp; 7. Upload des artefacts



\##### Job final : Release



\*\*Dépendances\*\* : Attend la fin des 3 jobs de build



\*\*Actions\*\* :

1\. Récupération de tous les artefacts

2\. Extraction de la version depuis le tag Git

3\. Génération du changelog (depuis CHANGELOG.md ou commits)

4\. Création de la GitHub Release

5\. Attachement des binaires :

&nbsp;  - Windows : `.exe` installateur

&nbsp;  - Linux : `.AppImage`, `.deb` (et `.rpm`)

&nbsp;  - macOS : `.dmg`

6\. Publication de la release (draft → published)



\##### Stratégie de matrice (alternative)



```yaml

strategy:

&nbsp; matrix:

&nbsp;   os: \[windows-latest, ubuntu-latest, macos-latest]

&nbsp;   include:

&nbsp;     - os: windows-latest

&nbsp;       artifact\_name: windows

&nbsp;       installer\_ext: exe

&nbsp;     - os: ubuntu-latest

&nbsp;       artifact\_name: linux

&nbsp;       installer\_ext: AppImage

&nbsp;     - os: macos-latest

&nbsp;       artifact\_name: macos

&nbsp;       installer\_ext: dmg

```



\#### Workflow secondaire : Tests automatisés



\*\*Fichier\*\* : `.github/workflows/tests.yml`



\*\*Déclenchement\*\* :

\- Push sur `main` et `dev`

\- Pull requests



\*\*Contenu\*\* :

\- Exécution des tests unitaires

\- Vérification du linting

\- Calcul du coverage

\- Rapport de tests



\#### Secrets GitHub nécessaires



\- `APPLE\_DEVELOPER\_CERTIFICATE` : Certificat macOS (optionnel)

\- `APPLE\_DEVELOPER\_PASSWORD` : Mot de passe certificat (optionnel)

\- `INNO\_SETUP\_COMPILER` : Chemin Inno Setup (si non standard)



\### Versioning sémantique



\#### Format

\- \*\*MAJOR.MINOR.PATCH\*\* (ex: 1.0.0)

\- \*\*MAJOR\*\* : Breaking changes

\- \*\*MINOR\*\* : Nouvelles fonctionnalités (rétrocompatibles)

\- \*\*PATCH\*\* : Corrections de bugs



\#### Process

1\. Mise à jour de `VERSION` dans le code

2\. Mise à jour du `CHANGELOG.md`

3\. Commit : `chore: bump version to X.Y.Z`

4\. Tag Git : `git tag vX.Y.Z`

5\. Push : `git push \&\& git push --tags`

6\. GitHub Actions déclenché automatiquement

7\. Release créée avec tous les binaires



---



\## 🧪 Tests et Qualité



\### Tests unitaires



\#### watermark\_logic.py

\- Test de création de filigrane sur différents formats

\- Test de gestion d'erreurs (fichier invalide, permissions)

\- Test de génération de preview

\- Test de nommage des fichiers



\#### watermark\_quick.py

\- Test de parsing des arguments

\- Test de validation du texte

\- Test de création de fichier



\#### watermark\_app.py

\- Test des endpoints Eel

\- Test de traitement multi-fichiers

\- Test de sélection de dossier



\### Tests d'intégration

\- Test de l'installation du menu contextuel

\- Test du workflow complet quick mode

\- Test du workflow complet app mode

\- Test de la désinstallation



\### Tests utilisateurs

\- Installation sur différentes versions de Windows (10, 11)

\- Test avec différents formats d'images

\- Test avec gros volumes de fichiers

\- Test des cas limites (noms de fichiers spéciaux, caractères Unicode)



---



\## 📅 Planning de Développement



\### Phase 1 : MVP Multi-plateforme (4 semaines)



\#### Semaine 1 : Core et logique métier

\- Setup du projet et structure multi-plateforme

\- Implémentation de `watermark\_logic.py` (images)

\- Gestion multi-OS (chemins, polices)

\- Tests unitaires du core



\#### Semaine 2 : Interfaces utilisateur

\- Développement du mode quick (Tkinter)

&nbsp; - Version Windows

&nbsp; - Adaptation Linux (GTK)

&nbsp; - Adaptation macOS (native)

\- Développement de l'interface web (HTML/CSS/JS)

\- Intégration Eel



\#### Semaine 3 : Intégration système

\- Intégration menu contextuel Windows (registre)

\- Intégration Linux (Nautilus/Dolphin scripts)

\- Intégration macOS (Finder Services)

\- Tests d'intégration par plateforme



\#### Semaine 4 : Packaging et CI/CD

\- Scripts de build PyInstaller (3 plateformes)

\- Création des installateurs :

&nbsp; - Inno Setup (Windows)

&nbsp; - AppImage + DEB (Linux)

&nbsp; - DMG (macOS)

\- Configuration GitHub Actions

\- Tests complets multi-plateformes

\- Documentation d'installation



\### Phase 2 : Support PDF et amélioration (2 semaines)



\#### Semaine 5 : PDF et optimisations

\- Support PDF (ReportLab ou PyPDF)

\- Amélioration de l'UI (animations, feedback)

\- Optimisations performances multi-plateformes

\- Tests sur différentes distributions Linux



\#### Semaine 6 : Documentation et release

\- Documentation utilisateur (3 plateformes)

\- Documentation développeur

\- Guide de contribution

\- Préparation release v1.0.0

\- Tests finaux



\### Phase 3 : Templates et sécurité (2-3 semaines)



\#### Semaine 7-8 : Templates administratifs

\- Templates prédéfinis (CONFIDENTIEL, BROUILLON, etc.)

\- Ajout métadonnées (nom, date, service)

\- Personnalisation avancée (opacité, rotation)

\- Interface de gestion des templates



\#### Semaine 9 : Fonctionnalités entreprise (optionnel)

\- Logo + texte

\- Historique d'utilisation

\- Export/Import configurations



\### Jalons importants



\- \*\*Fin Semaine 1\*\* : Core fonctionnel et testé

\- \*\*Fin Semaine 2\*\* : Interfaces complètes (mode rapide + app)

\- \*\*Fin Semaine 3\*\* : Intégration système sur les 3 plateformes

\- \*\*Fin Semaine 4\*\* : CI/CD opérationnel, première release candidate

\- \*\*Fin Semaine 6\*\* : Release v1.0.0 publique



---



\## 🎓 Aspect Pédagogique



\### Utilisation en enseignement (IUT MMI)



\#### Concepts abordés

1\. \*\*Développement Python\*\* :

&nbsp;  - Programmation orientée objet

&nbsp;  - Manipulation de fichiers

&nbsp;  - Gestion d'erreurs



2\. \*\*Interface utilisateur\*\* :

&nbsp;  - GUI native (Tkinter)

&nbsp;  - Interface web moderne (HTML/CSS/JS)

&nbsp;  - Bridge Python-JavaScript (Eel)



3\. \*\*Intégration système\*\* :

&nbsp;  - Registre Windows

&nbsp;  - Menu contextuel

&nbsp;  - Packaging d'applications



4\. \*\*Traitement d'images\*\* :

&nbsp;  - Bibliothèque Pillow

&nbsp;  - Manipulation de pixels

&nbsp;  - Formats d'images



5\. \*\*Gestion de projet\*\* :

&nbsp;  - Git et GitHub

&nbsp;  - Documentation

&nbsp;  - Tests

&nbsp;  - CI/CD



\#### Exercices possibles

\- \*\*Phase 1\*\* : Implémenter la logique de base (watermark simple)

\- \*\*Phase 2\*\* : Créer l'interface web avec preview

\- \*\*Phase 3\*\* : Ajouter des fonctionnalités (position, couleur)

\- \*\*Phase 4\*\* : Créer le système de build et distribution



\#### Projet fil rouge

\- Groupe de 3-4 étudiants

\- 6 semaines de développement

\- Livrable : Application fonctionnelle + documentation

\- Présentation finale du projet



---



\## 📖 Livrables



\### Code source

\- Repository GitHub public

\- Code source Python commenté

\- Interface web (HTML/CSS/JS)

\- Scripts de build



\### Documentation



\#### Utilisateur

\- README.md avec guide d'installation

\- Guide d'utilisation (quick + app)

\- FAQ

\- Screenshots



\#### Développeur

\- Architecture technique

\- Guide de contribution

\- Documentation de l'API interne

\- Processus de build



\### Binaires (par plateforme)



\#### Windows

\- `WatermarkQuick.exe` (mode rapide, standalone)

\- `WatermarkTool.exe` (application complète, standalone)

\- `WatermarkTool-Setup-v1.0.0-windows.exe` (installateur)



\#### Linux

\- `watermark-quick` (mode rapide, binaire)

\- `watermark-tool` (application complète, binaire)

\- `WatermarkTool-v1.0.0-x86\_64.AppImage` (portable)

\- `watermark-tool\_1.0.0\_amd64.deb` (package Debian/Ubuntu)

\- `watermark-tool-1.0.0-1.x86\_64.rpm` (package Fedora/RHEL, optionnel)



\#### macOS

\- `WatermarkQuick.app` (mode rapide, bundle)

\- `WatermarkTool.app` (application complète, bundle)

\- `WatermarkTool-v1.0.0-macos.dmg` (image disque)



\#### GitHub Release

\- Tous les binaires ci-dessus attachés à la release

\- Checksums SHA256 pour vérification

\- Notes de version (CHANGELOG)



\### Tests

\- Suite de tests unitaires

\- Tests d'intégration

\- Rapport de coverage



---



\## 🔄 CI/CD avec GitHub Actions - Spécifications détaillées



\### Architecture du workflow



\#### Fichier principal : `.github/workflows/build-release.yml`



\##### Structure

```yaml

name: Build and Release



on:

&nbsp; push:

&nbsp;   tags:

&nbsp;     - 'v\*.\*.\*'

&nbsp; workflow\_dispatch:  # Permet déclenchement manuel



env:

&nbsp; PYTHON\_VERSION: '3.11'

&nbsp; 

jobs:

&nbsp; test:

&nbsp;   # Job de tests préalable

&nbsp;   

&nbsp; build-windows:

&nbsp;   # Build Windows

&nbsp;   

&nbsp; build-linux:

&nbsp;   # Build Linux

&nbsp;   

&nbsp; build-macos:

&nbsp;   # Build macOS

&nbsp;   

&nbsp; create-release:

&nbsp;   # Création de la release GitHub

```



\##### Déclencheurs

1\. \*\*Automatique\*\* : Push sur tags `v\*.\*.\*` (ex: v1.0.0)

2\. \*\*Manuel\*\* : Via l'interface GitHub (workflow\_dispatch)



\### Job 1 : Tests (pré-requis)



\*\*Runner\*\* : `ubuntu-latest` (plus rapide pour les tests)



\*\*Étapes\*\* :

1\. Checkout du code

2\. Setup Python 3.11

3\. Installation des dépendances (`pip install -r requirements.txt`)

4\. Exécution de `pytest` avec coverage

5\. Upload du rapport de coverage (Codecov optionnel)

6\. Échec = arrêt de tous les builds



\*\*Conditions de succès\*\* :

\- Tous les tests passent

\- Coverage > 80% (warning si < 80%)



\### Job 2 : Build Windows



\*\*Runner\*\* : `windows-latest`



\*\*Dépendances\*\* : Job `test` réussi



\*\*Étapes détaillées\*\* :



1\. \*\*Checkout et setup\*\*

&nbsp;  ```yaml

&nbsp;  - uses: actions/checkout@v4

&nbsp;  - uses: actions/setup-python@v4

&nbsp;    with:

&nbsp;      python-version: '3.11'

&nbsp;  ```



2\. \*\*Installation dépendances\*\*

&nbsp;  ```yaml

&nbsp;  - name: Install dependencies

&nbsp;    run: |

&nbsp;      python -m pip install --upgrade pip

&nbsp;      pip install -r requirements.txt

&nbsp;      pip install pyinstaller

&nbsp;  ```



3\. \*\*Build mode rapide\*\*

&nbsp;  ```yaml

&nbsp;  - name: Build WatermarkQuick

&nbsp;    run: python build/build\_windows.py --quick

&nbsp;  ```



4\. \*\*Build application complète\*\*

&nbsp;  ```yaml

&nbsp;  - name: Build WatermarkTool

&nbsp;    run: python build/build\_windows.py --app

&nbsp;  ```



5\. \*\*Installation Inno Setup\*\*

&nbsp;  ```yaml

&nbsp;  - name: Setup Inno Setup

&nbsp;    run: |

&nbsp;      choco install innosetup -y

&nbsp;      echo "C:\\Program Files (x86)\\Inno Setup 6" >> $GITHUB\_PATH

&nbsp;  ```



6\. \*\*Création de l'installateur\*\*

&nbsp;  ```yaml

&nbsp;  - name: Create installer

&nbsp;    run: iscc build/installers/windows.iss

&nbsp;  ```



7\. \*\*Upload artefacts\*\*

&nbsp;  ```yaml

&nbsp;  - uses: actions/upload-artifact@v3

&nbsp;    with:

&nbsp;      name: windows-binaries

&nbsp;      path: |

&nbsp;        dist/windows/WatermarkTool-Setup-\*.exe

&nbsp;        dist/windows/checksums.txt

&nbsp;  ```



\### Job 3 : Build Linux



\*\*Runner\*\* : `ubuntu-latest`



\*\*Dépendances\*\* : Job `test` réussi



\*\*Étapes spécifiques\*\* :



1\. \*\*Installation dépendances système\*\*

&nbsp;  ```yaml

&nbsp;  - name: Install system dependencies

&nbsp;    run: |

&nbsp;      sudo apt-get update

&nbsp;      sudo apt-get install -y \\

&nbsp;        libfuse2 \\

&nbsp;        desktop-file-utils \\

&nbsp;        fakeroot \\

&nbsp;        dpkg-dev \\

&nbsp;        rpm

&nbsp;  ```



2\. \*\*Build binaires\*\*

&nbsp;  ```yaml

&nbsp;  - name: Build Linux binaries

&nbsp;    run: |

&nbsp;      python build/build\_linux.py --quick

&nbsp;      python build/build\_linux.py --app

&nbsp;  ```



3\. \*\*Création AppImage\*\*

&nbsp;  ```yaml

&nbsp;  - name: Create AppImage

&nbsp;    run: |

&nbsp;      chmod +x build/installers/linux\_appimage.sh

&nbsp;      ./build/installers/linux\_appimage.sh

&nbsp;  ```



4\. \*\*Création package DEB\*\*

&nbsp;  ```yaml

&nbsp;  - name: Create DEB package

&nbsp;    run: |

&nbsp;      chmod +x build/installers/linux\_deb.sh

&nbsp;      ./build/installers/linux\_deb.sh

&nbsp;  ```



5\. \*\*Création package RPM (optionnel)\*\*

&nbsp;  ```yaml

&nbsp;  - name: Create RPM package

&nbsp;    run: |

&nbsp;      chmod +x build/installers/linux\_rpm.sh

&nbsp;      ./build/installers/linux\_rpm.sh

&nbsp;    continue-on-error: true

&nbsp;  ```



6\. \*\*Upload artefacts\*\*

&nbsp;  ```yaml

&nbsp;  - uses: actions/upload-artifact@v3

&nbsp;    with:

&nbsp;      name: linux-binaries

&nbsp;      path: |

&nbsp;        dist/linux/\*.AppImage

&nbsp;        dist/linux/\*.deb

&nbsp;        dist/linux/\*.rpm

&nbsp;        dist/linux/checksums.txt

&nbsp;  ```



\### Job 4 : Build macOS



\*\*Runner\*\* : `macos-latest`



\*\*Dépendances\*\* : Job `test` réussi



\*\*Étapes spécifiques\*\* :



1\. \*\*Build binaires\*\*

&nbsp;  ```yaml

&nbsp;  - name: Build macOS binaries

&nbsp;    run: |

&nbsp;      python build/build\_macos.py --quick

&nbsp;      python build/build\_macos.py --app

&nbsp;  ```



2\. \*\*Code signing (si certificat disponible)\*\*

&nbsp;  ```yaml

&nbsp;  - name: Code Sign

&nbsp;    if: ${{ secrets.APPLE\_CERTIFICATE }}

&nbsp;    env:

&nbsp;      APPLE\_CERT: ${{ secrets.APPLE\_CERTIFICATE }}

&nbsp;      APPLE\_CERT\_PASSWORD: ${{ secrets.APPLE\_CERT\_PASSWORD }}

&nbsp;    run: |

&nbsp;      echo "$APPLE\_CERT" | base64 --decode > certificate.p12

&nbsp;      security create-keychain -p actions temp.keychain

&nbsp;      security import certificate.p12 -k temp.keychain -P "$APPLE\_CERT\_PASSWORD"

&nbsp;      codesign --deep --force --sign "Developer ID" dist/WatermarkTool.app

&nbsp;  ```



3\. \*\*Création DMG\*\*

&nbsp;  ```yaml

&nbsp;  - name: Create DMG

&nbsp;    run: |

&nbsp;      chmod +x build/installers/macos\_dmg.sh

&nbsp;      ./build/installers/macos\_dmg.sh

&nbsp;  ```



4\. \*\*Notarization (optionnel, si certificat)\*\*

&nbsp;  ```yaml

&nbsp;  - name: Notarize

&nbsp;    if: ${{ secrets.APPLE\_ID }}

&nbsp;    run: |

&nbsp;      xcrun notarytool submit dist/macos/\*.dmg \\

&nbsp;        --apple-id "${{ secrets.APPLE\_ID }}" \\

&nbsp;        --password "${{ secrets.APPLE\_APP\_PASSWORD }}" \\

&nbsp;        --team-id "${{ secrets.APPLE\_TEAM\_ID }}" \\

&nbsp;        --wait

&nbsp;  ```



5\. \*\*Upload artefacts\*\*

&nbsp;  ```yaml

&nbsp;  - uses: actions/upload-artifact@v3

&nbsp;    with:

&nbsp;      name: macos-binaries

&nbsp;      path: |

&nbsp;        dist/macos/\*.dmg

&nbsp;        dist/macos/checksums.txt

&nbsp;  ```



\### Job 5 : Create Release



\*\*Runner\*\* : `ubuntu-latest`



\*\*Dépendances\*\* : Jobs `build-windows`, `build-linux`, `build-macos` réussis



\*\*Étapes\*\* :



1\. \*\*Download tous les artefacts\*\*

&nbsp;  ```yaml

&nbsp;  - uses: actions/download-artifact@v3

&nbsp;    with:

&nbsp;      path: artifacts/

&nbsp;  ```



2\. \*\*Extraction version\*\*

&nbsp;  ```yaml

&nbsp;  - name: Get version

&nbsp;    id: version

&nbsp;    run: |

&nbsp;      VERSION=${GITHUB\_REF#refs/tags/v}

&nbsp;      echo "version=$VERSION" >> $GITHUB\_OUTPUT

&nbsp;  ```



3\. \*\*Génération changelog\*\*

&nbsp;  ```yaml

&nbsp;  - name: Generate changelog

&nbsp;    id: changelog

&nbsp;    run: |

&nbsp;      # Extraction depuis CHANGELOG.md ou commits

&nbsp;      sed -n "/## \\\[${VERSION}\\]/,/## \\\[/p" CHANGELOG.md | head -n -1 > release\_notes.md

&nbsp;  ```



4\. \*\*Création release\*\*

&nbsp;  ```yaml

&nbsp;  - uses: softprops/action-gh-release@v1

&nbsp;    with:

&nbsp;      name: Release v${{ steps.version.outputs.version }}

&nbsp;      body\_path: release\_notes.md

&nbsp;      draft: false

&nbsp;      prerelease: false

&nbsp;      files: |

&nbsp;        artifacts/windows-binaries/\*

&nbsp;        artifacts/linux-binaries/\*

&nbsp;        artifacts/macos-binaries/\*

&nbsp;    env:

&nbsp;      GITHUB\_TOKEN: ${{ secrets.GITHUB\_TOKEN }}

&nbsp;  ```



\### Workflows secondaires



\#### Tests automatiques : `.github/workflows/tests.yml`



\*\*Déclenchement\*\* :

\- Push sur `main`, `dev`

\- Pull requests vers `main`



\*\*Jobs\*\* :

\- Tests unitaires (matrice Python 3.10, 3.11, 3.12)

\- Linting (flake8, black)

\- Type checking (mypy)



\#### Qualité du code : `.github/workflows/lint.yml`



\*\*Déclenchement\*\* :

\- Pull requests



\*\*Jobs\*\* :

\- Vérification formatage (black --check)

\- Linting (flake8)

\- Security check (bandit)



\### Badges pour README



```markdown

!\[Build](https://github.com/username/watermark-tool/workflows/Build%20and%20Release/badge.svg)

!\[Tests](https://github.com/username/watermark-tool/workflows/Tests/badge.svg)

!\[License](https://img.shields.io/github/license/username/watermark-tool)

!\[Downloads](https://img.shields.io/github/downloads/username/watermark-tool/total)

!\[Latest Release](https://img.shields.io/github/v/release/username/watermark-tool)

```



\### Process de release complet



1\. \*\*Développement\*\* : Travail sur branches feature

2\. \*\*Merge\*\* : PR vers `dev`, puis vers `main`

3\. \*\*Tag\*\* : `git tag v1.0.0 \&\& git push --tags`

4\. \*\*Automatique\*\* :

&nbsp;  - Tests exécutés

&nbsp;  - Builds lancés sur 3 plateformes

&nbsp;  - Release créée avec tous les binaires

&nbsp;  - Notifications (optionnel : Discord, Slack)

5\. \*\*Publication\*\* : Release visible sur GitHub avec binaires téléchargeables



\### Optimisations



\#### Cache des dépendances

```yaml

\- uses: actions/cache@v3

&nbsp; with:

&nbsp;   path: ~/.cache/pip

&nbsp;   key: ${{ runner.os }}-pip-${{ hashFiles('\*\*/requirements.txt') }}

```



\#### Builds parallèles

\- Les 3 builds (Windows, Linux, macOS) s'exécutent en parallèle

\- Temps total : ~10-15 minutes au lieu de 30+ en séquentiel



\#### Retry en cas d'échec

```yaml

\- uses: nick-invision/retry@v2

&nbsp; with:

&nbsp;   timeout\_minutes: 10

&nbsp;   max\_attempts: 3

&nbsp;   command: python build/build\_windows.py

```



---



\## 🔒 Considérations Techniques



\### Sécurité

\- Validation des entrées utilisateur

\- Gestion sécurisée des chemins de fichiers

\- Pas d'exécution de code arbitraire

\- Permissions Windows appropriées



\### Performance

\- Traitement asynchrone pour l'UI

\- Optimisation des images (compression, thumbnails)

\- Mise en cache des previews

\- Gestion mémoire pour gros fichiers



\### Compatibilité



\#### Windows

\- Windows 10 (version 1809+)

\- Windows 11

\- Architecture x64

\- Indépendant de l'installation Python (standalone)



\#### Linux

\- \*\*Distributions supportées\*\* :

&nbsp; - Ubuntu 20.04+, Debian 11+

&nbsp; - Fedora 35+, RHEL 8+

&nbsp; - Arch Linux, Manjaro

&nbsp; - Linux Mint, Pop!\_OS

\- \*\*Environnements de bureau\*\* :

&nbsp; - GNOME (avec Nautilus)

&nbsp; - KDE Plasma (avec Dolphin)

&nbsp; - XFCE, MATE, Cinnamon (support partiel)

\- Architecture x86\_64

\- Dépendances système minimales (incluses dans AppImage)



\#### macOS

\- macOS 11 Big Sur ou supérieur

\- Architecture :

&nbsp; - Intel (x86\_64)

&nbsp; - Apple Silicon (arm64)

&nbsp; - Universal Binary (les deux)

\- Indépendant de l'installation Python (bundle)



\### Maintenance

\- Code modulaire et documenté

\- Tests automatisés

\- Versioning sémantique

\- Changelog



---



\## 📊 Métriques de Succès



\### Technique

\- Taux de couverture de tests > 80%

\- Temps de traitement < 2s par image (moyenne)

\- Taille des installateurs :

&nbsp; - Windows : < 40 MB

&nbsp; - Linux AppImage : < 45 MB

&nbsp; - macOS DMG : < 50 MB

\- Temps de démarrage de l'app < 3s

\- Build CI/CD réussi sur les 3 plateformes

\- Temps de build GitHub Actions < 15 minutes



\### Utilisateur

\- Installation en < 3 minutes (toutes plateformes)

\- Utilisation du mode quick sans documentation

\- Support des formats les plus courants (PNG, JPG, PDF)

\- Aucune dépendance externe à installer

\- Intégration menu contextuel fonctionnelle



\### Projet

\- Documentation complète (3 plateformes)

\- Code open-source sur GitHub

\- Release automatisée via GitHub Actions

\- Au moins 3 releases stables (v1.0.x)

\- README avec badges (build status, downloads, license)



\### Adoption (objectifs 6 mois)

\- 100+ téléchargements

\- 10+ stars GitHub

\- 3+ contributeurs

\- Aucun bug critique ouvert

\- Support communautaire actif (issues/discussions)



---



\## 🚀 Roadmap



\### v1.0 (MVP - Multi-plateforme)

\- ✅ Support Windows, Linux, macOS

\- ✅ Mode Quick (clic droit)

\- ✅ Application complète (drag \& drop, preview)

\- ✅ Support images (PNG, JPG, JPEG, BMP, GIF)

\- ✅ Support PDF basique

\- ✅ CI/CD GitHub Actions complet

\- ✅ Installateurs natifs pour chaque plateforme

\- ✅ Intégration menus contextuels (Windows, Nautilus, Dolphin, Finder)



\### v1.1 (Améliorations sécurité)

\- Templates de filigrane prédéfinis :

&nbsp; - CONFIDENTIEL

&nbsp; - BROUILLON

&nbsp; - COPIE

&nbsp; - ORIGINAL

&nbsp; - Personnalisés (sauvegardés)

\- Ajout de métadonnées :

&nbsp; - Nom de l'utilisateur

&nbsp; - Date et heure

&nbsp; - Service/Département

&nbsp; - Numéro de version

\- Rotation du filigrane (diagonal)

\- Opacité personnalisable



\### v1.2 (Fonctionnalités avancées)

\- Batch processing amélioré avec barre de progression

\- Positionnement avancé (coins, personnalisé)

\- Multi-pages PDF (filigrane différent par page)

\- Historique des filigranes utilisés

\- Export/Import de configurations



\### v1.3 (Entreprise)

\- Templates d'entreprise (logo + texte)

\- Filigrane avec QR code (traçabilité)

\- Logs d'utilisation (audit trail)

\- Configuration centralisée (pour déploiement)

\- Mode ligne de commande (CLI) pour automatisation



\### v2.0 (Professionnalisation)

\- Interface multilingue (FR, EN, ES, DE)

\- Thèmes personnalisables

\- API REST pour intégration

\- Plugin pour logiciels tiers (ex: navigateurs)

\- Support formats additionnels (TIFF, SVG)



\### Hors scope (volontairement exclus)

\- ❌ Support vidéo (hors périmètre documentaire)

\- ❌ Watermark image/logo complexe (focus texte)

\- ❌ Éditeur graphique intégré

\- ❌ OCR ou traitement d'image avancé



---



\## 📞 Support et Contribution



\### Canaux de support

\- GitHub Issues pour les bugs

\- GitHub Discussions pour les questions

\- Documentation en ligne



\### Contribution

\- Guide de contribution (CONTRIBUTING.md)

\- Code of Conduct

\- Process de Pull Request

\- Revue de code



\### Communauté

\- Discord (optionnel)

\- Twitter/X pour les annonces

\- Blog pour les tutoriels



---



\*\*Date de création\*\* : Février 2026  

\*\*Dernière mise à jour\*\* : Février 2026  

\*\*Statut\*\* : Spécification complète - Prêt pour développement

