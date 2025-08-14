#!/usr/bin/env python3
"""Script per creare icone PWA base da SVG"""

import base64
from PIL import Image, ImageDraw
import io

def create_pwa_icon(size):
    """Crea un'icona PWA di base con il size specificato"""
    # Crea immagine con sfondo verde Dashboard 555
    img = Image.new('RGB', (size, size), '#00d4aa')
    draw = ImageDraw.Draw(img)
    
    # Disegna simbolo finanziario stilizzato
    # Bordo esterno
    margin = size // 8
    draw.rectangle([margin, margin, size-margin, size-margin], 
                  outline='white', width=max(2, size//50))
    
    # Simbolo "555"
    font_size = size // 6
    text_y = size // 2 - font_size // 2
    
    # Disegna rettangolo per simulare "555"
    rect_width = size // 3
    rect_height = size // 8
    rect_x = (size - rect_width) // 2
    rect_y = (size - rect_height) // 2
    
    draw.rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], 
                  fill='white')
    
    return img

# Crea tutte le icone necessarie
sizes = [72, 96, 128, 144, 152, 192, 384, 512]

for size in sizes:
    icon = create_pwa_icon(size)
    filename = f"assets/icon-{size}x{size}.png"
    icon.save(filename, 'PNG')
    print(f"✅ Creata icona: {filename}")

print("🎉 Tutte le icone PWA create!")
