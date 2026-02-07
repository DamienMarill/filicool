#!/bin/bash
# 🍭 Fililico - Linux AppImage Builder
# Script pour créer un AppImage

set -e

APP_NAME="Fililico"
VERSION="1.0.0"
ARCH="x86_64"

# Couleurs
PINK='\033[0;35m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${PINK}🍭 Building Fililico AppImage...${NC}"

# Dossiers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BUILD_DIR="$PROJECT_ROOT/build/appimage"
APPDIR="$BUILD_DIR/$APP_NAME.AppDir"

# Nettoyer
rm -rf "$BUILD_DIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copier l'exécutable
if [ -f "$PROJECT_ROOT/dist/Fililico" ]; then
    cp "$PROJECT_ROOT/dist/Fililico" "$APPDIR/usr/bin/fililico"
else
    echo "⚠️  Exécutable non trouvé, utilisation du script Python"
    echo "#!/bin/bash
cd \"\$(dirname \"\$0\")/../..\"
python3 main.py \"\$@\"" > "$APPDIR/usr/bin/fililico"
fi
chmod +x "$APPDIR/usr/bin/fililico"

# Copier les assets
cp -r "$PROJECT_ROOT/assets" "$APPDIR/usr/share/"
cp -r "$PROJECT_ROOT/web" "$APPDIR/usr/share/"

# Icône
if [ -f "$PROJECT_ROOT/assets/images/logo.png" ]; then
    cp "$PROJECT_ROOT/assets/images/logo.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/fililico.png"
    cp "$PROJECT_ROOT/assets/images/logo.png" "$APPDIR/fililico.png"
fi

# Desktop entry
cat > "$APPDIR/fililico.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Fililico
GenericName=Watermark Tool
Comment=🍭 Application de filigranage kawaii
Exec=fililico %f
Icon=fililico
Terminal=false
Categories=Graphics;Utility;
MimeType=image/png;image/jpeg;image/bmp;image/gif;application/pdf;
Keywords=watermark;filigrane;image;pdf;
EOF

cp "$APPDIR/fililico.desktop" "$APPDIR/usr/share/applications/"

# AppRun
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib/:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/fililico" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Télécharger appimagetool si nécessaire
APPIMAGETOOL="$BUILD_DIR/appimagetool"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo -e "${PINK}📥 Downloading appimagetool...${NC}"
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -O "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
fi

# Créer l'AppImage
OUTPUT="$PROJECT_ROOT/build/installers/${APP_NAME}-${VERSION}-${ARCH}.AppImage"
mkdir -p "$(dirname "$OUTPUT")"

echo -e "${PINK}📦 Creating AppImage...${NC}"
ARCH=$ARCH "$APPIMAGETOOL" "$APPDIR" "$OUTPUT"

echo -e "${GREEN}✅ AppImage created: $OUTPUT${NC}"
