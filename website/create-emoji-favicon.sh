#!/bin/bash
# create-emoji-favicon.sh - Crear favicon desde emoji usando Python

cd "$(dirname "$0")"

cat > create_favicon.py << 'EOF'
from PIL import Image, ImageDraw, ImageFont
import sys

# Crear imagen 32x32
size = 32
img = Image.new('RGB', (size, size), color='#0a0a0a')
draw = ImageDraw.Draw(img)

# Intentar usar una fuente del sistema
try:
    font = ImageFont.truetype('/System/Library/Fonts/SFNS.ttf', 24)
except:
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Monaco.dfont', 24)
    except:
        font = ImageFont.load_default()

# Dibujar el símbolo >_
text = ">_"
draw.text((3, 5), text, fill='#60a5fa', font=font)

# Guardar como ICO
img.save('favicon.ico', format='ICO', sizes=[(32, 32)])
print('✓ favicon.ico creado')

# Guardar también como PNG
img.save('favicon-32.png', format='PNG')
print('✓ favicon-32.png creado')
EOF

echo "🎨 Creando favicon..."
python3 create_favicon.py

if [ $? -eq 0 ]; then
    rm create_favicon.py
    echo ""
    echo "✅ Favicon creado exitosamente"
    ls -lh favicon.* 2>/dev/null | awk '{printf "   %-30s %8s\n", $9, $5}'
else
    echo "⚠️  Error creando favicon"
    echo "Usando alternativa con SVG solamente"
fi






















