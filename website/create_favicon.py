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
