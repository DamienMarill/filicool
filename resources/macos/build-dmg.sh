#!/bin/bash
# 🍭 Fillico - macOS DMG Builder
# Script pour créer un DMG

set -e

APP_NAME="Fillico"
VERSION="1.0.0"

# Couleurs
PINK='\033[0;35m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${PINK}🍭 Building Fillico DMG...${NC}"

# Dossiers
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
BUILD_DIR="$PROJECT_ROOT/build/dmg"
APP_DIR="$BUILD_DIR/$APP_NAME.app"
DMG_DIR="$BUILD_DIR/dmg_contents"

# Nettoyer
rm -rf "$BUILD_DIR"
mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

# Info.plist
cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>French</string>
    <key>CFBundleExecutable</key>
    <string>Fillico</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>dev.marill.fillico</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>Fillico</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>${VERSION}</string>
    <key>CFBundleVersion</key>
    <string>${VERSION}</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>png</string>
                <string>jpg</string>
                <string>jpeg</string>
                <string>gif</string>
                <string>bmp</string>
                <string>pdf</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Watermarkable Document</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
        </dict>
    </array>
</dict>
</plist>
EOF

# Copier l'exécutable
if [ -f "$PROJECT_ROOT/dist/Fillico" ]; then
    cp "$PROJECT_ROOT/dist/Fillico" "$APP_DIR/Contents/MacOS/Fillico"
else
    echo "⚠️  Exécutable non trouvé, création d'un script wrapper"
    cat > "$APP_DIR/Contents/MacOS/Fillico" << 'WRAPPER'
#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/../Resources"
python3 main.py "$@"
WRAPPER
    chmod +x "$APP_DIR/Contents/MacOS/Fillico"
fi

# Copier les ressources
cp -r "$PROJECT_ROOT/assets" "$APP_DIR/Contents/Resources/"
cp -r "$PROJECT_ROOT/web" "$APP_DIR/Contents/Resources/"
cp -r "$PROJECT_ROOT/src" "$APP_DIR/Contents/Resources/"
cp "$PROJECT_ROOT/main.py" "$APP_DIR/Contents/Resources/"
cp "$PROJECT_ROOT/requirements.txt" "$APP_DIR/Contents/Resources/"

# Icône (conversion si iconutil disponible)
if [ -f "$PROJECT_ROOT/assets/images/logo.png" ]; then
    ICONSET="$BUILD_DIR/AppIcon.iconset"
    mkdir -p "$ICONSET"
    
    # Créer les différentes tailles
    sips -z 16 16 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_16x16.png" 2>/dev/null || true
    sips -z 32 32 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_16x16@2x.png" 2>/dev/null || true
    sips -z 32 32 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_32x32.png" 2>/dev/null || true
    sips -z 64 64 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_32x32@2x.png" 2>/dev/null || true
    sips -z 128 128 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_128x128.png" 2>/dev/null || true
    sips -z 256 256 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_128x128@2x.png" 2>/dev/null || true
    sips -z 256 256 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_256x256.png" 2>/dev/null || true
    sips -z 512 512 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_256x256@2x.png" 2>/dev/null || true
    sips -z 512 512 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_512x512.png" 2>/dev/null || true
    sips -z 1024 1024 "$PROJECT_ROOT/assets/images/logo.png" --out "$ICONSET/icon_512x512@2x.png" 2>/dev/null || true
    
    # Convertir en .icns
    iconutil -c icns "$ICONSET" -o "$APP_DIR/Contents/Resources/AppIcon.icns" 2>/dev/null || true
fi

# Créer le DMG
mkdir -p "$DMG_DIR"
cp -r "$APP_DIR" "$DMG_DIR/"

# Lien vers Applications
ln -sf /Applications "$DMG_DIR/Applications"

# Créer le DMG
OUTPUT="$PROJECT_ROOT/build/installers/${APP_NAME}-${VERSION}.dmg"
mkdir -p "$(dirname "$OUTPUT")"

hdiutil create -volname "$APP_NAME" -srcfolder "$DMG_DIR" -ov -format UDZO "$OUTPUT"

echo -e "${GREEN}✅ DMG created: $OUTPUT${NC}"
