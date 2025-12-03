#!/bin/bash
# generate-favicons.sh - Generar favicons desde SVG

echo "🎨 Generando favicons..."
echo ""

# Verificar si rsvg-convert está instalado
if ! command -v rsvg-convert &> /dev/null; then
    echo "⚠️  rsvg-convert no instalado"
    echo "Instalando..."
    brew install librsvg
fi

cd "$(dirname "$0")"

# Generar PNG de 512x512 (alta calidad)
echo "→ Generando favicon-512.png..."
rsvg-convert -w 512 -h 512 favicon.svg -o favicon-512.png

# Generar PNG de 192x192 (PWA)
echo "→ Generando favicon-192.png..."
rsvg-convert -w 192 -h 192 favicon.svg -o favicon-192.png

# Generar PNG de 32x32 (standard)
echo "→ Generando favicon-32.png..."
rsvg-convert -w 32 -h 32 favicon.svg -o favicon-32.png

# Generar ICO (si imagemagick está disponible)
if command -v convert &> /dev/null; then
    echo "→ Generando favicon.ico..."
    convert favicon-32.png favicon.ico
else
    echo "⚠️  ImageMagick no disponible, saltando .ico"
    echo "   (Opcional: brew install imagemagick)"
fi

echo ""
echo "✅ Favicons generados:"
ls -lh favicon* | awk '{printf "   %-30s %8s\n", $9, $5}'
echo ""
echo "📤 Ahora copia los archivos al servidor:"
echo "   scp favicon.svg favicon.ico mytechzone@192.168.68.116:/home/mytechzone/n8n-lab/website/html/"

