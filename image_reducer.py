from PIL import Image
import os

# Abre la imagen
original_img_path = "/home/atp/downloads/ATP.png"
compressed_img_path = "/home/atp/downloads/ATP_compressed.png"
imagen = Image.open(original_img_path)

# Define el tamaño máximo deseado en bytes (3.5 MB)
tamano_maximo = 3.5 * 1024 * 1024  # Convertimos MB a bytes

# Comprime la imagen reduciendo la calidad hasta que el tamaño sea menor o igual al máximo
while True:
    # Guarda la imagen con la calidad actual
    imagen.save(compressed_img_path, optimize=True, quality=100)  # Puedes ajustar la calidad de 0 a 100
    
    # Verifica el tamaño del archivo
    if os.path.getsize(compressed_img_path) <= tamano_maximo:
        break
    else:
        # Reducimos la calidad en 5 puntos porcentuales
        imagen = Image.open(original_img_path)
        imagen.save(compressed_img_path, optimize=True, quality=imagen.info['quality'] - 5)

print("Compresión completa.")